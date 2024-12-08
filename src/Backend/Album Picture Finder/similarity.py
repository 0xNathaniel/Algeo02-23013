import numpy as np
#
def calculate_euclidean_distance(query_projection, image_projections):
    distances = np.linalg.norm(image_projections - query_projection, axis=1)
    return distances