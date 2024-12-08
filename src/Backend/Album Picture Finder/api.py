from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.responses import JSONResponse
import os
from PIL import Image
from cache import preprocess_database_images
from retrieval_and_output import preprocess_query_image, output_similarity

'''
This API will:
1. Accept a query image request and validate it.
2. Preprocess database images and count/sort similarity to the query image.
3. Return a JSON response with rank, pic_name, audio_file, and distance.
'''

# FastAPI app
app = FastAPI()

# Parameters
IMAGE_DIRECTORY = "C:\\Users\\omgit\\repos\\Tugas Besar Semester 3\\Algeo02-23013\\src\\Data\\Dataset"
MAPPER_FILE = "C:\\Users\\omgit\\repos\\Tugas Besar Semester 3\\Algeo02-23013\\src\\Data\\mapper.txt"
RESIZE_DIM = 512  # Number of pixels (for image resizing)
N_COMPONENTS = 8  # Number of principal components
TOP_N_IMAGES = 6  # Number of top similar images to return

# Check if the IMAGE_DIRECTORY exists
if not os.path.exists(IMAGE_DIRECTORY):
    raise FileNotFoundError(f"The specified image directory does not exist: {IMAGE_DIRECTORY}")

# Check if the MAPPER_FILE exists
if not os.path.exists(MAPPER_FILE):
    raise FileNotFoundError(f"The specified mapper file does not exist: {MAPPER_FILE}")

# Load mapper file into a dictionary
def load_mapper(mapper_file):
    """
    Load the mapper file and return a dictionary mapping pic_name to audio_file.
    """
    mapper = {}
    try:
        with open(mapper_file, "r") as file:
            for line_number, line in enumerate(file, start=1):
                # Skip the header line
                if line_number == 1:
                    continue
                stripped_line = line.strip()
                if not stripped_line:  # Skip empty lines
                    print(f"Skipping empty line {line_number}")
                    continue
                try:
                    # Expecting `audio_file pic_name` structure
                    audio_file, pic_name = stripped_line.split()
                    mapper[pic_name] = audio_file
                except ValueError:
                    print(f"Skipping invalid line {line_number}: {stripped_line}")
    except FileNotFoundError:
        print(f"Mapper file not found: {mapper_file}")
        raise
    except Exception as e:
        print(f"Error reading mapper file: {e}")
        raise
    return mapper

# Load the mapper
mapper = load_mapper(MAPPER_FILE)

# Preload and preprocess database images
image_files, mean, principal_components, image_projections = preprocess_database_images(IMAGE_DIRECTORY, RESIZE_DIM, N_COMPONENTS)

# API endpoint
@app.post("/picturefinder/")
async def find_similar_images(query_image: UploadFile = File(...)):
    try:
        # Ensure the query image is valid
        if not query_image.filename.lower().endswith(('png', 'jpg', 'jpeg')):
            raise HTTPException(status_code=400, detail="Invalid image format. Supported formats are: PNG, JPG, JPEG.")
        
        # Preprocess query image
        query_image = Image.open(query_image.file)
        query_projection = preprocess_query_image(mean, query_image, RESIZE_DIM, principal_components)
        
        # Calculate similarity (Euclidean distance)
        distances, _, top_n_indices = output_similarity(query_projection, image_projections, TOP_N_IMAGES)
        
        # Get results
        results = []
        for rank, index in enumerate(top_n_indices):
            pic_name = image_files[index]
            audio_file = mapper.get(pic_name, "Unknown")  # Default to "Unknown" if no mapping is found
            results.append({
                "rank": rank + 1,
                "pic_name": pic_name,
                "audio_file": audio_file,
                "distance": float(distances[index]),
            })
        
        return JSONResponse(content={"similar_images": results})
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing the query image: {str(e)}")
