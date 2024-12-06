import os
import numpy as np
from image_processing_and_loading import load_and_process_images
from data_centering import standardize_data
from pca import perform_svd, get_principal_components, project_images

# Local cache file
CACHE_FILE = "album_picture_finder_cache.txt" 

def load_cache():
    if not os.path.exists(CACHE_FILE):
        return None
    cache = {}
    with open(CACHE_FILE, "r") as f:
        for line in f:
            key, value = line.strip().split("=", 1)
            if key in {"mean", "principal_components", "image_projections"}:
                cache[key] = np.fromstring(value, sep=",")
            elif key == "image_files":
                cache[key] = value.split(",")
            elif key in {"n_components", "resize_dim"}:
                cache[key] = int(value)
    return cache

def save_cache(metadata, mean, principal_components, image_projections):
    with open(CACHE_FILE, "w") as f:
        f.write(f"image_files={','.join(metadata['image_files'])}\n")
        f.write(f"n_components={metadata['n_components']}\n")
        f.write(f"resize_dim={metadata['resize_dim']}\n")
        f.write(f"mean={','.join(map(str, mean.flatten()))}\n")
        f.write(f"principal_components={','.join(map(str, principal_components.flatten()))}\n")
        f.write(f"image_projections={','.join(map(str, image_projections.flatten()))}\n")

def check_cache(metadata):
    cache = load_cache()
    if not cache:
        # No cache exists
        return None 
    if (cache["image_files"] == metadata["image_files"] and
        cache["n_components"] == metadata["n_components"] and
        cache["resize_dim"] == metadata["resize_dim"]):
        # Cache matches
        return cache 
    # Cache doesn't match
    return None  

def preprocess_database_images(image_directory, resize_dim, n_components):
    # Load and process images
    images, image_files = load_and_process_images(image_directory, resize_dim)
    metadata = {
        "image_files": image_files,
        "n_components": n_components,
        "resize_dim": resize_dim,
    }
    # Check cache
    cache = check_cache(metadata)
    if cache:
        # Use cached data
        mean = cache["mean"].reshape((-1,))
        principal_components = cache["principal_components"].reshape((n_components, -1))
        image_projections = cache["image_projections"].reshape((-1, n_components))
    else:
        # Recompute new data
        standardized_images, mean = standardize_data(images)
        _, _, eigenvector = perform_svd(standardized_images, n_components)
        principal_components = get_principal_components(eigenvector, n_components)
        image_projections = project_images(standardized_images, principal_components)
        # Save to cache
        save_cache(metadata, mean, principal_components, image_projections)
    
    return image_files, mean, principal_components, image_projections
