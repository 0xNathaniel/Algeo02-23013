import numpy as np
import mido
import matplotlib.pyplot as plt
from process_midi import process_midi
from process_midi import transpose_to_c
from process_midi import clamp
from process_midi import normalize_histogram_cumulative
# from process_midi import vectorize

def relative_tone_based(file_path, window_size=40, sliding_step=8):
    processed_data, mean_pitch, std_pitch = process_midi(file_path)
    normalized_pitches = [int(round((note * std_pitch) + mean_pitch)) for note, _ in processed_data]
    temp_pitch_differences = np.diff(normalized_pitches)
    histogram, _ = np.histogram(temp_pitch_differences, bins=255, range=(-127, 127))
    output = np.array(histogram)
    return output