from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.responses import JSONResponse
import os
from PIL import Image
from cache import preprocess_database_images
from retrieval_and_output import preprocess_query_image, output_similarity
from mapper import load_mapper

# FastAPI app
app = FastAPI()

# Parameters 
IMAGE_DIRECTORY = "../../Data/Dataset"
MAPPER_FILE = "../../Data/mapper.txt"
RESIZE_DIM = 512  # Number of pixels (for image resizing)
N_COMPONENTS = 8  # Number of principal components
TOP_N_IMAGES = 6  # Number of top similar images to return

# Check if the IMAGE_DIRECTORY exists
if not os.path.exists(IMAGE_DIRECTORY):
    raise FileNotFoundError(f"The specified image directory does not exist: {IMAGE_DIRECTORY}")

# Check if the MAPPER_FILE exists
if not os.path.exists(MAPPER_FILE):
    raise FileNotFoundError(f"The specified mapper file does not exist: {MAPPER_FILE}")

# Load the mapper
mapper = load_mapper(MAPPER_FILE)

# Preload and preprocess database images
image_files, mean, principal_components, image_projections = preprocess_database_images(IMAGE_DIRECTORY, RESIZE_DIM, N_COMPONENTS)

# API endpoint
@app.post("/finder/")
async def find_similar_images(query_image: UploadFile = File(...)):
    try:
        # Ensure the query image is valid
        if not query_image.filename.lower().endswith(('png', 'jpg', 'jpeg')):
            raise HTTPException(status_code=400, detail="Invalid image format. Supported formats are: PNG, JPG, JPEG.")
        
        # Preprocess query image
        query_image = Image.open(query_image.file)
        query_projection = preprocess_query_image(mean, query_image, RESIZE_DIM, principal_components)
        
        # Calculate similarity (Euclidean distance)
        distances, _, top_n_indices = output_similarity(query_projection, image_projections, len(image_files))
        
        # Normalize the distances to percentages (0 - 100%)
        min_distance = min(distances)
        max_distance = max(distances)
        similarity_percentages = [
            100 * (1 - (dist - min_distance) / (max_distance - min_distance)) for dist in distances
        ]
        
        # Prepare the results with similarity percentages
        results = []
        for index, similarity_percentage in zip(top_n_indices, similarity_percentages):
            pic_name = image_files[index]
            audio_file = mapper.get(pic_name, "Unknown")
            results.append({
                "pic_name": pic_name,
                "audio_file": audio_file,
                "similarity_percentage": round(similarity_percentage, 2),
            })
        
        # Sort the results by similarity_percentage in descending order
        results_sorted = sorted(results, key=lambda x: x['similarity_percentage'], reverse=True)
        
        # Select only the top N results
        top_n_results = results_sorted[:TOP_N_IMAGES]
        
        # Assign ranks based on sorted results
        for i, result in enumerate(top_n_results):
            result['rank'] = i + 1
        
        return JSONResponse(content={"similar_images": top_n_results})
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing the query image: {str(e)}")
