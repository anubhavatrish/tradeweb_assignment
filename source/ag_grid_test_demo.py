import re
import time
from selenium import webdriver
from selenium.common import NoSuchElementException
from selenium.webdriver import ActionChains
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.wait import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as ec



def get_driver():
    # Initialize the driver for Chrome
    return webdriver.Chrome(service=Service(ChromeDriverManager().install()))


def launch_webpage(driver):
    driver.get("https://www.ag-grid.com/example-finance/")
    driver.maximize_window()
    time.sleep(3)


def close_driver(driver):
    driver.quit()


def find_header_element_by_label(driver, label):
    WebDriverWait(driver, 10).until(ec.visibility_of_all_elements_located((By.CSS_SELECTOR, ".ag-header-cell-text")))
    # Find the header element by label
    headers = driver.find_elements(By.CSS_SELECTOR, ".ag-header-cell-text")
    for header in headers:
        if label == header.text:
            return header


def get_table_data_as_rows(driver):
    table_rows = []
    table_header = []
    time.sleep(5)
    try:
        # Wait until the headers are visible
        WebDriverWait(driver, 10).until(ec.visibility_of_all_elements_located((By.CSS_SELECTOR, ".ag-header-cell-text")))

        # Find all the headers and add the text values to a list
        headers = driver.find_elements(By.CSS_SELECTOR, ".ag-header-cell-text")
        header_row = [header.text for header in headers]
        table_header.append(header_row)

        # Scroll and iterate through rows to add them to the table rows list
        row_index = 0
        consecutive_scroll_count = 0
        while True:
            try:
                if 2 == consecutive_scroll_count: # If two consecutive scroll actions do not result in new rows, break the loop
                    print(f'\nconsecutive scroll count reached 2 at the row index: {row_index}')
                    break

                row = driver.find_element(By.CSS_SELECTOR, f".ag-row[row-index='{row_index}']")
                cells = row.find_elements(By.CSS_SELECTOR, ".ag-cell")
                row_data = [cell.text for cell in cells]
                table_rows.append(row_data)
                row_index += 1  # Move to the next row index
                consecutive_scroll_count = 0 # Reset consecutive scroll count

            except NoSuchElementException: # If the current value of row index is not found, scroll the grid
                driver.execute_script("document.querySelector('.ag-body-viewport').scrollTop += 500;")
                time.sleep(2)
                consecutive_scroll_count +=1
    finally:
        pass

    return table_header, table_rows

# Functional validation requirement #1(i)
def test_validate_sort_ascending_by_ticker_column():
    driver = get_driver()
    launch_webpage(driver)
    ticker_header_label = find_header_element_by_label(driver, "Ticker")
    ticker_header_label.click()
    time.sleep(2)
    table_header, table_data_rows = get_table_data_as_rows(driver)
    close_driver(driver)
    ticker_column_values = []
    for row in table_data_rows:
        ticker_column_values.append(row[0])
    assert ticker_column_values == sorted(ticker_column_values), f'The values for the Ticker column are not sorted in ascending order'


# Functional validation requirement #1(ii)
def test_validate_sort_descending_by_ticker_column():
    driver = get_driver()
    launch_webpage(driver)
    ticker_header_label = find_header_element_by_label(driver, "Ticker")
    ticker_header_label.click() # Click on the header to sort in ascending order
    time.sleep(2)
    ticker_header_label.click()  # Click once more on the header to sort in descending order
    time.sleep(2)
    table_header, table_data_rows = get_table_data_as_rows(driver)
    close_driver(driver)
    ticker_column_values = []
    for row in table_data_rows:
        ticker_column_values.append(row[0])
    assert ticker_column_values == sorted(ticker_column_values, reverse=True), f'The values for the Ticker column are not sorted in descending order'


# Functional validation requirement #2
def test_validate_instrument_column_values():
    driver = get_driver()
    launch_webpage(driver)
    table_header, table_data_rows = get_table_data_as_rows(driver)
    close_driver(driver)
    allowed_values = ['Bond', 'ETF', 'Crypto', 'Stock']
    for row in table_data_rows:
        assert row[1] in allowed_values, f'The "Instrument" column value "{row[1]}" for the row with ticker "{row[0]}" is not is not in {allowed_values}'


