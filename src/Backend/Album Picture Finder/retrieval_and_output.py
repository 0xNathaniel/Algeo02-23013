import os
import numpy as np
from PIL import Image
from image_processing_and_loading import load_and_process_images
from data_centering import standardize_data
from pca import perform_pca, get_principal_components, project_images
from similarity import calculate_euclidean_distance

# Parameters
image_directory = "src/Backend/Album Picture Finder/Album Pictures"  # Change to your image directory
query_image_name = "0.jpg"  # Change to your query image name
n_components = 8  # Number of principal components
n_images = 5  # Number of top similar images to return
resize_dim = 512  # Resize dimension (images will be resized to resize_dim x resize_dim)

def main():
    # Load and process database images
    images, image_files = load_and_process_images(image_directory, resize_dim)
    standardized_images, mean = standardize_data(images)
    _, _, eigenvector = perform_pca(standardized_images, n_components)
    principal_components = get_principal_components(eigenvector, n_components)
    image_projections = project_images(standardized_images, principal_components)
    
    # Load and process the query image
    query_image = Image.open(os.path.join(image_directory, query_image_name)).convert('L')
    query_image_resized = query_image.resize((resize_dim, resize_dim))
    query_image_array = np.array(query_image_resized).flatten()
    query_image_standardized = query_image_array - mean
    query_projection = np.dot(query_image_standardized, principal_components.T)
    
    # Calculate distances or similiarity
    distances = calculate_euclidean_distance(query_projection, image_projections)
    
    sorted_indices = np.argsort(distances)
    top_n_indices = sorted_indices[:n_images]
    
    # Display the results
    print(f"Top {n_images} most similar images to {query_image_name}:")
    for rank, index in enumerate(top_n_indices, start=1):
        print(f"{rank}. {image_files[index]} with distance {distances[index]}")

if __name__ == "__main__":
    main()
