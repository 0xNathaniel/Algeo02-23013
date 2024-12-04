import numpy as np
from PIL import Image

# Loads and process image into a 1D list of grayscale values
def load_and_process(image_path):
    # Load image and convert the pixels into the RGB format
    img = Image.open(image_path).convert("RGB")
    # Convert image to NumPy array
    img_array = np.array(img)
    # Calculate grayscale values using I(x,y) = 0.2989.R(x,y) + 0.5870.G(x,y) + 0.1140.B(x,y)
    grayscale_values = (
        0.2989 * img_array[:, :, 0] +  # Red 
        0.5870 * img_array[:, :, 1] +  # Green 
        0.1140 * img_array[:, :, 2]    # Blue 
    )
    # Return flattened 2D grayscale array (1D array)
    return grayscale_values.flatten()

# Driver
if __name__ == "__main__":
    directory = ""
    file_name = input("Test image file name: ")
    grayscale_values = load_and_process(directory + file_name)
    print(grayscale_values)