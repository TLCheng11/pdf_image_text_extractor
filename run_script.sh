#!/bin/bash

# Check if the virtual environment directory exists
if [ ! -d "venv" ]; then
    echo "Virtual environment 'venv' does not exist. Creating..."
    python3 -m venv venv
fi

# Activate the virtual environment
source venv/bin/activate

# Install packages from requirements.txt
pip install -r requirements.txt

# Create an empty JSON object and overwrite the prev_extracted_text.json file
echo '{"file_name": "", "current_page": 1}' > prev_extracted_text.json

# Run the main.py script with Streamlit in viewer mode
streamlit run main.py --client.toolbarMode viewer

# Deactivate the virtual environment
deactivate

# Exit the script
exit
