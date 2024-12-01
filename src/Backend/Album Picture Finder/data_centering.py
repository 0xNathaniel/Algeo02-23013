import numpy as np

# Count the average of an image's processed grayscale values
def count_average(grayscale_values):
    # Sum and count accumulator
    return np.mean(grayscale_values)

# Standardize an image's grayscale values
def standardize(grayscale_values):
    # Standardize or center each pixels
    standardized_values = grayscale_values - count_average(grayscale_values)
    # Return standarized grayscale values
    return standardized_values

# Driver
def main():
    grayscale_values = np.array([120, 125, 130])

    print("Original Grayscale Values:")
    print(grayscale_values)

    # Standardize the grayscale values
    standardized_values = standardize(grayscale_values)

    print("\nStandardized Grayscale Values:")
    print(standardized_values)

if __name__ == "__main__":
    main()