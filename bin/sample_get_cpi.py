"""A sample of getting input industry ppi since 2015. data will be saved in a csv file."""
import sys
import os
from datetime import datetime

import core.cpi_data as cpi_data
from conf.settings import cpi_last_year_period_category

# Determine the base path for locating necessary files
base_path = os.path.dirname(os.path.dirname(__file__))
sys.path.append(base_path)

if __name__ == '__main__':
    # Display the available categories for CPI data collection
    for i, category in enumerate(cpi_last_year_period_category):
        print("{}. {}".format(i + 1, category))

    # Input validation for category selection
    while True:
        try:
            selection = int(input(
                'Please choose from above by entering a number (1 to {}): '.format(len(cpi_last_year_period_category))))
            if 1 <= selection <= len(cpi_last_year_period_category):
                break
            else:
                print("Invalid selection. Please choose a valid number.")
        except ValueError:
            print("Please enter a valid number.")

    selected_category = cpi_last_year_period_category[selection - 1]
    print(f'You have chosen: {selected_category}')

    # Input validation for year
    current_year = datetime.today().year
    while True:
        try:
            input_year = int(input(f'From which year do you want to collect data? (2000-{current_year}): '))
            if 2000 <= input_year <= current_year:
                break
            else:
                print(f"Please enter a year between 2000 and {current_year}.")
        except ValueError:
            print("Please enter a valid year.")

    # Fetch the CPI data for the chosen category and year
    cpi_df = cpi_data.get_cpi_data(input_year, selected_category, 'all')

    # Construct the path for saving the data
    data_path = os.path.join(base_path, 'db')
    os.makedirs(data_path, exist_ok=True)  # Ensure the directory exists
    file_name = os.path.join(data_path, f'{selected_category}_{input_year}.csv')

    # Save the data to a CSV file
    cpi_df.to_csv(file_name, encoding='gbk')
    print(f'Data was saved to {file_name}')
