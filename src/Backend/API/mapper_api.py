import os
from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.responses import JSONResponse
from io import StringIO

MAPPER_FILE_PATH = os.path.join(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../Data/")), "mapper.txt")

app = FastAPI()

def validate_mapper_format(file_content: str):
    lines = file_content.strip().split("\n")
    
    if lines[0].strip() != "audio_file pic_name":
        raise ValueError("Invalid file format. The first line must be 'audio_file pic_name'.")
    
    for line in lines[1:]:
        columns = line.strip().split()
        if len(columns) != 2:
            raise ValueError(f"Invalid format in line: '{line}'. Each line must contain exactly two columns.")
        
        audio_file, pic_name = columns
        if not audio_file.endswith(".mid") or not (pic_name.endswith(".png") or pic_name.endswith(".jpg")):
            raise ValueError(f"Invalid file format in line: '{line}'. Audio file must end with '.mid' and image file must end with '.png' or '.jpg'.")
    
    return lines

@app.post("/upload-mapper/")
async def upload_mapper_file(file: UploadFile = File(...)):
    try:
        file_content = await file.read()
        file_content = file_content.decode("utf-8")  
        
        valid_lines = validate_mapper_format(file_content)

        with open(MAPPER_FILE_PATH, "w") as f:
            for line in valid_lines:
                f.write(line)
        
        return JSONResponse(content={"message": "Mapper file successfully uploaded and saved to 'mapper.txt'."})
    
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing the file: {str(e)}")

