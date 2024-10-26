@echo off
REM Step 1: Create a virtual environment
python -m venv venv

REM Step 2: Activate the virtual environment
call venv\Scripts\activate

REM Step 3: Install all dependencies from requirements.txt
pip install -r requirements.txt

REM Step 4: Run pytest tests located in the specified .py file
pytest source\ag_grid_test_demo.py

REM Deactivate the virtual environment after tests are done
deactivate
