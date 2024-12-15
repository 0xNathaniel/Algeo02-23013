import numpy as np

def perform_svd(images):
    print("Performing SVD...")
    
    U, S, Vt = np.linalg.svd(images, full_matrices=False)
    return U, S, Vt

def get_principal_components(eigenvector, n_components):
    print("Retrieving PCA...")
    
    return eigenvector[:n_components]

def project_images(images, principal_components):
    print("Projecting PCA to images...")
    
    return np.dot(images, principal_components.T)
