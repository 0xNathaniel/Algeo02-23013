import os
import zipfile
import io
import shutil
import sys
from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.responses import JSONResponse
from PIL import Image
from mido import MidiFile
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../Album Picture Finder")))
from retrieval_and_output import preprocess_query_image, output_similarity
from cache import preprocess_database_images
from mapper import load_mapper
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../Music information Retrieval")))
from find_most_similar import find_most_similar

# Directories and constants
EXTRACTION_DIR = os.path.join(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../Data/Dataset")))
MIDI_DIRECTORY = "../../Data/Dataset"
MAPPER_FILE = "../../Data/mapper.txt"
RESIZE_DIM = 64
N_COMPONENTS = 8
TOP_N_IMAGES = 30
MAPPER_FILE_PATH = os.path.join(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../Data/")), "mapper.txt")

dataset_midis = []
mapper = load_mapper(MAPPER_FILE)

# Ensure directories exist
if not os.path.exists(EXTRACTION_DIR):
    os.makedirs(EXTRACTION_DIR)

if not os.path.exists(MIDI_DIRECTORY):
    raise FileNotFoundError(f"The specified MIDI directory does not exist: {MIDI_DIRECTORY}")

if not os.path.exists(MAPPER_FILE):
    raise FileNotFoundError(f"The specified mapper file does not exist: {MAPPER_FILE}")

image_files, principal_components, image_projections = preprocess_database_images(EXTRACTION_DIR, RESIZE_DIM, N_COMPONENTS)

app = FastAPI()

# Utility Functions
def extract_zip_file(zip_file_path: str, extraction_dir: str):
    try:
        with zipfile.ZipFile(zip_file_path, 'r') as zip_ref:
            zip_ref.testzip()
            zip_ref.extractall(extraction_dir)
            return zip_ref.namelist()
    except zipfile.BadZipFile:
        raise ValueError("The uploaded file is not a valid zip file.")
    except Exception as e:
        raise ValueError(f"Error extracting zip file: {str(e)}")

def clear_dataset_directory(extraction_dir: str):
    existing_files = os.listdir(extraction_dir)
    if len(existing_files) >= 1:
        for file in existing_files:
            file_path = os.path.join(extraction_dir, file)
            if os.path.isdir(file_path):
                shutil.rmtree(file_path)
            else:
                os.remove(file_path)

def load_dataset_midis():
    global dataset_midis
    dataset_midis = []
    for filename in os.listdir(MIDI_DIRECTORY):
        if filename.endswith(".mid") or filename.endswith(".midi"):
            file_path = os.path.join(MIDI_DIRECTORY, filename)
            try:
                midi_obj = MidiFile(file_path)
                dataset_midis.append((filename, midi_obj))
            except Exception as e:
                print(f"Skipping {filename}: {e}")

load_dataset_midis()

# API Endpoints
@app.post("/upload-zip/")
async def upload_zip_file(file: UploadFile = File(...)):
    try:
        if not file.filename.endswith(".zip"):
            raise HTTPException(status_code=400, detail="Invalid file format. Only .zip files are allowed.")

        clear_dataset_directory(EXTRACTION_DIR)

        temp_zip_path = os.path.join(EXTRACTION_DIR, file.filename)

        with open(temp_zip_path, "wb") as temp_file:
            shutil.copyfileobj(file.file, temp_file)

        extracted_files = extract_zip_file(temp_zip_path, EXTRACTION_DIR)

        os.remove(temp_zip_path)

        return JSONResponse(content={"message": "Zip file successfully uploaded and extracted.", "extracted_files": extracted_files})
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing the zip file: {str(e)}")

@app.post("/image/")
async def find_similar_images(query_image: UploadFile = File(...)):
    try:
        if not query_image.filename.lower().endswith(('png', 'jpg', 'jpeg')):
            raise HTTPException(status_code=400, detail="Invalid image format. Supported formats are: PNG, JPG, JPEG.")
        
        query_image = Image.open(query_image.file)
        query_projection = preprocess_query_image(query_image, RESIZE_DIM, principal_components)
        distances, _, top_n_indices = output_similarity(query_projection, image_projections, len(image_files))

        results = []
        for rank, index in enumerate(top_n_indices):
            pic_name = image_files[index]
            mapper_entry = mapper.get(pic_name, {})
            audio_file = mapper_entry.get("audio_file", "Unknown")
            audio_name = mapper_entry.get("audio_name", "Unknown")
            results.append({
                "rank": rank + 1,
                "pic_name": pic_name,
                "audio_file": audio_file,
                "audio_name": audio_name,
                "distance": distances[index],
            })
        
        max_distance = max([result['distance'] for result in results])
        similarity_percentages = [
            100 * (1 - (result['distance']) / (max_distance)) for result in results
        ]
        
        for i, result in enumerate(results):
            result['similarity_percentage'] = round(similarity_percentages[i], 2)
        
        top_n_results = results[:TOP_N_IMAGES]
        
        return JSONResponse(content={"similar_images": top_n_results})
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing the query image: {str(e)}")

@app.post("/music/")
async def find_similar_midi(query_midi: UploadFile = File(...)):
    try:
        if not (query_midi.filename.endswith(".mid") or query_midi.filename.endswith(".midi")):
            raise HTTPException(status_code=400, detail="Invalid file type. Only .mid or .midi files are allowed.")
        
        query_midi_bytes = await query_midi.read()
        query_midi_filelike = io.BytesIO(query_midi_bytes)

        query_midi_obj = MidiFile(file=query_midi_filelike)
        
        similarities = find_most_similar(query_midi_obj, dataset_midis)
        results = []
        for rank, audio_file, similarity in similarities:
            mapper_entry = mapper.get(audio_file, {})
            audio_name = mapper_entry.get("audio_name", "Unknown")
            pic_name = mapper_entry.get("pic_name", "Unknown")
            results.append({
                "rank": rank,
                "pic_name": pic_name,
                "audio_file": audio_file,
                "audio_name": audio_name,
                "similarity_percentage": similarity
            })
        
        return JSONResponse(content={"similar_audio_files": results})
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing the query MIDI file: {str(e)}")

@app.post("/upload-mapper/")
async def upload_mapper_file(file: UploadFile = File(...)):
    try:
        file_content = await file.read()
        file_content = file_content.decode("utf-8")  
        
        valid_lines = validate_mapper_format(file_content)

        with open(MAPPER_FILE_PATH, "w") as f:
            for line in valid_lines:
                f.write(line + "\n")
        
        return JSONResponse(content={"message": "Mapper file successfully uploaded and saved to 'mapper.txt'."})
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing the file: {str(e)}")

def validate_mapper_format(file_content: str):
    lines = file_content.strip().split("\n")
    
    if lines[0].strip() != "audio_file pic_name":
        raise ValueError("Invalid file format. The first line must be 'audio_file pic_name'.")
    
    for line in lines[1:]:
        columns = line.strip().split()
        if len(columns) != 2:
            raise ValueError(f"Invalid format in line: '{line}'. Each line must contain exactly two columns.")
        
        audio_file, pic_name = columns
        if not audio_file.endswith(".mid") or not (pic_name.endswith(".png") or pic_name.endswith(".jpg")):
            raise ValueError(f"Invalid file format in line: '{line}'. Audio file must end with '.mid' and image file must end with '.png' or '.jpg'.")
    
    return lines