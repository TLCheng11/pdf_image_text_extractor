# WordExtract (Demo)

Welcome to WordExtract (Demo), a robust SaaS platform designed to provide OCR (Optical Character Recognition) and multilingual translation services.

This is a Demo Vision using Tesseract for OCR and OpenAI API for text translation.

The official version github repository is private.

You can still visit here [wordextract.com](https://wordextract.com/) to try the offical application.

## Features

-   **OCR Functionality**: Extract text from images Tesseract.
-   **Multilingual Translation**: Translate extracted text into a wide range of languages with OpenAI API.

## Getting Started

To get a local copy up and running follow these simple steps.

### Prerequisites

-   Docker
-   Python 3.9+ (if don't have Docker)

### Installation

1.  Clone the repository

    ```sh
    git clone https://github.com/yourusername/wordextract.git
    ```

2.  Add the following api keys into a .env file

    OPENAI_API_KEY=your_api_key<br>
    LLM_MODEL=gpt-3.5-turbo<br>
    "TESSERACT_PATH"=your_tesseract_path<br>

3.  Start App

    1. Start Docker

        ```sh
        docker compose up
        ```

    2. Run the follow file (if no Docker)

        - run_app.bat (for window)
        - run_app.sh (for mac)

4.  Open app

    open app in [localhost:8601](http://localhost:8601)

## License

This project is licensed under the Apache License 2.0 - see the [LICENSE](LICENSE) file for details.
