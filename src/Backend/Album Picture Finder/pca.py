import numpy as np

def perform_pca(images, n_components):
    U, S, Vt = np.linalg.svd(images, full_matrices=False)
    principal_components = Vt[:n_components]
    return principal_components, U, S

def project_images(images, principal_components):
    return np.dot(images, principal_components.T)
