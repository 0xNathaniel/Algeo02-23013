import os
from data_centering import standardize
from image_processing_and_loading import load_and_process
from pca import pca_pipeline
from similarity import process_query_image, calculate_similarity
from PIL import Image
import numpy as np

# Number of principal components for PCA
n_components = 5
n_images = 5  # Top N most similar images to store

def main():
    directory = "src/Backend/Album Picture Finder/Album Pictures"
    query_image_name = "0.jpg"
    query_image_path = os.path.join(directory, query_image_name)
    image_files = [f for f in os.listdir(directory) if f.lower().endswith(('.png', '.jpg', '.jpeg'))]
    projected_query = process_query_image(query_image_path, n_components)

    similarity_list = []

    # Process each image and calculate the similarity
    for image_file in image_files:
        image_path = os.path.join(directory, image_file)
        grayscale_values = load_and_process(image_path)
        standardized_values = standardize(grayscale_values)
        projected_image = pca_pipeline(standardized_values, n_components)
        similarity = calculate_similarity(projected_query, projected_image)
        similarity_list.append((similarity, image_file))

    similarity_list.sort(key=lambda x: x[0])
    top_n_images = similarity_list[:n_images]

    print(f"Top {n_images} most similar images to {query_image_path}:")
    for rank, (similarity, image_file) in enumerate(top_n_images, start=1):
        print(f"{rank}. {image_file} with similarity (distance) of {similarity}")

if __name__ == "__main__":
    main()
