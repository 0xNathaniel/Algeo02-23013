import numpy as np

def standardize_data(images):
    print("Standardizing data...")
    
    mean = np.mean(images, axis=1, keepdims=True)
    standardized_images = images - mean
    return standardized_images, mean