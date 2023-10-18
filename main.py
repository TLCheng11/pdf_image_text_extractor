import io
import json
import re
import os
import streamlit as st
from dotenv import load_dotenv
from collections import defaultdict

import ocr_processor as op
import image_helper as ih
import pdf_helper as pdf
import langchain_helper as lch

data = {}

def save_data():
    with open('prev_extracted_text.json', 'w') as file:
        json.dump(data, file)

@st.cache_data
def save_current_page_data(page, text):
    data[str(page)] = text
    with open('prev_extracted_text.json', 'w') as file:
        json.dump(data, file)

if __name__ == "__main__":
    # load saved data and setup globle variables
    load_dotenv()
    openai_key = os.getenv("OPENAI_API_KEY")

    with open('prev_extracted_text.json', 'r') as file:
        data = json.load(file)

    # config main ui setting
    st.set_page_config(
        page_title="PDF Text Extractor",
        page_icon="🧊",
        layout="wide",
    )

    tab1, tab2 = st.tabs(["Image and PDF Text Extractor", "Translator"])


    # tab for Image text extraction
    with tab1:
        st.title("Image Text Extractor")

        image_file = st.file_uploader(label="Upload your image here.", type=['jpg', 'jpeg', 'png', 'pdf'])

        img_language = st.selectbox(label="Please select the language you want to extract", key="language_option_2", options=["Chinese Simplified", "Chinese Traditional", "English"])

        # options for deskew image
        deskew_col1, deskew_col2, _ = st.columns((1, 1, 1))
        img_deskew = deskew_col1.checkbox("Fix image orientation", value=False)
        img_trun_90 = deskew_col2.checkbox("Turn image 90 degree", value=False)

        # options for adjusting image contrast and brightness
        adj_col1, adj_col2 = st.columns(2)
        img_contrast = adj_col1.slider("Adjust contrast ratio:", 0.0, 2.0, (1.0))
        img_brightness = adj_col2.slider("Adjust brightness ratio:", -100.0, +100.0, (0.0))

        # options for adjusting font thinkness and black and white image
        _ , bnw_checkbox_col2 = st.columns(2)
        img_bnw = bnw_checkbox_col2.checkbox("Turn image black and white (use this if text color is too light)", value=False)

        font_col1, bnw_col2 = st.columns(2)
        img_font = font_col1.slider("Adjust Font Weight:", 0, 5, (0))
        img_darkness = bnw_col2.slider("Adjust darkness:", 0, 255, (240))

        # columns for the btn to align right
        page_selection_col, _, btn_col = st.columns([1, 3, 1])
        img_extract_btn_clicked = btn_col.button(label="Extract Text from Image")


        if image_file is not None:
            if data["file_name"] != image_file.name:
                data = {"file_name": "", "current_page": 1}
                data["file_name"] = image_file.name
                save_data()

            images = []
            pdf_extension_pattern = r".+\.pdf$"
            if re.match(pdf_extension_pattern, image_file.name):
                pdf_data = io.BytesIO(image_file.read())
                images = pdf.parse_file(pdf_data)
            else:
                images.append(image_file)

            current_page = page_selection_col.selectbox("Page", [i + 1 for i in range(len(images))], index=data["current_page"] - 1)

            if re.match(pdf_extension_pattern, image_file.name):
                processed_img = ih.numpify_image(images[current_page - 1])
            else:
                processed_img = ih.decode_img(images[current_page - 1])

            if img_deskew:
                processed_img = ih.deskew(processed_img, turn_90=img_trun_90)
            if img_contrast != 1.0 or img_brightness != 0.0:
                processed_img = ih.adj_contrast(processed_img, img_contrast, img_brightness)
            if img_font != 0:
                processed_img = ih.thick_font(processed_img, size=img_font)
            if img_bnw:
                processed_img = ih.black_and_white(processed_img, darkness=img_darkness)
                    
            img_col1, img_col2 = st.columns(2)
            img_col1.image(processed_img, use_column_width=True)

            img_text_area = None

            if img_extract_btn_clicked:
                img_extracted_text = op.extract_text_from_image(processed_img, language=img_language)
                img_text_area = img_col2.text_area("Text", img_extracted_text, height=500)
                data[str(current_page)] = img_text_area
                save_data()

            elif str(current_page) in data:
                img_text_area = img_col2.text_area("Text", data[str(current_page)], height=500)

            save_current_page_data(current_page, img_text_area)

            # show translate box if openai api key present
            if openai_key:
                if img_text_area:
                    translate_col1, translate_col2 = img_col2.columns([3,1])
                    img_target_language = translate_col1.text_input(
                        label="Enter the language you want to translate into:",
                        max_chars=20,
                        value="English",
                        key="img_target_language"
                    )
                    placeholder = translate_col2.subheader("")
                    translate_text = translate_col2.button("Translate Text")


                    if translate_text and img_text_area:
                        loading = img_col2.empty()
                        loading.text("Translating...")
                        response, cb = lch.translate_text(img_target_language, img_text_area).values()
                        img_col2.write(response)
                        loading.empty()
            # else:
            #     img_col2.text("OpenAI API key is required for translating function.")



    # tab for translation
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
