import os
import pytesseract
from dotenv import load_dotenv

load_dotenv()
tesseract_path = os.environ["TESSERACT_PATH"]

# Path to the Tesseract executable (update this if necessary)
pytesseract.pytesseract.tesseract_cmd = tesseract_path

languages = {
    "English": "eng",
    "Chinese Simplified": "chi_sim",
    "Chinese Traditional": "chi_tra",
}

def extract_text_from_image(image, language):
    # determine which language package to be used for OCR
    lang = "eng"
    if language in languages:
        lang = languages[language]

    try:
        # Use pytesseract to extract text from the image
        extracted_text = pytesseract.image_to_string(image, lang=lang)
        return extracted_text
    except Exception as e:
        print(f"An error occurred: {e}")
        return None


