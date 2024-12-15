import os
import numpy as np
from PIL import Image
from image_processing_and_loading import load_and_process_images
from data_centering import standardize_data
from pca import perform_svd, get_principal_components, project_images
from similarity import calculate_euclidean_distance

def preprocess_query_image(query_image, resize_dim, principal_components):
    grayscale_image = query_image.convert('L')
    resized_image = grayscale_image.resize((resize_dim, resize_dim))
    query_image_array = np.array(resized_image).flatten()
    query_image_standardized = query_image_array - np.mean(query_image_array)
    query_projection = np.dot(query_image_standardized, principal_components.T)
    
    return query_projection

def output_similarity(query_projection, image_projections, top_n_images):
    distances = calculate_euclidean_distance(query_projection, image_projections)
    sorted_indices = np.argsort(distances)
    top_n_indices = sorted_indices[:top_n_images]

    return distances, sorted_indices, top_n_indices