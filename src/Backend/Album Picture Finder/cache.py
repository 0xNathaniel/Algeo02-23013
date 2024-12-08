import os
import hashlib
import numpy as np
from image_processing_and_loading import load_and_process_images
from data_centering import standardize_data
from pca import perform_svd, get_principal_components, project_images

# Local cache file 
CACHE_FILE = "album_picture_finder_cache.txt"

def calculate_dataset_hash(image_files, image_directory):
    hash_md5 = hashlib.md5()
    for image_file in sorted(image_files):  # Sort to ensure consistent order
        image_path = os.path.join(image_directory, image_file)
        if os.path.exists(image_path):
            with open(image_path, "rb") as f:
                while chunk := f.read(8192):
                    hash_md5.update(chunk)
    return hash_md5.hexdigest()

def load_cache():
    if not os.path.exists(CACHE_FILE):
        print("Cache file does not exist.")
        return None
    cache = {}
    try:
        with open(CACHE_FILE, "r") as f:
            for line in f:
                key, value = line.strip().split("=", 1)
                if key in {"mean", "principal_components", "image_projections"}:
                    cache[key] = np.fromstring(value, sep=",")
                elif key in {"image_files", "dataset_hash"}:  # Ensure dataset_hash is loaded
                    cache[key] = value
                elif key in {"n_components", "resize_dim"}:
                    cache[key] = int(value)
        print("Cache loaded successfully.")
    except Exception as e:
        print(f"Error loading cache: {e}")
    return cache

def save_cache(metadata, mean, principal_components, image_projections, dataset_hash):
    try:
        # Ensure the directory exists
        directory = os.path.dirname(CACHE_FILE)
        if not os.path.exists(directory):
            os.makedirs(directory)
        
        # Write to cache file
        print(f"Saving cache to: {CACHE_FILE}")
        with open(CACHE_FILE, "w") as f:
            f.write(f"image_files={','.join(metadata['image_files'])}\n")
            f.write(f"n_components={metadata['n_components']}\n")
            f.write(f"resize_dim={metadata['resize_dim']}\n")
            f.write(f"dataset_hash={dataset_hash}\n")  # Ensure dataset_hash is saved
            f.write(f"mean={','.join(map(str, mean.flatten()))}\n")
            f.write(f"principal_components={','.join(map(str, principal_components.flatten()))}\n")
            f.write(f"image_projections={','.join(map(str, image_projections.flatten()))}\n")
        print("Cache successfully written.")
    except Exception as e:
        print(f"Failed to write cache: {e}")

def check_cache(metadata, dataset_hash):
    cache = load_cache()
    if not cache:
        print("No valid cache found.")
        return None
    
    # Check if the cached dataset hash exists and matches
    if ("dataset_hash" not in cache or
        cache["dataset_hash"] != dataset_hash or
        cache["image_files"] != ','.join(metadata["image_files"]) or
        cache["n_components"] != metadata["n_components"] or
        cache["resize_dim"] != metadata["resize_dim"]):
        print("Cache mismatch. Recomputing data...")
        return None
    
    print("Cache matches.")
    return cache

def preprocess_database_images(image_directory, resize_dim, n_components):
    try:
        # Load and process images
        images, image_files = load_and_process_images(image_directory, resize_dim)
        metadata = {
            "image_files": image_files,
            "n_components": n_components,
            "resize_dim": resize_dim,
        }

        # Calculate dataset hash
        dataset_hash = calculate_dataset_hash(image_files, image_directory)

        # Check cache
        cache = check_cache(metadata, dataset_hash)
        if cache:
            print("Using cached data...")
            mean = cache["mean"].reshape((-1,))
            principal_components = cache["principal_components"].reshape((n_components, -1))
            image_projections = cache["image_projections"].reshape((-1, n_components))
        else:
            print("Recomputing data...")
            standardized_images, mean = standardize_data(images)
            _, _, eigenvector = perform_svd(standardized_images, n_components)
            principal_components = get_principal_components(eigenvector, n_components)
            image_projections = project_images(standardized_images, principal_components)
            
            # Save to cache
            save_cache(metadata, mean, principal_components, image_projections, dataset_hash)
        
        return image_files, mean, principal_components, image_projections
    except Exception as e:
        print(f"Error during preprocessing: {e}")
        raise
