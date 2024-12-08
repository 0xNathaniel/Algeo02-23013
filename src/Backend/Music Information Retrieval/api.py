from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.responses import JSONResponse
import os
import numpy as np
from mido import MidiFile
from find_most_similar import find_most_similar

# FastAPI app
app = FastAPI()

# Parameters
MIDI_DIRECTORY = "src/Backend/Music Information Retrieval/Data" # MIDI Files directory

# API
@app.post("/music/")
async def find_similar_midi(query_midi: UploadFile = File(...)):
    try:
        query_audio = MidiFile(query_midi.file)
        similarities = find_most_similar(query_audio, MIDI_DIRECTORY)
        results = [{"rank": rank, "midi_name": midi_name, "similarity": similarity} for rank, midi_name, similarity in similarities]
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing the query MIDI file: {str(e)}")
