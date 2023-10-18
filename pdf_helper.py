import fitz  # PyMuPDF
from PIL import Image

def parse_file(file, fix=True):
    doc = fitz.open(stream=file, filetype="pdf")
    images = []

    for page_num in range(len(doc)):
        page = doc.load_page(page_num)
        image_list = page.get_pixmap(matrix=fitz.Matrix(300 / 72, 300 / 72))

        image = Image.frombytes("RGB", [image_list.width, image_list.height], image_list.samples)

        images.append(image)

    doc.close()
    return images