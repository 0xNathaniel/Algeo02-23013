from PIL import Image

def load_and_process(image_path):
    img = Image.open(image_path).convert("RGB)")
    
    width, height = img.size
    
    grayscale_values = []
    
    for x in range(width):
        for y in range(height):
            r, g, b = img.getpixel((x, y))
            grayscale = 0.2989 * r + 0.5870 * g + 0.1140 * b
            grayscale_values.append(grayscale)
            
    return grayscale_values
            