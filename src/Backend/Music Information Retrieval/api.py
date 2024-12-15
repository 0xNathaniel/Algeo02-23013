import os
import io
from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.responses import JSONResponse
from mido import MidiFile
from find_most_similar import find_most_similar
from fastapi.middleware.cors import CORSMiddleware
from mapper_music import load_mapper

# FastAPI app
app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Parameters
MIDI_DIRECTORY = "../../Frontend/public/Data/Music Dataset"
MAPPER_FILE = "../../Data/mapper.txt"

# Preload dataset MIDI files at startup
dataset_midis = []

mapper = load_mapper(MAPPER_FILE)

def load_dataset_midis():
    global dataset_midis
    dataset_midis = []
    for filename in os.listdir(MIDI_DIRECTORY):
        if filename.endswith(".mid") or filename.endswith(".midi"):
            file_path = os.path.join(MIDI_DIRECTORY, filename)
            try:
                midi_obj = MidiFile(file_path)
                dataset_midis.append((filename, midi_obj))
            except Exception as e:
                print(f"Skipping {filename}: {e}")

# Load MIDI files at startup
load_dataset_midis()

@app.post("/music/")
async def find_similar_midi(query_midi: UploadFile = File(...)):
    try:
        # Validate file extension
        if not (query_midi.filename.endswith(".mid") or query_midi.filename.endswith(".midi")):
            raise HTTPException(status_code=400, detail="Invalid file type. Only .mid or .midi files are allowed.")
        
        # Read uploaded file as bytes
        query_midi_bytes = await query_midi.read()
        
        # Wrap the bytes in a BytesIO object
        query_midi_filelike = io.BytesIO(query_midi_bytes)

        query_midi_obj = MidiFile(file=query_midi_filelike)
        
        # Call the modified find_most_similar function
        similarities = find_most_similar(query_midi_obj, dataset_midis)
        results = []
        for rank, audio_file, similarity in similarities:
            mapper_entry = mapper.get(audio_file, {})
            audio_name = mapper_entry.get("audio_name", "Unknown")
            pic_name = mapper_entry.get("pic_name", "Unknown")
            results.append({
                "rank": rank,
                "pic_name": pic_name,
                "audio_file": audio_file,
                "audio_name": audio_name,
                "similarities": similarity
            })
        
        return JSONResponse(content={"similar_audio_files": results})
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing the query MIDI file: {str(e)}")
