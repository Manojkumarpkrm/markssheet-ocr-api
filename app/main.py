from fastapi import FastAPI, UploadFile, File, HTTPException
import shutil
import os

from app.ocr_utils import extract_text_from_file
from app.openai_utils import parse_text_to_json

app = FastAPI(
    title="Marksheet Extraction API",
    version="1.0.0",
    description="API to extract raw text from marksheets using OCR and parse it into structured JSON with OpenAI."
)

UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)


@app.get("/")
def home():
    """
    Health check endpoint.
    """
    return {"message": "Welcome to Marksheet OCR API 🚀"}


@app.post("/extract-text/")
async def extract_text(file: UploadFile = File(...)):
    """
    Upload an image/PDF → Extract raw text using OCR → Return text.
    """
    try:
        file_path = os.path.join(UPLOAD_DIR, file.filename)
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        text = extract_text_from_file(file_path)

        if not text or text.startswith("Error"):
            raise HTTPException(status_code=500, detail=f"OCR failed: {text}")

        return {"filename": file.filename, "extracted_text": text}

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Extraction error: {str(e)}")


@app.post("/parse-json/")
async def parse_marksheet(file: UploadFile = File(...)):
    """
    Upload an image/PDF → Extract text using OCR → Convert into structured JSON.
    """
    try:
        file_path = os.path.join(UPLOAD_DIR, file.filename)
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        # Step 1: OCR
        text = extract_text_from_file(file_path)
        if not text or text.startswith("Error"):
            raise HTTPException(status_code=500, detail=f"OCR failed: {text}")

        # Step 2: JSON Parsing
        parsed = parse_text_to_json(text)
        if "error" in parsed:
            raise HTTPException(status_code=500, detail="OpenAI parsing failed")

        return {"filename": file.filename, "parsed_data": parsed}

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Parsing error: {str(e)}")
