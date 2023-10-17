@echo off

rem Check if the virtual environment exists
if not exist venv (
    echo Virtual environment 'venv' does not exist. Creating...
    python -m venv venv
)

rem Activate the virtual environment
call venv\Scripts\activate

rem Install packages from requirements.txt
pip install -r requirements.txt

rem Run the main.py script
streamlit run main.py --client.toolbarMode viewer

rem Close the Command Prompt window after completion
exit

