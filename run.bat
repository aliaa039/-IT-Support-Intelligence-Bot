@echo off
REM Run IT Support Bot (use venv's Python so streamlit is found)
if exist venv\Scripts\activate.bat (
    call venv\Scripts\activate.bat
)
python -m streamlit run app.py %*
