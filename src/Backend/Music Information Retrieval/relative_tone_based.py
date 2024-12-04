import numpy as np
import mido
import matplotlib.pyplot as plt
from process_midi import process_midi

def relative_tone_based(file_path, window_size=40, sliding_step=8):
    processed_data, mean_pitch, std_pitch = process_midi(file_path)
    normalized_pitches = [int(round((note * std_pitch) + mean_pitch)) for note, _ in processed_data]
    temp_pitch_differences = np.diff(normalized_pitches)
    pitch_differences = temp_pitch_differences.tolist()
    return pitch_differences

# Menghasilkan array of "selisih nada berurutan"
# file_path = 'test1.mid'
# try:
#     hasil = relative_tone_based(file_path)
#     print(hasil)    

# except Exception as e:
#     print(f"Error: {e}")
