import os
from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.responses import JSONResponse
from PIL import Image
from retrieval_and_output import preprocess_query_image, output_similarity
from cache import preprocess_database_images
from mapper_album import load_mapper
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

# Parameters
RESIZE_DIM = 64  # Number of pixels (for image resizing)
IMAGE_DIRECTORY = "../../Frontend/public/Data/Album Dataset"
MAPPER_FILE = "../../Frontend/public/Data/mapper.txt"
N_COMPONENTS = 8  # Number of principal components
TOP_N_IMAGES = 30  # Number of top similar images to return

# Check if the IMAGE_DIRECTORY exists
if not os.path.exists(IMAGE_DIRECTORY):
    raise FileNotFoundError(f"The specified image directory does not exist: {IMAGE_DIRECTORY}")

# Check if the MAPPER_FILE exists
if not os.path.exists(MAPPER_FILE):
    raise FileNotFoundError(f"The specified mapper file does not exist: {MAPPER_FILE}")

# Load the mapper
mapper = load_mapper(MAPPER_FILE)

# Preload and preprocess database images
image_files, principal_components, image_projections = preprocess_database_images(IMAGE_DIRECTORY, RESIZE_DIM, N_COMPONENTS)

# API endpoint
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
        
        #min_distance = min([result['distance'] for result in results])
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


