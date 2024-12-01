import numpy as np
import matplotlib.pyplot as plt
from process_midi import process_midi

def absolute_tone_based(file_path):
    # Processing MIDI file
    processed_data = process_midi(file_path)

    if not processed_data:
        raise ValueError("Tidak ada data melodi yang dapat diproses.")

    # Converting normalized pitch to original midi pitch
    original_pitches = [int(round((note * 12) + 60)) for note, _ in processed_data]

    # Making a histogram of 128 notes
    histogram, _ = np.histogram(original_pitches, bins=128, range=(0, 127))

    return histogram


# Just for testing
def plot_histogram(histogram): 
    """
    Memvisualisasikan histogram nada MIDI.

    Args:
        histogram (np.ndarray): Histogram nada (128 bin, skala MIDI).
    """
    plt.bar(range(128), histogram, width=1.0, edgecolor='black')
    plt.title("Distribusi Nada MIDI (Absolute Tone Based)")
    plt.xlabel("Nada MIDI (0-127)")
    plt.ylabel("Frekuensi Kemunculan")
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    plt.show()
