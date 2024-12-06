import os
import numpy as np
from PIL import Image
from similarity import calculate_euclidean_distance

'''
def preprocess_database_images(image_directory, resize_dim, n_components):
    images, image_files = load_and_process_images(image_directory, resize_dim)
    standardized_images, mean = standardize_data(images)
    _, _, eigenvector = perform_svd(standardized_images, n_components)  
    principal_components = get_principal_components(eigenvector, n_components)
    image_projections = project_images(standardized_images, principal_components)
    return image_files, mean, principal_components, image_projections
'''
    
def preprocess_query_image(mean, query_image, resize_dim, principal_components):
    # Preprocess the query image using the calculated
    grayscale_image = query_image.convert('L')
    resized_image = grayscale_image.resize((resize_dim, resize_dim))
    query_image_array = np.array(resized_image).flatten()
        
    # Standardize the query image
    query_image_standardized = query_image_array - mean
        
    # Project the query image onto the principal components
    query_projection = np.dot(query_image_standardized, principal_components.T)
    return query_projection

def output_similarity(query_projection, image_projections, top_n_images):
    distances = calculate_euclidean_distance(query_projection, image_projections)
    sorted_indices = np.argsort(distances)
    top_n_indices = sorted_indices[:top_n_images]

    return distances, sorted_indices, top_n_indices