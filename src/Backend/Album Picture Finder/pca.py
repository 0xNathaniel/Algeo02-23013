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
    return np.dot(standardized_values, principal_components)

# Full PCA pipeline
def pca_pipeline(standardized_values, n_components):
    covariance_matrix = create_covariance(standardized_values)
    eigenvector_matrix = svd(covariance_matrix)
    principal_components = pca(eigenvector_matrix, n_components)
    return project(principal_components, standardized_values)

# Eigenvalue-related helper functions
def determinant(matrix):
    n = matrix.shape[0]
    if n == 2:
        return matrix[0, 0] * matrix[1, 1] - matrix[0, 1] * matrix[1, 0]
    det = 0
    for col in range(n):
        sub_matrix = np.delete(np.delete(matrix, 0, axis=0), col, axis=1)
        det += ((-1) ** col) * matrix[0, col] * determinant(sub_matrix)
    return det

def characteristic_polynomial(matrix):
    n = matrix.shape[0]
    def poly_func(lmbda):
        identity = np.eye(n)
        return determinant(lmbda * identity - matrix)
    return poly_func

def find_eigenvalues(matrix, start=-10, end=10, steps=1000):
    char_poly = characteristic_polynomial(matrix)
    lambdas = np.linspace(start, end, steps)
    eigenvalues = []
    for i in range(len(lambdas) - 1):
        if char_poly(lambdas[i]) * char_poly(lambdas[i + 1]) < 0:
            root = (lambdas[i] + lambdas[i + 1]) / 2
            if not any(np.isclose(root, ev, atol=1e-5) for ev in eigenvalues):
                eigenvalues.append(root)
    return eigenvalues

# Gaussian elimination and back substitution
def gaussian_elimination(matrix):
    matrix = matrix.astype(float)
    n, m = matrix.shape
    for i in range(n):
        max_row = i + np.argmax(abs(matrix[i:, i]))
        matrix[[i, max_row]] = matrix[[max_row, i]]
        if matrix[i, i] != 0:
            matrix[i] = matrix[i] / matrix[i, i]
        for j in range(i + 1, n):
            matrix[j] -= matrix[j, i] * matrix[i]
    return matrix

def back_substitution(matrix):
    n = matrix.shape[0]
    x = np.zeros(n)
    for i in range(n - 1, -1, -1):
        if matrix[i, i] == 0:
            x[i] = 1
        else:
            x[i] = -np.sum(matrix[i, i + 1:] * x[i + 1:]) / matrix[i, i]
    return x

# Compute eigenvectors
def compute_eigenvectors(matrix, eigenvalues):
    n = matrix.shape[0]
    eigenvectors = []
    for eigenvalue in eigenvalues:
        A_minus_lambda_I = matrix - eigenvalue * np.eye(n)
        row_echelon_form = gaussian_elimination(A_minus_lambda_I)
        null_vector = back_substitution(row_echelon_form)
        norm = vector_normalization(null_vector)
        if norm != 0:
            null_vector = null_vector / norm
        eigenvectors.append(null_vector)
    return np.array(eigenvectors).T

# Custom vector normalization
def vector_normalization(vector):
    squared_sum = sum(v ** 2 for v in vector)
    return squared_sum ** 0.5

# Driver
if __name__ == "__main__":
    # Example standardized data
    standardized_values = np.array([[1.0, 2.0, 3.0],
                                     [4.0, 5.0, 6.0],
                                     [7.0, 8.0, 9.0]])
    
    # Perform PCA
    n_components = 2
    projected = pca_pipeline(standardized_values, n_components)
    
    print("Projected Data:")
    print(projected)
