import os
import numpy as np
from PIL import Image

def load_and_process_images(image_directory, resize_dim):
    print("Loading and processing images...")    
    
    image_files = [f for f in os.listdir(image_directory) if f.lower().endswith(('.png', '.jpg', '.jpeg'))]
    images = []
    
    for image_file in image_files:
        image_path = os.path.join(image_directory, image_file)
        image = Image.open(image_path)
        grayscale_image = image.convert('L')
        resized_image = grayscale_image.resize((resize_dim, resize_dim))
        image_array = np.array(resized_image).flatten()
        images.append(image_array)
    
    return np.array(images), image_files