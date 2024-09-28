import sys
import os
from core.main_industry_indicators import get_industry_main_indicators_data
from conf.settings import industry_l3_main_indicators
from core.nbos_api import save_to_csv

# Determine the base path for locating necessary files
base_path = os.path.dirname(os.path.dirname(__file__))
sys.path.append(base_path)


if __name__ == '__main__':
    for i, industry in enumerate(industry_l3_main_indicators, start=1):
        print(f'{i}. {industry}')

    try:
        # Get user's selection
        selection = int(input(f'Select an industry from above [1 to {len(industry_l3_main_indicators)}]: '))
        if selection < 1 or selection > len(industry_l3_main_indicators):
            raise ValueError("Selection out of range.")

        l3_industry = industry_l3_main_indicators[selection - 1]

        start_year = int(input('input start year for query:'))
        data_path = os.path.join(base_path, 'db')
        file_name = f'{l3_industry}_{start_year}_industry_indicators.csv'

        # Fetch industry PPI data
        l2_industry_df = get_industry_main_indicators_data(start_year,l3_industry)

        # Save to CSV file
        save_to_csv(l2_industry_df, data_path, file_name)

    except ValueError as ve:
        print(f"Invalid input: {ve}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")