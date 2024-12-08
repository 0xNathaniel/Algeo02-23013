import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

from process_midi import process_midi
from process_midi import normalize_length
from absolute_tone_based import absolute_tone_based
from relative_tone_based import relative_tone_based
from first_tone_based import first_tone_based
from cosine_similarity import cosine_similarity_custom

def find_most_similar(query_file, dataset_features):

    query_atb, mean, std = process_midi(query_file)
    query_rtb, mean, std = process_midi(query_file)
    query_ftb, mean, std = process_midi(query_file)

    query_atb = absolute_tone_based(query_file)
    query_rtb = relative_tone_based(query_file)
    query_ftb = first_tone_based(query_file)

    if query_atb is None or query_rtb is None or query_ftb is None:
        print(f"Query file {query_file} does not contain valid pitch data.")
        return []

    similarities = []
    features_atb = {}
    features_rtb = {}
    features_ftb = {}

    i = 1

    for filename in os.listdir(dataset_features):
        if filename.endswith(".mid"):
            rank = i
            file_path = os.path.join(dataset_features, filename)
            features_atb[filename] = absolute_tone_based(file_path)
            features_rtb[filename] = relative_tone_based(file_path)
            features_ftb[filename] = first_tone_based(file_path)

            if features_atb[filename] is None or features_rtb[filename] is None or features_ftb[filename] is None:
                print(f"Skipping file {file_path} due to invalid pitch data.")
                continue

            atb_similarity = cosine_similarity_custom(query_atb, features_atb[filename])
            rtb_similarity = cosine_similarity_custom(query_rtb, features_rtb[filename])
            ftb_similarity = cosine_similarity_custom(query_ftb, features_ftb[filename])
            similarity = (atb_similarity * 5 + rtb_similarity * 47.5 + ftb_similarity * 47.5)/100
            similarities.append((rank, filename, similarity))

    similarities = sorted(similarities, key=lambda x: x[1], reverse=True)
    return similarities