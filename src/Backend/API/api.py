import os
import tarfile
import zipfile
import rarfile
import py7zr
import shutil
import io
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
ALBUM_DIR = "../../Frontend/public/Data/Album Dataset"
AUDIO_DIR = "../../Frontend/public/Data/Music Dataset"
SUPPORTED_IMAGE_FILES = (".png", ".jpg", ".jpeg")
SUPPORTED_AUDIO_FILES = (".wav", ".mid", ".midi")
SUPPORTED_ARCHIVES = (".zip", ".tar", ".rar", ".7z")
MIDI_DIRECTORY = AUDIO_DIR
MAPPER_FILE = "../../Frontend/public/Data/mapper.txt"
RESIZE_DIM = 64
N_COMPONENTS = 8
TOP_N_IMAGES = 30
MAPPER_FILE_PATH = os.path.join(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../Frontend/public/Data/")), "mapper.txt")

dataset_midis = []
mapper = load_mapper(MAPPER_FILE)

# Ensure directories exist
if not os.path.exists(ALBUM_DIR):
    os.makedirs(ALBUM_DIR)

if not os.path.exists(AUDIO_DIR):
    os.makedirs(AUDIO_DIR)


if not os.path.exists(MIDI_DIRECTORY):
    raise FileNotFoundError(f"The specified MIDI directory does not exist: {MIDI_DIRECTORY}")

if not os.path.exists(MAPPER_FILE):
    raise FileNotFoundError(f"The specified mapper file does not exist: {MAPPER_FILE}")

image_files, principal_components, image_projections = preprocess_database_images(ALBUM_DIR, RESIZE_DIM, N_COMPONENTS)

app = FastAPI()
# Utility Functions

def validate_mapper_format(file_content: str):
    lines = file_content.strip().split("\n")

    first_line = lines[0].strip()
    if first_line != "audio_file audio_name pic_name":
        raise ValueError(f"Invalid file format. The first line must be 'audio_file audio_name pic_name', but got: '{first_line}'.")

    for line in lines[1:]:
        columns = line.strip().split()
        if len(columns) != 3:
            raise ValueError(f"Invalid format in line: '{line}'. Each line must contain exactly three columns: 'audio_file audio_name pic_name'.")

        audio_file, audio_name, pic_name = columns
        if not audio_file.endswith(".mid") or not (pic_name.endswith(".png") or pic_name.endswith(".jpg")):
            raise ValueError(f"Invalid file format in line: '{line}'. Audio file must end with '.mid' and image file must end with '.png' or '.jpg'.")
        
        if not audio_name.isalnum():
            raise ValueError(f"Invalid audio name in line: '{line}'. Audio name must be alphanumeric.")

    return lines

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

def extract_file(file_path: str, extraction_dir: str):
    """Extract files from a zip, tar, rar, or 7z archive."""
    if file_path.endswith(".zip"):
        try:
            with zipfile.ZipFile(file_path, 'r') as zip_ref:
                zip_ref.testzip()
                zip_ref.extractall(extraction_dir)
                return zip_ref.namelist()
        except zipfile.BadZipFile:
            raise ValueError("The uploaded file is not a valid zip file.")
    elif file_path.endswith(".tar") or file_path.endswith(".tar.gz") or file_path.endswith(".tgz") or file_path.endswith(".tar.bz2"):
        try:
            with tarfile.open(file_path, 'r:*') as tar_ref:
                tar_ref.extractall(extraction_dir)
                return tar_ref.getnames()
        except tarfile.TarError:
            raise ValueError("The uploaded file is not a valid tar file.")
    elif file_path.endswith(".rar"):
        try:
            with rarfile.RarFile(file_path, 'r') as rar_ref:
                rar_ref.extractall(extraction_dir)
                return rar_ref.namelist()
        except rarfile.Error:
            raise ValueError("The uploaded file is not a valid rar file.")
    elif file_path.endswith(".7z"):
        try:
            with py7zr.SevenZipFile(file_path, mode='r') as z_ref:
                z_ref.extractall(path=extraction_dir)
                return z_ref.getnames()
        except py7zr.exceptions.Bad7zFile:
            raise ValueError("The uploaded file is not a valid 7z file.")
    else:
        raise ValueError("Unsupported file format. Supported formats are zip, tar, rar, and 7z.")

def clear_directory(directory: str):
    """Clear the specified directory before saving new files."""
    if os.path.exists(directory):
        for filename in os.listdir(directory):
            file_path = os.path.join(directory, filename)
            if os.path.isdir(file_path):
                shutil.rmtree(file_path)
            else:
                os.remove(file_path)
    else:
        os.makedirs(directory)

def save_file(file: UploadFile, save_dir: str):
    """Save a regular file (image or audio) to the specified directory."""
    file_path = os.path.join(save_dir, file.filename)
    with open(file_path, "wb") as temp_file:
        shutil.copyfileobj(file.file, temp_file)
    return file_path

async def process_files(files: list[UploadFile], target_dir: str, supported_files: tuple):
    """Process and save uploaded files to the target directory."""
    clear_directory(target_dir)

    processed_files = {
        "files": [],
        "extracted_files": []
    }

    for file in files:
        temp_file_path = os.path.join(target_dir, file.filename)

        # Save the uploaded file temporarily
        with open(temp_file_path, "wb") as temp_file:
            shutil.copyfileobj(file.file, temp_file)

        # Check the file type
        if file.filename.endswith(supported_files):
            processed_files["files"].append(save_file(file, target_dir))
        elif file.filename.endswith(SUPPORTED_ARCHIVES):
            try:
                extracted_files = extract_file(temp_file_path, target_dir)
                processed_files["extracted_files"] += extracted_files
            except ValueError as e:
                raise HTTPException(status_code=400, detail=str(e))
        else:
            raise HTTPException(status_code=400, detail=f"Unsupported file type: {file.filename}")

        # Remove the temporary file
        os.remove(temp_file_path)

    return processed_files

# API Endpoints
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
                f.write(line)
        
        return JSONResponse(content={"message": "Mapper file successfully uploaded and saved to 'mapper.txt'."})
    
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing the file: {str(e)}")

@app.post("/upload-images/")
async def upload_images(files: list[UploadFile] = File(...)):
    try:
        processed_files = await process_files(files, ALBUM_DIR, SUPPORTED_IMAGE_FILES)
        return JSONResponse(content={
            "message": "Image files successfully uploaded and processed.",
            "processed_files": processed_files
        })
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing the uploaded image files: {str(e)}")

@app.post("/upload-music/")
async def upload_music(files: list[UploadFile] = File(...)):
    try:
        processed_files = await process_files(files, AUDIO_DIR, SUPPORTED_AUDIO_FILES)
        return JSONResponse(content={
            "message": "Music files successfully uploaded and processed.",
            "processed_files": processed_files
        })
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing the uploaded music files: {str(e)}")
