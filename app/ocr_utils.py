def extract_text_from_file(file_path: str) -> str:
    """
    Extract text from an image (JPG/PNG) or PDF file.
    Uses lazy imports to save memory on Render.
    """
    try:
        import os
        import pytesseract
        from PIL import Image

        try:
            from pdf2image import convert_from_path
        except ImportError:
            convert_from_path = None

        # For Render/Linux, tesseract is usually installed in PATH
        # Comment this line out if Render has tesseract preinstalled
        # pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

        file_ext = os.path.splitext(file_path)[1].lower()

        if file_ext in [".jpg", ".jpeg", ".png"]:
            # Handle image files
            image = Image.open(file_path)
            text = pytesseract.image_to_string(image)

        elif file_ext == ".pdf":
            if convert_from_path is None:
                return "pdf2image is not installed. Run: pip install pdf2image"

            # Convert PDF pages to images
            pages = convert_from_path(file_path)
            text = ""
            for page in pages:
                text += pytesseract.image_to_string(page) + "\n"

        else:
            return f"Unsupported file format: {file_ext}"

        return text.strip()

    except Exception as e:
        return f"Error extracting text: {str(e)}"
