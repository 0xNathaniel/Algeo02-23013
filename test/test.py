import os
import sys
import numpy as np
from PIL import Image
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../src/Backend/Album Picture Finder/")))
from retrieval_and_output import preprocess_query_image, output_similarity
from cache import preprocess_database_images

# Parameters
image_directory = "src\Frontend\public\Data\Album Dataset"
#image_directory = "src/Backend/Album Picture Finder/Album Pictures"# Change to your image directory
query_image_name = "pic1.png"  # Change to your query image name
n_components = 64  # Number of principal components
n_images = 6  # Number of top similar images to return
resize_dim = 64  # Resize dimension (images will be resized to resize_dim x resize_dim)
top_n_images = 6 # # Number of top similar images to return

def main():
    # Load and process database images
    image_files, principal_components, image_projections = preprocess_database_images(image_directory, resize_dim, n_components)
    # Load and process the query image
    query_image = Image.open(os.path.join(image_directory, query_image_name)).convert('L')
    query_projection = preprocess_query_image(query_image, resize_dim, principal_components)
    # Calculate similarity (Euclidean distance)
    distances, _, top_n_indices = output_similarity(query_projection, image_projections, top_n_images)
    
    # Display the results
    print(f"Top {n_images} most similar images to {query_image_name}:")
    for rank, index in enumerate(top_n_indices, start=1):
        print(f"{rank}. {image_files[index]} with distance {distances[index]}")

if __name__ == "__main__":
    main()
