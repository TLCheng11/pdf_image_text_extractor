import io
import json
import os
import streamlit as st
from dotenv import load_dotenv
from collections import defaultdict

import ocr_processor as op
import image_helper as ih
import langchain_helper as lch

def save_data(data):
    with open('prev_extracted_text.json', 'w') as file:
        json.dump(data, file)

if __name__ == "__main__":
    load_dotenv()
    openai_key = os.getenv("OPENAI_API_KEY")

    data = {}
    with open('prev_extracted_text.json', 'r') as file:
        data = json.load(file)

    st.set_page_config(
        page_title="PDF Text Extractor",
        page_icon="🧊",
        layout="wide",
    )

    tab1, tab2, tab3 = st.tabs(["PDF Text Extractor", "Image Text Extractor", "Translator"])

    # tab for PDF text extraction
    with tab1:
        st.title("PDF Text Extractor")

        pdf_file = st.file_uploader(label="Upload your PDF file here.", type=['pdf'])

        pdf_language = st.selectbox(label="Please select the language you want to extract", key="language_option_1", options=["Chinese Simplified", "Chinese Traditional", "English"])

        fix = st.checkbox("Fix image orientation", value=True)

        pdf_extract_btn_clicked = st.button(label="Extract Text from PDF")

        if pdf_file is not None:
            # Pass the file as BytesIO stream
            pdf_data = io.BytesIO(pdf_file.read())
            images = op.parse_file(pdf_data, fix)

            # Display images in a loop
            for i, img in enumerate(images):
                st.subheader(f"Page {i + 1}")
                image_np = ih.numpify_image(img)

                pdf_col1, pdf_col2 = st.columns(2)
                pdf_col1.image(img, use_column_width=True)
                if str(i) in data:
                    pdf_col2.text_area("Text", data[str(i)], height=500)
                else:
                    pdf_col2.empty()
                if pdf_extract_btn_clicked:
                    text = op.extract_text_from_image(image_np, language=pdf_language)
                    pdf_col2.text_area("Text", text, height=500)
                    data[i] = text

            save_data(data)

    # tab for Image text extraction
    with tab2:
        st.title("Image Text Extractor")

        image_file = st.file_uploader(label="Upload your image here.", type=['jpg', 'jpeg', 'png'])

        img_language = st.selectbox(label="Please select the language you want to extract", key="language_option_2", options=["Chinese Simplified", "Chinese Traditional", "English"])

        # options for deskew image
        deskew_col1, deskew_col2, _ = st.columns((1, 1, 1))
        img_deskew = deskew_col1.checkbox("Fix image orientation", value=False)
        img_trun_90 = deskew_col2.checkbox("Turn image 90 degree", value=False)

        # options for adjusting image contrast and brightness
        adj_col1, adj_col2 = st.columns(2)
        img_contrast = adj_col1.slider("Adjust contrast ratio:", 0.0, 2.0, (1.0))
        img_brightness = adj_col2.slider("Adjust brightness ratio:", -100.0, +100.0, (0.0))

        # options for adjusting font thinkness
        font_col1, _ = st.columns(2)
        img_font = font_col1.slider("Adjust Font Weight:", 0, 5, (0))

        img_extract_btn_clicked = st.button(label="Extract Text from Image")

        if image_file is not None:
            processed_img = ih.decode_img(image_file)
            if img_deskew:
                processed_img = ih.deskew(processed_img, turn_90=img_trun_90)
            if img_contrast != 1.0 or img_brightness != 0.0:
                processed_img = ih.adj_contrast(processed_img, img_contrast, img_brightness)
            if img_font != 0:
                processed_img = ih.thick_font(processed_img, size=img_font)
                    
            img_col1, img_col2 = st.columns(2)
            img_col1.image(processed_img, use_column_width=True)

            if img_extract_btn_clicked:
                text = op.extract_text_from_image(processed_img, language=img_language)
                img_col2.text_area("Text", text, height=500)

    # tab for translation
    with tab3:
        st.title("GPT-translator")

        if not openai_key:
            st.text("OpenAI API key is required for this function.")
        else:
            target_language = st.text_input(
                label="Enter the language you want to translate into:",
                max_chars=20,
                value="English",
            )

            source_text = st.text_area(
                label="Enter source text here:",
                max_chars=2000,
                placeholder="Maxmium input charaters is 2000.",
                height=300,
            )

            clicked = st.button(label="Translate")
            loading = st.empty()
            results = st.empty()

            if clicked:
                if source_text:
                    loading.text("Translating...")
                    response, cb = lch.translate_text(target_language, source_text).values()
                    results.write(response)
                    loading.empty()
                    st.divider()
                    st.caption(f"Request cost data:")
                    st.caption(f"input_char_count: {len(source_text)}")
                    st.caption(f"input_token_count: {cb.prompt_tokens}")
                    st.caption(f"output_char_count: {len(response)}")
                    st.caption(f"output_token_count: {cb.completion_tokens}")
                    st.caption(f"total_cost: ${cb.total_cost}")
                else:
                    loading.text("Input cannot be empty!")