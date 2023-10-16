import io
import streamlit as st
import ocr_processor as op
import image_helper as ih

file = st.file_uploader(label="Upload your PDF file here.", type=['pdf'])

if file is not None:
    # Pass the file as BytesIO stream
    pdf_data = io.BytesIO(file.read())
    images = op.parse_file(pdf_data)

    # Display images in a loop
    for i, img in enumerate(images):
        st.image(img, caption=f"Page {i + 1}")