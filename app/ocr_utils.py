import pytesseract
from PIL import Image
import os

try:
    from pdf2image import convert_from_path
except ImportError:
    convert_from_path = None

# Path to tesseract.exe (safe for Windows, adjust if installed elsewhere)
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"


def extract_text_from_file(file_path: str) -> str:
    """
    Extract text from an image (JPG/PNG) or PDF file using Tesseract OCR.
    Supports multi-page PDFs.
    Returns extracted text as a string.
    """
    try:
        if not os.path.exists(file_path):
            return "Error: File does not exist."

        file_ext = os.path.splitext(file_path)[1].lower()

        # Handle images
        if file_ext in [".jpg", ".jpeg", ".png"]:
            image = Image.open(file_path)
            text = pytesseract.image_to_string(image)

        # Handle PDFs
        elif file_ext == ".pdf":
            if convert_from_path is None:
                return "Error: pdf2image is not installed. Run: pip install pdf2image"

            pages = convert_from_path(file_path, dpi=300)
            text_parts = []
            for page in pages:
                text_parts.append(pytesseract.image_to_string(page))
            text = "\n".join(text_parts)

        else:
            return f"Error: Unsupported file format {file_ext}. Only JPG, PNG, PDF are supported."

        # Clean up OCR output
        return text.strip()

    except Exception as e:
        return f"Error extracting text: {str(e)}"
