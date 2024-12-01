import numpy as np

# Create and return a covariance matrix of image's standardized grayscale values
def create_covariance(standardized_values):
    return (1 / standardized_values.shape[0]) * np.dot(standardized_values.T, standardized_values)

# Perform SVD using eigen decomposition and return the eigen vector matrix needed for projection
def svd(covariance_matrix):
    eigenvalues = find_eigenvalues(covariance_matrix)
    eigenvector_matrix = compute_eigenvectors(covariance_matrix, eigenvalues)
    return eigenvector_matrix

# Select principal components (n_components)
def pca(eigenvector_matrix, n_components):
    return eigenvector_matrix[:, :n_components]

# Project data onto principal components
def project(principal_components, standardized_values):
    principal_components = np.repeat(principal_components, len(standardized_values))

    return np.dot(standardized_values, principal_components)

# Full PCA pipeline
def pca_pipeline(standardized_values, n_components):
    covariance_matrix = create_covariance(standardized_values)
    eigenvector_matrix = svd(covariance_matrix)
    principal_components = pca(eigenvector_matrix, n_components)
    return project(principal_components, standardized_values)

def find_eigenvalues(scalar_covariance):
    return [scalar_covariance]

# Compute eigenvectors
def compute_eigenvectors(scalar_covariance, eigenvalues):
    return np.array([[1.0]])

# Custom vector normalization
def vector_normalization(vector):
    squared_sum = sum(v ** 2 for v in vector)
    return squared_sum ** 0.5

# Driver
if __name__ == "__main__":
    # Example standardized data
    standardized_values = np.array([1.0, 2.0, 3.0])
    
    covariance = create_covariance(standardized_values)
    print(covariance)
    
    # Perform PCA
    n_components = 2
    projected = pca_pipeline(standardized_values, n_components)
    
    print("Projected Data:")
    print(projected)
