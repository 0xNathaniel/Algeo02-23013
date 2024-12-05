import numpy as np
import matplotlib.pyplot as plt
from process_midi import process_midi
from process_midi import transpose_to_c
from process_midi import clamp

def absolute_tone_based(file_path):
    # Processing MIDI file
    processed_data, mean_pitch, std_pitch = process_midi(file_path)

    # Converting normalized pitch to original midi pitch
    original_pitches = [int(round((note * std_pitch) + mean_pitch)) for note, _ in processed_data]
    transpose = transpose_to_c(original_pitches[0])
    original_pitches = [note + transpose for note in original_pitches]
    original_pitches = [clamp(note) for note in original_pitches]
    temp_histogram, _ = np.histogram(original_pitches, bins=128, range=(0, 127))
    histogram = temp_histogram.tolist()

    return histogram

# Just for testing
# file_path = 'test1.mid'
# try:
#     hasil = absolute_tone_based(file_path)
#     print(hasil)    

# except Exception as e:
#     print(f"Error: {e}")
