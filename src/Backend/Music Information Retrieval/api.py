from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.responses import JSONResponse
from mido import MidiFile
from find_most_similar import find_most_similar
import os
import io

# FastAPI app
app = FastAPI()

# Parameters
MIDI_DIRECTORY = "../../Data/Dataset"

# Preload dataset MIDI files at startup
dataset_midis = []

@app.on_event("startup")
async def load_dataset_midis():
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
        
        # Load the BytesIO object into MidiFile
        query_midi_obj = MidiFile(file=query_midi_filelike)
        
        # Call the modified find_most_similar function
        similarities = find_most_similar(query_midi_obj, dataset_midis)
        results = [{"rank": rank, "midi_name": midi_name, "similarity": similarity} for rank, midi_name, similarity in similarities]
        return JSONResponse(content={"similar_audio_files": results})
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing the query MIDI file: {str(e)}")
