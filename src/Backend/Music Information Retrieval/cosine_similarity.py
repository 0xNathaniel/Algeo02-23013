import numpy as np

def cosine_similarity_custom(vec1, vec2):
    # Calculating the dot product: sigma[i = 1..n] A[i]B[i]
    dot_product = np.dot(vec1, vec2)
    # Calculating norm A: sqrt(sigma[i = 1..n] A[i]^2)
    
    norm_a = np.linalg.norm(vec1)
    # Calculating norm B: sqrt(sigma[i = 1..n] B[i]^2)
    norm_b = np.linalg.norm(vec2)
    # Calculating cosine similarity: A.B / (norm A * norm B)
    if norm_a == 0 or norm_b == 0:
        return 0
    
    if (norm_a * norm_b == 0):
        return dot_product
    cosine_similarity = dot_product / (norm_a * norm_b)
    return cosine_similarity