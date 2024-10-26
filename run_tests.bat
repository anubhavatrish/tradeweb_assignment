@echo off
REM Activate the virtual environment
call venv\Scripts\activate

REM Run pytest tests located in the specified .py file
pytest source\ag_grid_test_demo.py

REM Deactivate the virtual environment after tests are done
deactivate
