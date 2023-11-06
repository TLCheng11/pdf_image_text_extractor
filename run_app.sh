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

# Run the main.py script with Streamlit in viewer mode
streamlit run main.py --client.toolbarMode viewer --server.port 8601

# Deactivate the virtual environment
deactivate

# Exit the script
exit
