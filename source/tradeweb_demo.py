import re
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By


def get_driver():
    # Initialize the driver for Chrome
    return webdriver.Chrome(service=Service(ChromeDriverManager().install()))


def launch_webpage(driver):
    driver.get("https://www.ag-grid.com/example-finance/")
    time.sleep(3)  # Adjust the wait time as needed

def close_driver(driver):
    driver.quit()

def validate_numeric_column_values(value_to_validate):
    assert bool(re.match(r'^[\d,.]+$', value_to_validate))

def get_table_data_as_column(column_name):
    ticker = []
    instrument = []
    pnl = []
    total_value = []
    quantity = []
    price = []
    last_24_hrs = []

    driver = get_driver()
    try:
        launch_webpage(driver)
        time.sleep(3)

        grid = driver.find_element(By.CSS_SELECTOR, ".ag-root-wrapper-body")

        rows = grid.find_elements(By.CSS_SELECTOR, ".ag-row")

        for row in rows:
            cells = row.find_elements(By.CSS_SELECTOR, ".ag-cell")
            row_data = [cell.text for cell in cells]
            ticker.append(row_data[0])
            instrument.append(row_data[1])
            pnl.append(row_data[2])
            total_value.append(row_data[3])
            quantity.append(row_data[4])
            price.append(row_data[5])
            last_24_hrs.append(row_data[6])

    finally:
        close_driver(driver)

    return locals().get(column_name)






def test_validate_sorting_functionality():
    pass


def test_validate_instrument_column():
    instrument_col_values = get_table_data_as_column('instrument')
    allowed_values = ['Bond', 'ETF', 'Crypto', 'Stock']
    for instrument_col_value in instrument_col_values:
        assert (instrument_col_value in allowed_values)


def test_validate_pnl_values():
    pnl_column_values = get_table_data_as_column('pnl')
    print(pnl_column_values)
    for pnl_column_value in pnl_column_values:
        validate_numeric_column_values(pnl_column_value.lstrip('↑').lstrip('↓'))


def test_validate_total_value_values():
    total_value_column_values = get_table_data_as_column('total_value')
    print(total_value_column_values)
    for total_value_column_value in total_value_column_values:
        validate_numeric_column_values(total_value_column_value.lstrip('↑').lstrip('↓'))

