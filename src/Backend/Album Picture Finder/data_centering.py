# Count the average of an image's processed grayscale values
def count_average(grayscale_values):
    # Sum and count accumulator
    sum = 0
    count = len(grayscale_values)
    # Calculate sum and count
    for i in range(count):
        sum += grayscale_values[i]
        
    return (sum / count)

# Standardize an image's grayscale values
def standardize(grayscale_values):
    count = len(grayscale_values)
    average = count_average(grayscale_values)
    # Standardize or center each pixels
    for i in range(count):
        grayscale_values[i] -= average
    # Return standarized grayscale values
    return grayscale_values