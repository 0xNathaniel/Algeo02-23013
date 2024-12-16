import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

from process_midi import process_midi
from process_midi import normalize_length
from absolute_tone_based import absolute_tone_based
from relative_tone_based import relative_tone_based
from first_tone_based import first_tone_based
from cosine_similarity import cosine_similarity_custom

def find_most_similar(query_file, dataset_midis):
    query_atb = process_midi(query_file)
    query_rtb = process_midi(query_file)
    query_ftb = process_midi(query_file)
    
    query_atb = absolute_tone_based(query_file)
    query_rtb = relative_tone_based(query_file)
    query_ftb = first_tone_based(query_file)
    
    if query_atb is None or query_rtb is None or query_ftb is None:
        print(f"Query file does not contain valid pitch data.")
        return []

    similarities = []
    
    for filename, midi_obj in dataset_midis:
            
        features_atb = absolute_tone_based(midi_obj)
        features_rtb = relative_tone_based(midi_obj)
        features_ftb = first_tone_based(midi_obj)

        if (features_atb is None or len(features_atb) == 0 or
            features_rtb is None or len(features_rtb) == 0 or
            features_ftb is None or len(features_ftb) == 0):
                print(f"Skipping file {filename} due to invalid pitch data.")
                continue

        atb_similarity = cosine_similarity_custom(query_atb, features_atb)
        rtb_similarity = cosine_similarity_custom(query_rtb, features_rtb)
        ftb_similarity = cosine_similarity_custom(query_ftb, features_ftb)
        similarity = (atb_similarity * 5 + rtb_similarity * 50 + ftb_similarity * 45) / 100
        similarity_percentage = f"{similarity * 100:.2f}"
        similarities.append((filename, similarity_percentage))
        
    similarities = sorted(similarities, key=lambda x: float(x[1].rstrip('%')), reverse=True)
    ranked_similarities = [(rank + 1, filename, similarity) for rank, (filename, similarity) in enumerate(similarities)]
    ranked_similarities_capped = ranked_similarities[:40]
    
    return ranked_similarities_capped