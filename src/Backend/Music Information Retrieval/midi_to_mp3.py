import os
import pyfluidsynth
from pydub import AudioSegment

def midi_to_mp3_fixed_paths(midi_file_path):
    """
    Converts a MIDI file to MP3 format using pyfluidsynth and stores it in the specified output directory.
    """
    # Hardcoded paths
    soundfont_path = "../../Frontend/public/Audio Sample/general_audio_sample.sf2"
    output_directory = "../../Frontend/public/ConvertMP3"

    # Ensure output directory exists
    os.makedirs(output_directory, exist_ok=True)

    # Extract filename without extension
    filename_without_ext = os.path.splitext(os.path.basename(midi_file_path))[0]

    # Define output paths
    output_mp3_path = os.path.join(output_directory, f"{filename_without_ext}.mp3")
    temp_wav_path = os.path.join(output_directory, f"{filename_without_ext}.wav")

    try:
        # Check if SoundFont exists
        if not os.path.exists(soundfont_path):
            print(f"SoundFont file not found: {soundfont_path}")
            return

        print(f"Converting MIDI: {midi_file_path}")

        # Initialize FluidSynth
        fs = pyfluidsynth.Synth()
        fs.start(driver="file", filename=temp_wav_path)
        sfid = fs.sfload(soundfont_path)  # Load the SoundFont
        fs.program_select(0, sfid, 0, 0)  # Assign SoundFont to channel 0

        # Play MIDI file
        fs.midi_file_play(midi_file_path)
        fs.delete()  # Clean up the synthesizer

        # Convert WAV to MP3
        print(f"Converting WAV to MP3: {temp_wav_path}")
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
    """
    Walks through the input directory and processes all .mid and .midi files.
    """
    print(f"Scanning directory: {input_directory}")
    if not os.path.exists(input_directory):
        print(f"Input directory not found: {input_directory}")
        return

    # Walk through the directory
    for filename in os.listdir(input_directory):
        file_path = os.path.join(input_directory, filename)
        print(f"Found file: {file_path}")
        if filename.endswith(".mid") or filename.endswith(".midi"):
            print(f"Processing MIDI file: {file_path}")
            midi_to_mp3_fixed_paths(file_path)
