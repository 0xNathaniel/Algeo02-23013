from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.responses import JSONResponse
import os
import numpy as np
from PIL import Image
from cache import preprocess_database_images
from retrieval_and_output import preprocess_query_image, output_similarity

'''
This API will:
1. Accept a query image request and validate it
2. If it's valid, preprocess database images, count and sort the database images similarity to the query image
3. Returns a list (TOP_N_IMAGES) of dictionary
'''

# FastAPI app
app = FastAPI()

# Parameters
IMAGE_DIRECTORY = "src/Backend/Album Picture Finder/Album Pictures" # Album Pictures directory
RESIZE_DIM = 512 # Number of pixels (for image resizing)
N_COMPONENTS = 8 # Number of principal components
TOP_N_IMAGES = 24  # Number of top similar images to return

# Preload and preprocess database images
image_files, mean, principal_components, image_projections = preprocess_database_images(IMAGE_DIRECTORY, RESIZE_DIM, N_COMPONENTS)

# API
@app.post("/finder/")
async def find_similar_images(query_image: UploadFile = File(...)):
    try:
        # Preproces query image
        query_image = Image.open(query_image.file)
        query_projection = preprocess_query_image(mean, query_image, RESIZE_DIM, principal_components)
        # Calculate similarity (Euclidean distance)
        distances, _, top_n_indices = output_similarity(query_projection, image_projections, TOP_N_IMAGES)
        # Get results
        results = [
            {"rank": rank + 1, "image_name": image_files[index], "distance": float(distances[index])}
            for rank, index in enumerate(top_n_indices)
        ]
        return JSONResponse(content={"similar_images": results})
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing the query image: {str(e)}")