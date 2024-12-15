import os
import zipfile
from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.responses import JSONResponse
import shutil

EXTRACTION_DIR = os.path.join(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../Data/Dataset")))

app = FastAPI()


if not os.path.exists(EXTRACTION_DIR):
    os.makedirs(EXTRACTION_DIR)

def extract_zip_file(zip_file_path: str, extraction_dir: str):
    try:
        with zipfile.ZipFile(zip_file_path, 'r') as zip_ref:
            zip_ref.testzip()  
            zip_ref.extractall(extraction_dir)
            return zip_ref.namelist()
    except zipfile.BadZipFile:
        raise ValueError("The uploaded file is not a valid zip file.")
    except Exception as e:
        raise ValueError(f"Error extracting zip file: {str(e)}")

def clear_dataset_directory(extraction_dir: str):
    existing_files = os.listdir(extraction_dir)
    
    if len(existing_files) >= 1:
        for file in existing_files:
            file_path = os.path.join(extraction_dir, file)
            if os.path.isdir(file_path):
                shutil.rmtree(file_path) 
            else:
                os.remove(file_path)

@app.post("/upload-zip/")
async def upload_zip_file(file: UploadFile = File(...)):
    try:
        if not file.filename.endswith(".zip"):
            raise HTTPException(status_code=400, detail="Invalid file format. Only .zip files are allowed.")

        clear_dataset_directory(EXTRACTION_DIR)

        temp_zip_path = os.path.join(EXTRACTION_DIR, file.filename)

        with open(temp_zip_path, "wb") as temp_file:
            shutil.copyfileobj(file.file, temp_file)

        extracted_files = extract_zip_file(temp_zip_path, EXTRACTION_DIR)

        os.remove(temp_zip_path)

        return JSONResponse(content={"message": "Zip file successfully uploaded and extracted.", "extracted_files": extracted_files})
    
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing the zip file: {str(e)}")
