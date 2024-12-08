import numpy as np
import matplotlib.pyplot as plt
from process_midi import process_midi
from process_midi import transpose_to_c
from process_midi import clamp
from process_midi import normalize_histogram_cumulative
# from process_midi import vectorize

def absolute_tone_based(file_path):
    # Processing MIDI file
    processed_data, mean_pitch, std_pitch = process_midi(file_path)

    # Converting normalized pitch to original midi pitch
    original_pitches = [int(round((note * std_pitch) + mean_pitch)) for note, _ in processed_data]
    transpose = transpose_to_c(original_pitches[0])
    original_pitches = [note + transpose for note in original_pitches]
    original_pitches = [clamp(note) for note in original_pitches]
    temp_histogram, _ = np.histogram(original_pitches, bins=128, range=(0, 127))
    normalized_histogram = normalize_histogram_cumulative(temp_histogram)
    output = np.array(normalized_histogram)

    return output
