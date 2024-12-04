from data_centering import standardize
from image_processing_and_loading import load_and_process
from PIL import Image
from pca import pca_pipeline
import numpy as np

# Return projected query image using the PCA method
def process_query_image(query_path, n_components):
    grayscale_values = load_and_process(query_path)
    standardized_values = standardize(grayscale_values)
    projected_query = pca_pipeline(standardized_values, n_components)
    return projected_query

# Calculate the euclidean distance or the similarity between the projected query and dataset image (projected_image)
def calculate_similarity(projected_query, projected_image):
    query = np.array(projected_query).flatten()
    image = np.array(projected_image).flatten()
    squared_differences = (query - image) ** 2
    distance = np.sqrt(np.sum(squared_differences))
    return distance