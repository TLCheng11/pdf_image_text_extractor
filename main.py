import io
import streamlit as st
import ocr_processor as op
import image_helper as ih

if __name__ == "__main__":
    st.title("PDF text extractor demo")

    file = st.file_uploader(label="Upload your PDF file here.", type=['pdf'])

    language = st.selectbox(label="Please select the language you want to extract", options=["Chinese Simplified", "Chinese Traditional", "English"])

    if file is not None:
        # Pass the file as BytesIO stream
        pdf_data = io.BytesIO(file.read())
        images = op.parse_file(pdf_data)

        # Display images in a loop
        for i, img in enumerate(images):
            st.subheader(f"Page {i + 1}")
            col1, col2 = st.columns(2)
            col1.image(img, use_column_width=True)
            text = op.extract_text_from_image(img, language=language)
            col2.text(text)