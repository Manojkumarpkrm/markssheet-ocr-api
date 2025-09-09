import easyocr
import os

# Initialize EasyOCR reader (English for now, can add more languages like ['en', 'hi'])
reader = easyocr.Reader(['en'], gpu=False)

def extract_text_from_file(file_path: str) -> str:
    """
    Extract text from an image (JPG/PNG) or PDF file using EasyOCR.
    """
    try:
        file_ext = os.path.splitext(file_path)[1].lower()

        if file_ext in [".jpg", ".jpeg", ".png"]:
            # Handle image files
            result = reader.readtext(file_path, detail=0)
            text = "\n".join(result)

        elif file_ext == ".pdf":
            from pdf2image import convert_from_path
            pages = convert_from_path(file_path)
            text = ""
            for page in pages:
                result = reader.readtext(page, detail=0)
                text += "\n".join(result) + "\n"

        else:
            return f"Unsupported file format: {file_ext}"

        return text.strip()

    except Exception as e:
        return f"Error extracting text: {str(e)}"

