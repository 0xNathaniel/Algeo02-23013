import numpy as np

# Count the average of an image's processed grayscale values
def count_average(grayscale_values):
    # Sum and count accumulator
    return np.mean(grayscale_values)

# Standardize an image's grayscale values
def standardize(grayscale_values):
    # Standardize or center each pixels
    standardized_values -= count_average(grayscale_values)
    # Return standarized grayscale values
    return standardized_values