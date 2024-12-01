import numpy as np
from PIL import Image

# Loads and process image into a 1D list of grayscale values
def load_and_process(image_path):
    # Load image
    img = Image.open(image_path).convert("RGB")
    # Convert image to NumPy array
    img_array = np.array(img)
    # Calculate grayscale values
    grayscale_values = (
        0.2989 * img_array[:, :, 0] +  # Red 
        0.5870 * img_array[:, :, 1] +  # Green 
        0.1140 * img_array[:, :, 2]    # Blue 
    )
    # Return flatten the 2D grayscale array into a 1D array
    return grayscale_values.flatten()