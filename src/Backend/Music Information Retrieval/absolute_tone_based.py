import numpy as np
import matplotlib.pyplot as plt
from process_midi import process_midi

def absolute_tone_based(file_path):
    # Processing MIDI file
    processed_data, mean_pitch, std_pitch = process_midi(file_path)

    # Converting normalized pitch to original midi pitch
    original_pitches = [int(round((note * std_pitch) + mean_pitch)) for note, _ in processed_data]

    # Making a histogram of 128 notes
    temp_histogram, _ = np.histogram(original_pitches, bins=128, range=(0, 127))
    histogram = temp_histogram.tolist()

    return histogram

# Just for testing
# def plot_histogram(histogram): 
#     plt.bar(range(128), histogram, width=1.0, edgecolor='black')
#     plt.title("Distribusi Nada MIDI (Absolute Tone Based)")
#     plt.xlabel("Nada MIDI (0-127)")
#     plt.ylabel("Frekuensi Kemunculan")
#     plt.grid(axis='y', linestyle='--', alpha=0.7)
#     plt.show()
