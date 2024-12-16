import numpy as np
import mido
import matplotlib.pyplot as plt
from process_midi import process_midi
from process_midi import transpose_to_c
from process_midi import clamp
from process_midi import normalize_histogram_cumulative

def first_tone_based(file_path, window_size=40, sliding_step=8):
    """
    Extract first tone-based features from a MIDI file.
    """
    try:
        # Process the MIDI file
        processed_data = process_midi(file_path)

        # Handle edge cases where std_pitch is zero

        # Normalize pitches

        # Compute differences from the first tone
        temp_normalized_pitches = np.array(processed_data)
        temp_pitch_differences = temp_normalized_pitches - temp_normalized_pitches[0]

        # Create histogram
        histogram, _ = np.histogram(temp_pitch_differences, bins=255, range=(-127, 127))

        # Convert to numpy array and return
        output = np.array(histogram)
        return output

    except ValueError as e:
        print(f"Error in first_tone_based for {file_path}: {e}")
        return None