import os
from data_centering import standardize
from image_processing_and_loading import load_and_process
from pca import pca_pipeline
from similarity import process_query_image, calculate_similarity
from PIL import Image
import numpy as np

# Number of principal components for PCA
n_components = 5

def main():
    # Directory containing the images
    directory = "src/Backend/Album Picture Finder/Album Pictures"
    # Query image path (image to compare against others)
    query_image_path = os.path.join(directory, "0.jpg")
    #List all image files in the directory
    image_files = [f for f in os.listdir(directory) if f.lower().endswith(('.png', '.jpg', '.jpeg'))]
    #Process query image
    projected_query = process_query_image(query_image_path, n_components)
    #Track the most similar image
    min_distance = float('inf')
    most_similar_image = None

    for image_file in image_files:
        # Skip the query image itself
        #if image_file == os.path.basename(query_image_path):
            #continue

        # Full path of the image
        image_path = os.path.join(directory, image_file)

        # Process the image
        grayscale_values = load_and_process(image_path)
        standardized_values = standardize(grayscale_values)
        projected_image = pca_pipeline(standardized_values, n_components)

        # Calculate similarity (distance)
        similarity = calculate_similarity(projected_query, projected_image)

        # Check if this is the most similar image
        if similarity < min_distance:
            min_distance = similarity
            most_similar_image = image_file

    # Output the file name with the lowest distance
    print(f"The most similar image to {query_image_path} is {most_similar_image} with a distance of {min_distance}")

if __name__ == "__main__":
    main()
