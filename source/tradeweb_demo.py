import re
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time


def get_driver():
    # Initialize the driver for Chrome
    return webdriver.Chrome(service=Service(ChromeDriverManager().install()))


def launch_webpage(driver):
    driver.get("https://www.ag-grid.com/example-finance/")
    time.sleep(3)  # Adjust the wait time as needed

def close_driver(driver):
    driver.quit()

def validate_numeric_column_values(identifier):
    driver = get_driver()
    try:
        time.sleep(3)
        launch_webpage(driver)
        instrument_col_cells = driver.find_elements(By.CSS_SELECTOR, identifier)
        instrument_cell_values = [cell.text for cell in instrument_col_cells]
        for instrument_cell_value in instrument_cell_values:
            assert bool(re.match(r'^-?\d+(\.\d+)?$', instrument_cell_value))
    finally:
        close_driver(driver)


def test_validate_numeric_column():
    pass

def test_validate_sorting_functionality():
    pass

def test_validate_instrument_column():
    driver = get_driver()
    try:
        time.sleep(3)
        launch_webpage(driver)
        instrument_col_cells = driver.find_elements(By.CSS_SELECTOR, '')
        instrument_cell_values = [cell.text for cell in instrument_col_cells]
        allowed_values = ['Bond', 'ETF', 'Crypto', 'Stock']
        for instrument_cell_value in instrument_cell_values:
            if instrument_cell_value in allowed_values:
                assert True
            else:
                assert False
    finally:
        close_driver(driver)
