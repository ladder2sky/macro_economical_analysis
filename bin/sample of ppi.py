import sys
import os
from conf.settings import industry_l2_category_2018
import core.l2_ppi as l2_ppi
from core.nbos_api import save_to_csv
# Get the base directory of the project
base_path = os.path.dirname(os.path.dirname(__file__))
sys.path.append(base_path)

def clean_columns(df):
    """
    Cleans column names by removing '工业生产者出厂价格指数(上年同月=100)' if present.

    Args:
        df (DataFrame): DataFrame to be cleaned.

    Returns:
        DataFrame: Cleaned DataFrame with updated column names.
    """
    old_cols = df.columns
    df.rename(columns={col: col.replace("工业生产者出厂价格指数(上年同月=100)", '') for col in old_cols}, inplace=True)
    return df


if __name__ == '__main__':
    # Display industry options for user to select
    for i, industry in enumerate(industry_l2_category_2018, start=1):
        print(f'{i}. {industry}')

    try:
        # Get user's selection
        selection = int(input(f'Select an industry from above [1 to {len(industry_l2_category_2018)}]: '))
        if selection < 1 or selection > len(industry_l2_category_2018):
            raise ValueError("Selection out of range.")

        l2_industry = industry_l2_category_2018[selection - 1]

        start_year = 2015
        data_path = os.path.join(base_path, 'db')
        file_name = f'{l2_industry}_{start_year}_ppi.csv'

        # Fetch industry PPI data
        l2_industry_df = l2_ppi.get_l2_ppi(start_year, l2_industry)

        # Clean column names
        l2_industry_df = clean_columns(l2_industry_df)

        # Save to CSV file
        save_to_csv(l2_industry_df, data_path, file_name)

    except ValueError as ve:
        print(f"Invalid input: {ve}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
