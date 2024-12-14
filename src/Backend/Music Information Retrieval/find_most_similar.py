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
    """
    Finds the most similar MIDI files from a list of preloaded MIDI objects.

    Args:
        query_file (mido.MidiFile): Query MIDI file object.
        dataset_midis (list of tuples): List of tuples (filename, mido.MidiFile).

    Returns:
        list: Ranked similarities with (rank, filename, similarity).
    """
    query_atb, mean, std = process_midi(query_file)
    query_rtb, mean, std = process_midi(query_file)
    query_ftb, mean, std = process_midi(query_file)

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

        if features_atb is None or features_rtb is None or features_ftb is None:
            print(f"Skipping file {filename} due to invalid pitch data.")
            continue

        atb_similarity = cosine_similarity_custom(query_atb, features_atb)
        rtb_similarity = cosine_similarity_custom(query_rtb, features_rtb)
        ftb_similarity = cosine_similarity_custom(query_ftb, features_ftb)
        similarity = (atb_similarity * 5 + rtb_similarity * 47.5 + ftb_similarity * 47.5) / 100
        similarities.append((filename, similarity))

    similarities = sorted(similarities, key=lambda x: x[1], reverse=True)
    ranked_similarities = [(rank + 1, filename, similarity) for rank, (filename, similarity) in enumerate(similarities)]
    
    return ranked_similarities