from PIL import Image

# Loads and process image into a 1D list of grayscale values
def load_and_process(image_path):
    # Load image
    img = Image.open(image_path).convert("RGB)")
    # Retrieve image's width and height
    width, height = img.size
    # 1D list for grayscale values
    grayscale_values = []
    # Grayscale value pixel creation
    for x in range(width):
        for y in range(height):
            r, g, b = img.getpixel((x, y))
            grayscale = 0.2989 * r + 0.5870 * g + 0.1140 * b
            grayscale_values.append(grayscale)
            
    return grayscale_values