import numpy as np

# Create and return a covariance matrix of image's standardized grayscale values
def create_covariance(standardized_values):
    return (1 / standardized_values.shape[0]) * np.dot(standardized_values.T, standardized_values)

# Perform SVD and return the eigen vector matrix
def svd(covariance_matrix):
    covariance_matrix = covariance_matrix.reshape(1, -1)
    eigenvector_matrix, _, _ = np.linalg.svd(covariance_matrix)
    return eigenvector_matrix

# Select principal components (n_components)
def pca(eigenvector_matrix, n_components):
    return eigenvector_matrix[:, :n_components]

# Project data onto principal components
def project(principal_components, standardized_values):
    principal_components = np.repeat(principal_components, len(standardized_values))
    return np.dot(standardized_values, principal_components)

# Full PCA using SVD pipeline
def pca_pipeline(standardized_values, n_components):
    covariance_matrix = create_covariance(standardized_values)
    eigenvector_matrix = svd(covariance_matrix)
    principal_components = pca(eigenvector_matrix, n_components)
    return project(principal_components, standardized_values)

# Driver
if __name__ == "__main__":
    n_components = 2
    
    # Example of standardized data as test input
    standardized_values = np.array([100, 120, 130, 140, 150])
    
    # create_covariance test
    covariance_matrix = create_covariance(standardized_values)
    print("Covariance Matrix:")
    print(covariance_matrix)
    
    # svd test
    eigenvector_matrix = svd(covariance_matrix)
    print("Eigenvector Matrix:")
    print(eigenvector_matrix)
    
    # pca test
    principal_components = pca(eigenvector_matrix, n_components)
    print("Principal Components")
    print(principal_components)
    
    # project test
    projected = project(principal_components, standardized_values)
    print("Projected Data:")
    print(projected)
    
    #pca_pipeline test
    projected_pipeline = pca_pipeline(standardized_values, n_components)
    print("Projected Data Using Pipeline:")
    print(projected_pipeline)
