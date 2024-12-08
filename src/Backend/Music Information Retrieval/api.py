from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.responses import JSONResponse
from mido import MidiFile
from find_most_similar import find_most_similar

# FastAPI app
app = FastAPI()

# Parameters
MIDI_DIRECTORY = "C:\\Users\\omgit\\repos\\Tugas Besar Semester 3\\Algeo02-23013\\src\\Data\\Dataset"  # MIDI Files directory

# API
@app.post("/music/")
async def find_similar_midi(query_midi: UploadFile = File(...)):
    try:
        # Use the file-like object directly
        temp_filename = "temp.mid"
        with open(temp_filename, "wb") as temp_file:
            temp_file.write(query_midi.file.read())
            # This should work with a file-like object
        similarities = find_most_similar(temp_filename, MIDI_DIRECTORY)
        results = [{"rank": rank, "midi_name": midi_name, "similarity": similarity} for rank, midi_name, similarity in similarities]
        return JSONResponse(content={"similar_audio_files": results})
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing the query MIDI file: {str(e)}")
