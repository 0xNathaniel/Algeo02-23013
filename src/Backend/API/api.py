import os
import time
import tarfile
import zipfile
import rarfile
import py7zr
import shutil
import io
import sys
from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.responses import JSONResponse
from typing import Union
from PIL import Image
from mido import MidiFile
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../Album Picture Finder/")))
from retrieval_and_output import preprocess_query_image, output_similarity
from cache import preprocess_database_images
from mapper_album import load_mapper_album
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../Music Information Retrieval/")))
from find_most_similar import find_most_similar
from mapper_music import load_mapper_music

from fastapi.middleware.cors import CORSMiddleware

# FastAPI app
app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Directories and constants
IMAGE_DIRECTORY = "../../Frontend/public/Data/Album Dataset"
AUDIO_DIR = "../../Frontend/public/Data/Music Dataset"
SUPPORTED_IMAGE_FILES = (".png", ".jpg", ".jpeg")
SUPPORTED_AUDIO_FILES = (".wav", ".mid", ".midi")
SUPPORTED_ARCHIVES = (".zip", ".tar", ".rar", ".7z")
MIDI_MP3_DIRECTORY = AUDIO_DIR
MAPPER_FILE = "../../Frontend/public/Data/mapper.txt"
RESIZE_DIM = 64
N_COMPONENTS = 8
TOP_N_IMAGES = 30
MAPPER_FILE_PATH = os.path.join(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../Frontend/public/Data/")), "mapper.txt")
SOUNDFONT_PATH = "../../Frontend/public/Audio Sample/general_audio_sample.sf2"
OUTPUT_DIRECTORY = "../../Frontend/public/ConvertMP3"

dataset_midis = []
album_mapper = load_mapper_album(MAPPER_FILE)
music_mapper = load_mapper_music(MAPPER_FILE)


# Ensure directories exist
try:
    if os.listdir(IMAGE_DIRECTORY):  # Check if the directory is not empty
        image_files, principal_components, image_projections = preprocess_database_images(
            IMAGE_DIRECTORY, RESIZE_DIM, N_COMPONENTS
        )
    else:
        # If the directory is empty, initialize with empty values
        image_files, principal_components, image_projections = [], None, None
        print(f"Warning: The image directory {IMAGE_DIRECTORY} is empty.")
except Exception as e:
    # Handle any unexpected errors during initialization
    print(f"Error initializing image processing: {e}")
    image_files, principal_components, image_projections = [], None, None


if not os.path.exists(MAPPER_FILE):
    raise FileNotFoundError(f"The specified mapper file does not exist: {MAPPER_FILE}")

if not os.path.exists(MAPPER_FILE):
    raise FileNotFoundError(f"The specified mapper file does not exist: {MAPPER_FILE}")


# Ensure output directory exists
os.makedirs(OUTPUT_DIRECTORY, exist_ok=True)


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
    for filename in os.listdir(AUDIO_DIR):
        if filename.endswith(".mid") or filename.endswith(".midi"):
            file_path = os.path.join(AUDIO_DIR, filename)
            try:
                midi_obj = MidiFile(file_path)
                dataset_midis.append((filename, midi_obj))
            except Exception as e:
                print(f"Skipping {filename}: {e}")

load_dataset_midis()

def extract_file(file_path: str, extraction_dir: str):
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
    file_path = os.path.join(save_dir, file.filename)
    with open(file_path, "wb") as temp_file:
        shutil.copyfileobj(file.file, temp_file)
    return file_path

async def process_files(files: list[UploadFile], target_dir: str, supported_files: tuple):
    clear_directory(target_dir)

    processed_files = {
        "files": [],
        "extracted_files": []
    }

    for file in files:
        temp_file_path = os.path.join(target_dir, file.filename)

        with open(temp_file_path, "wb") as temp_file:
            shutil.copyfileobj(file.file, temp_file)

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

        os.remove(temp_file_path)

    return processed_files

async def process_files(files: list[UploadFile], target_dir: str, supported_files: tuple):
    os.makedirs(target_dir, exist_ok=True)

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
            processed_files["files"].append(temp_file_path)
        elif file.filename.endswith(SUPPORTED_ARCHIVES):
            try:
                extracted_files = extract_file(temp_file_path, target_dir)
                processed_files["extracted_files"] += extracted_files
            except ValueError as e:
                os.remove(temp_file_path)  
                raise HTTPException(status_code=400, detail=str(e))
        else:
            os.remove(temp_file_path)  
            raise HTTPException(status_code=400, detail=f"Unsupported file type: {file.filename}")

    return processed_files


# API Endpoints
@app.post("/image/")
async def find_similar_images(query_image: UploadFile = File(...)):
    global image_files, principal_components, image_projections
    
    start_time = time.perf_counter()
    
    if not image_files or len(image_files) == 0:
        raise HTTPException(
            status_code=400, 
            detail="The album dataset is empty. Please upload images to the dataset first."
        )
    if principal_components is None or principal_components.size == 0:
        raise HTTPException(
            status_code=400, 
            detail="Principal components are missing. Please ensure PCA is performed on the dataset."
        )
    if image_projections is None or image_projections.size == 0:
        raise HTTPException(
            status_code=400, 
            detail="Image projections are missing. Please ensure dataset processing is complete."
        )

    try:
        if not query_image.filename.lower().endswith(('png', 'jpg', 'jpeg')):
            raise HTTPException(status_code=400, detail="Invalid image format. Supported formats are: PNG, JPG, JPEG.")
        
        query_image = Image.open(query_image.file)
        query_projection = preprocess_query_image(query_image, RESIZE_DIM, principal_components)
        
        distances, _, top_n_indices = output_similarity(query_projection, image_projections, len(image_files))

        results = []
        for rank, index in enumerate(top_n_indices):
            pic_name = image_files[index]
            mapper_entry = album_mapper.get(pic_name, {})
            audio_file = mapper_entry.get("audio_file", "Unknown")
            audio_name = mapper_entry.get("audio_name", "Unknown")
            results.append({
                "rank": rank + 1,
                "pic_name": pic_name,
                "audio_file": audio_file,
                "audio_name": audio_name,
                "distance": distances[index],
            })
        
        max_distance = max(result['distance'] for result in results)
        similarity_percentages = [
            100 * (1 - result['distance'] / max_distance) if max_distance > 0 else 100 
            for result in results
        ]
        
        for i, result in enumerate(results):
            result['similarity_percentage'] = round(similarity_percentages[i], 2)
        
        top_n_results = results[:TOP_N_IMAGES]
        
        execution_time = time.perf_counter() - start_time
        
        return JSONResponse(content={"similar_images": top_n_results, "execution_time": execution_time})
    
    except HTTPException:
        raise  
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing the query image: {str(e)}")


@app.post("/music/")
async def find_similar_midi(query_midi: UploadFile = File(...)):
    start_time = time.perf_counter()

    try:
        if not (query_midi.filename.endswith(".mid") or query_midi.filename.endswith(".midi")):
            raise HTTPException(status_code=400, detail="Invalid file type. Only .mid or .midi files are allowed.")
        
        query_midi_bytes = await query_midi.read()
        
        query_midi_filelike = io.BytesIO(query_midi_bytes)

        query_midi_obj = MidiFile(file=query_midi_filelike)
        
        similarities = find_most_similar(query_midi_obj, dataset_midis)
        results = []
        for rank, audio_file, similarity in similarities:
            mapper_entry = music_mapper.get(audio_file, {})
            audio_name = mapper_entry.get("audio_name", "Unknown")
            pic_name = mapper_entry.get("pic_name", "Unknown")
            results.append({
                "rank": rank,
                "pic_name": pic_name,
                "audio_file": audio_file,
                "audio_name": audio_name,
                "similarity_percentage": similarity
            })
        
        execution_time = time.perf_counter() - start_time

        return JSONResponse(content={"similar_audio_files": results, "execution_time": execution_time})
    
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
async def upload_images(files: Union[list[UploadFile], UploadFile] = File(...)):
    global image_files, principal_components, image_projections  

    if not isinstance(files, list):
        files = [files]  

    try:
        processed_files = await process_files(files, IMAGE_DIRECTORY, SUPPORTED_IMAGE_FILES)

        if os.listdir(IMAGE_DIRECTORY):  
            image_files, principal_components, image_projections = preprocess_database_images(
                IMAGE_DIRECTORY, RESIZE_DIM, N_COMPONENTS
            )
        else:
            image_files, principal_components, image_projections = [], None, None
            print(f"Warning: The image directory {IMAGE_DIRECTORY} is still empty after upload.")

        return JSONResponse(content={
            "message": "Image files successfully uploaded and database re-processed.",
            "processed_files": processed_files
        })
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing the uploaded image files: {str(e)}")

@app.post("/upload-music/")
async def upload_music(files: Union[list[UploadFile], UploadFile] = File(...)):
    if not isinstance(files, list):
        files = [files] 

    try:
        # Process uploaded music files
        processed_files = await process_files(files, AUDIO_DIR, SUPPORTED_AUDIO_FILES)
        load_dataset_midis()
        return JSONResponse(content={
            "message": "Music files successfully uploaded and processed.",
            "processed_files": processed_files
        })
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing the uploaded music files: {str(e)}")
