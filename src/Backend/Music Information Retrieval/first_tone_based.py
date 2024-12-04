import numpy as np
import mido
import matplotlib.pyplot as plt
from process_midi import process_midi

def first_tone_based(file_path, window_size=40, sliding_step=8):
    processed_data, mean_pitch, std_pitch = process_midi(file_path)
    normalized_pitches = [int(round((note * std_pitch) + mean_pitch)) for note, _ in processed_data]
    temp_normalized_pitches = np.array(normalized_pitches)
    temp_pitch_differences =  temp_normalized_pitches - temp_normalized_pitches[0]
    pitch_differences = temp_pitch_differences.tolist()
    return pitch_differences