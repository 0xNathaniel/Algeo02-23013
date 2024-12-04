import mido
import math
import numpy as np

def process_midi(file_path, window_size=40, sliding_step=8):
    midi_file = mido.MidiFile(file_path)
    melody_notes = []
    time_accumulator = 0  # Time Accumulation

    # Getting tempo from MIDI (default 120 BPM = 500,000 ms per beat)
    tempo = 500000  # Default tempo
    for track in midi_file.tracks:
        for msg in track:
            if msg.type == 'set_tempo':
                tempo = msg.tempo
                break

    ticks_per_beat = midi_file.ticks_per_beat

    # Appending notes and time to melody_notes
    for track in midi_file.tracks:
        for msg in track:
            # Converting time to seconds based on tempo
            time_accumulator += msg.time * tempo / ticks_per_beat / 1e6
            if not msg.is_meta and hasattr(msg, 'channel') and msg.channel == 0:
                if msg.type == 'note_on' and msg.velocity > 0:
                    # Debug log : print(f"Adding Note: {msg.note}, Time: {time_accumulator}")
                    melody_notes.append((msg.note, time_accumulator))

    # Error handling if no notes found in Channel 0
    if not melody_notes:
        raise ValueError("Tidak ada notasi yang ditemukan di Channel 0.")
    
    dev_notes_list = [x[0] for x in melody_notes]
    # Getting mean of pitch
    dev_notes_list_mean = sum(dev_notes_list) / len(dev_notes_list)
    # Getting standard deviation of pitch
    dev_notes = math.sqrt(sum((x - dev_notes_list_mean) ** 2 for x in dev_notes_list) / len(dev_notes_list))

    # Normalizing pitch and appending to process_midi_result
    process_midi_result = []
    for i in range (len(melody_notes)):
        converted_notes = (melody_notes[i][0] - dev_notes_list_mean) / dev_notes
        process_midi_result.append((converted_notes, melody_notes[i][1]))
        
    return process_midi_result


def find_active_channels(file_path):
    midi_file = mido.MidiFile(file_path)
    active_channels = set()
    for track in midi_file.tracks:
        for msg in track:
            if not msg.is_meta and hasattr(msg, 'channel'):
                active_channels.add(msg.channel)
    return active_channels
