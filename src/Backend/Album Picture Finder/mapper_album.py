import os

MAPPER_FILE = "src/Backend/Album Picture Finder/mapper.txt"

def load_mapper_album(mapper_file):
    print("Loading mapper...")

    mapper = {}
    try:
        with open(mapper_file, "r") as file:
            for line_number, line in enumerate(file, start=1):
                if line_number == 1:
                    continue
                stripped_line = line.strip()
                if not stripped_line:  # Skip empty lines
                    print(f"Skipping empty line {line_number}")
                    continue
                try:
                    audio_file, audio_name, pic_name = stripped_line.split()
                    mapper[pic_name] = {
                        "audio_file": audio_file,
                        "audio_name": audio_name
                    }
                except ValueError:
                    print(f"Skipping invalid line {line_number}: {stripped_line}")
    except FileNotFoundError:
        print(f"Mapper file not found: {mapper_file}")
        raise
    except Exception as e:
        print(f"Error reading mapper file: {e}")
        raise

    return mapper

if __name__ == "__main__":
    mapper = load_mapper(MAPPER_FILE)
    for pic_name, info in mapper.items():
        print(f"Picture: {pic_name}, Audio File: {info['audio_file']}, Audio Name: {info['audio_name']}")
