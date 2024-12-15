import os
import fluidsynth
from pydub import AudioSegment

def midi_to_mp3_fixed_paths(midi_file_path):
    # Hardcoded paths
    soundfont_path = "../../Frontend/public/Audio Sample/general_audio_sample.sf2"
    output_directory = "../../Frontend/public/Convert Result"

    # Ensure output directory exists
    os.makedirs(output_directory, exist_ok=True)

    # Extract filename without extension
    filename_without_ext = os.path.splitext(os.path.basename(midi_file_path))[0]

    # Define output paths
    output_mp3_path = os.path.join(output_directory, f"{filename_without_ext}.mp3")
    temp_wav_path = os.path.join(output_directory, f"{filename_without_ext}.wav")

    try:
        # Initialize FluidSynth and load the SoundFont
        fs = fluidsynth.Synth()
        fs.start(driver="file", filename=temp_wav_path)  # Output to WAV file
        fs.sfload(soundfont_path)
        fs.midi_file_play(midi_file_path)  # Play the MIDI file
        fs.delete()

        # Convert WAV to MP3 using pydub
        sound = AudioSegment.from_file(temp_wav_path, format="wav")
        sound.export(output_mp3_path, format="mp3")

        print(f"MP3 file created: {output_mp3_path}")

    except Exception as e:
        print(f"Error converting MIDI to MP3: {e}")

    finally:
        # Clean up the temporary WAV file
        if os.path.exists(temp_wav_path):
            os.remove(temp_wav_path)


def convert_all_mid_to_mp3(input_directory):
    # Walk through the directory
    for root, _, files in os.walk(input_directory):
        for file in files:
            if file.endswith(".mid") or file.endswith(".midi"):
                midi_file_path = os.path.join(root, file)
                print(f"Processing: {midi_file_path}")
                midi_to_mp3_fixed_paths(midi_file_path)