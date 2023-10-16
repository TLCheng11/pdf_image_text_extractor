import fitz  # PyMuPDF
import pytesseract
import image_helper as ih
from PIL import Image

# Path to the Tesseract executable (update this if necessary)
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

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

def parse_file(file):
    doc = fitz.open(stream=file, filetype="pdf")
    images = []

    for page_num in range(len(doc)):
        page = doc.load_page(page_num)
        image_list = page.get_pixmap(matrix=fitz.Matrix(300 / 72, 300 / 72))

        image = Image.frombytes("RGB", [image_list.width, image_list.height], image_list.samples)
        
        fixed_image = ih.deskew(image)

        images.append(fixed_image)

    doc.close()
    return images

def ocr_image(image):
    extracted_text = extract_text_from_image(fixed_image)
    
    # if extracted_text:
    #     print(f"Extracted text from page {page_num + 1}:\n{extracted_text}\n")
    # else:
    #     print(f"Text extraction failed for page {page_num + 1}.\n")

    return extracted_text
