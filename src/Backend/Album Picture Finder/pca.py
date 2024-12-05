import numpy as np

def perform_pca(images, n_components):
    U, S, Vt = np.linalg.svd(images, full_matrices=False)
    return U, S, Vt

def get_principal_components(eigenvector, n_components):
    return eigenvector[:n_components]

def project_images(images, principal_components):
    return np.dot(images, principal_components.T)
