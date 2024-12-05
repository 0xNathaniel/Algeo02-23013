import numpy as np

def standardize_data(images):
    mean = np.mean(images, axis=0)
    standardized_images = images - mean
    return standardized_images, mean