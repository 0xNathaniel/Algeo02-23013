import mido
import math
import numpy as np

def transpose_to_c(note):
    transpose_amount = (60 - note) % 12
    return transpose_amount

def normalize_length(RTB1, RTB2, FTB1, FTB2):
    selisih = abs(len(RTB1) - len(RTB2))
    if (selisih != 0):
        if (len(RTB1) > len(RTB2)):
            for i in range (selisih):
                RTB1 = np.delete(RTB1, -1)
                FTB1 = np.delete(FTB1, -1)
        else:
            for i in range (selisih):
                RTB2 = np.delete(RTB2, -1)
                FTB2 = np.delete(FTB2, -1)
    return RTB1, RTB2, FTB1, FTB2

def clamp(note):
    if (note > 127):
        return 127
    elif (note < 0):
        return 0
    else:
        return note
    
def normalize_histogram_cumulative(histogram):
    cumulative_sum = np.cumsum(histogram[::-1])[::-1]
    normalized_histogram = np.zeros_like(histogram, dtype=float)
    
    for d in range(len(histogram)):
        if cumulative_sum[d] > 0:
            normalized_histogram[d] = histogram[d] / cumulative_sum[d]
    
    return normalized_histogram

import math

def process_midi(midi_file, window_size=40, sliding_step=8):
    dev_notes_list = [msg.note for msg in midi_file if msg.type == 'note_on' and msg.channel ==0]
    
    if len(dev_notes_list) == 0:
        print("No notes available for deviation calculation.")
        return []
    else:
        return dev_notes_list

def find_active_channels(file_path):
    midi_file = mido.MidiFile(file_path)
    active_channels = set()
    for track in midi_file.tracks:
        for msg in track:
            if not msg.is_meta and hasattr(msg, 'channel'):
                active_channels.add(msg.channel)
    return active_channels
