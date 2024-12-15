import os

MAPPER_FILE = "src/Backend/Album Picture Finder/mapper.txt"

# Load mapper file into a dictionary
def load_mapper(mapper_file):
    print("Loading mapper...")
    
    mapper = {}
    try:
        with open(mapper_file, "r") as file:
            for line_number, line in enumerate(file, start=1):
                # Skip the header line
                if line_number == 1:
                    continue
                stripped_line = line.strip()
                if not stripped_line:  # Skip empty lines
                    print(f"Skipping empty line {line_number}")
                    continue
                try:
                    # Expecting `audio_file pic_name` structure
                    audio_file, pic_name = stripped_line.split()
                    mapper[pic_name] = audio_file
                except ValueError:
                    print(f"Skipping invalid line {line_number}: {stripped_line}")
    except FileNotFoundError:
        print(f"Mapper file not found: {mapper_file}")
        raise
    except Exception as e:
        print(f"Error reading mapper file: {e}")
        raise
    return mapper