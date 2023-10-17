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

    st.set_page_config(page_title="PDF Text Extractor")

    tab1, tab2 = st.tabs(["Text Extractor", "Translator"])

    with tab1:
        st.title("PDF Text Extractor")

        file = st.file_uploader(label="Upload your PDF file here.", type=['pdf'])

        language = st.selectbox(label="Please select the language you want to extract", options=["Chinese Simplified", "Chinese Traditional", "English"])

        fix = st.checkbox("Fix image orientation", value=True)

        extract_btn_clicked = st.button(label="Extract Texts")

        if file is not None:
            # Pass the file as BytesIO stream
            pdf_data = io.BytesIO(file.read())
            images = op.parse_file(pdf_data, fix)

            # Display images in a loop
            for i, img in enumerate(images):
                st.subheader(f"Page {i + 1}")
                col1, col2 = st.columns(2)
                col1.image(img, use_column_width=True)
                if str(i) in data:
                    col2.text_area("Text", data[str(i)], height=400)
                else:
                    col2.empty()
                if extract_btn_clicked:
                    text = op.extract_text_from_image(img, language=language)
                    col2.text_area("Text", text, height=400)
                    data[i] = text

            save_data(data)

    with tab2:
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