# Functional validation requirement #3
def test_validate_numeric_column_values():
    driver = get_driver()
    launch_webpage(driver)
    table_header, table_data_rows = get_table_data_as_rows(driver)
    close_driver(driver)
    for row in table_data_rows:
        assert re.match(r'^[\d,.]+$', row[2].lstrip('↑').lstrip('↓')), f'The "P&L" column value "{row[2]}" for the row with ticker "{row[0]}" is not a number'
        assert re.match(r'^[\d,.]+$', row[3].lstrip('↑').lstrip('↓')), f'The "Total Value" column value "{row[3]}" for the row with ticker "{row[0]}" is not a number'
        assert re.match(r'^[\d,.]+$', row[4]), f'The "Quantity" column value "{row[4]}" for the row with ticker "{row[0]}" is not a number'
        assert re.match(r'^[\d,.]+$', row[5]), f'The "Price" column value "{row[5]}" for the row with ticker "{row[0]}" is not a number'


# Functional validation requirement #4 (i)
def test_validate_pnl_calculation():
    driver = get_driver()
    launch_webpage(driver)
    table_header, table_data_rows = get_table_data_as_rows(driver)
    close_driver(driver)
    for row in table_data_rows:
        try:
            pnl = float(row[2].replace(',', ''))
            total_value = float(row[3].replace(',', ''))
            quantity = float(row[4].replace(',', ''))
            price = float(row[5].replace(',', ''))
            calculated_pnl = total_value - quantity*price
            assert calculated_pnl == pnl, f'The calculated PnL "{calculated_pnl}" is not equal to the PnL value "{pnl}" from the grid for the row with ticker "{row[0]}"'
        except ValueError:
            print(f'Error converting values to numbers for the row : {row}')


# Functional validation requirement #4 (ii)
def test_validate_adding_column_to_the_grid():
    driver = get_driver()
    launch_webpage(driver)
    table_header, table_data_rows = get_table_data_as_rows(driver) # Fetch the table header and rows immediately after loading the page
    ticker_header_label = find_header_element_by_label(driver, "Ticker")
    actions = ActionChains(driver)
    actions.context_click(ticker_header_label).perform()
    time.sleep(10)
    menu_options = driver.find_elements(By.CSS_SELECTOR, ".ag-menu-option-text")
    for menu_option in menu_options:
        if menu_option.text == 'Choose Columns':
            menu_option.click()
            time.sleep(2)
            break
    checkboxes = driver.find_elements(By.CSS_SELECTOR, ".ag-column-select-column-label")
    for checkbox in checkboxes:
        if checkbox.text == 'Purchase Date':
            checkbox.click()
            time.sleep(2)
            break

    table_header_updated, table_data_rows_updated = get_table_data_as_rows(driver) # Fetch the table header and rows after adding the new column
    close_driver(driver)

    print(f'Number of columns before adding additional columns is :{len(table_header[0])}')
    print(f'Number of columns after adding additional columns is :{len(table_header_updated[0])}')

    assert int(len(table_header[0]) + 1) == int(len(table_header_updated[0])), f'Additional column "Purchase Date" could not be added to the grid'

# Functional validation requirement #4(iii)
def test_validate_sorting_descending_by_ticker_column():
    driver = get_driver()
    launch_webpage(driver)
    ticker_header_label = find_header_element_by_label(driver, "Ticker")
    ticker_header_label.click() # Click on the header to sort in ascending order
    time.sleep(2)
    ticker_header_label.click()  # Click once more on the header to sort in descending order
    time.sleep(2)
    table_header, table_data_rows = get_table_data_as_rows(driver)
    close_driver(driver)
    ticker_column_values = []
    for row in table_data_rows:
        ticker_column_values.append(row[0])
    assert ticker_column_values == sorted(ticker_column_values, reverse=True), f'The values for the Ticker column are not sorted in descending order'


