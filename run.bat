@echo off
REM Activate conda environment first if needed:
REM conda activate aisci
set FLASK_APP=app:create_app
set FLASK_ENV=development
python app.py
