from data_centering import standardize
from image_processing_and_loading import load_and_process
from PIL import Image
from pca import pca_pipeline
from similarity import process_query_image, calculate_similarity
import numpy as np

n_components = 1

def main():
    grayscale_values = load_and_process("src/Backend/Album Picture Finder/test.png")
    standardized_values = standardize(grayscale_values)
    projected_image = pca_pipeline(standardized_values, n_components)
    projected_query = process_query_image("src/Backend/Album Picture Finder/test3.png", n_components)
    similarity = calculate_similarity(projected_query, projected_image)
    print(similarity)
    
if __name__ == "__main__":
    main()