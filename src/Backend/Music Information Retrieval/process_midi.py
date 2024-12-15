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

def process_midi(midi_file, window_size=40, sliding_step=8):

    melody_notes = []
    time_accumulator = 0

    tempo = 500000
    for track in midi_file.tracks:
        for msg in track:
            if msg.type == 'set_tempo':
                tempo = msg.tempo
                break

    ticks_per_beat = midi_file.ticks_per_beat

    for track in midi_file.tracks:
        for msg in track:
            time_accumulator += msg.time * tempo / ticks_per_beat / 1e6
            if not msg.is_meta and hasattr(msg, 'channel') and msg.channel == 0:
                if msg.type == 'note_on' and msg.velocity > 0:
                    melody_notes.append((msg.note, time_accumulator))

    if not melody_notes:
        raise ValueError("Tidak ada notasi yang ditemukan di Channel 0.")
    
    dev_notes_list = [x[0] for x in melody_notes]
    dev_notes_list_mean = sum(dev_notes_list) / len(dev_notes_list)
    dev_notes = math.sqrt(sum((x - dev_notes_list_mean) ** 2 for x in dev_notes_list) / len(dev_notes_list))

    process_midi_result = []
    for i in range(len(melody_notes)):
        converted_notes = (melody_notes[i][0] - dev_notes_list_mean) / dev_notes
        process_midi_result.append((converted_notes, melody_notes[i][1]))
        
    return process_midi_result, dev_notes_list_mean, dev_notes

def find_active_channels(file_path):
    midi_file = mido.MidiFile(file_path)
    active_channels = set()
    for track in midi_file.tracks:
        for msg in track:
            if not msg.is_meta and hasattr(msg, 'channel'):
                active_channels.add(msg.channel)
    return active_channels
