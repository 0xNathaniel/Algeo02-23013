import numpy as np
import mido
import matplotlib.pyplot as plt
from process_midi import process_midi
from process_midi import transpose_to_c
from process_midi import clamp
from process_midi import normalize_histogram_cumulative
# from process_midi import vectorize

def relative_tone_based(file_path, window_size=40, sliding_step=8):
    """
    Extract relative tone-based features from a MIDI file.
    """
    try:
        # Process the MIDI file
        processed_data = process_midi(file_path)

        # Handle edge cases where std_pitch is zero

        # Normalize pitches

        # Compute pitch differences
        temp_pitch_differences = np.diff(processed_data)

        # Create histogram
        histogram, _ = np.histogram(temp_pitch_differences, bins=255, range=(-127, 127))

        # Convert to numpy array and return
        output = np.array(histogram)
        return output

    except ValueError as e:
        print(f"Error in relative_tone_based for {file_path}: {e}")
        return None
