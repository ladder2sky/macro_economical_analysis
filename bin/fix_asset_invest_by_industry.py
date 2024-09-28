import sys
import os
from core.fix_asset_invest import get_fix_asset_invest_data

# Determine the base path for locating necessary files
base_path = os.path.dirname(os.path.dirname(__file__))
sys.path.append(base_path)

if __name__ == '__main__':
    start_query_year = 2002
    asset_invest_df = get_fix_asset_invest_data(start_query_year)
    data_path = os.path.join(base_path, 'db')
    os.makedirs(data_path, exist_ok=True)  # Ensure the directory exists
    file_name = os.path.join(data_path, f'fix_asset_invest_date_from_{start_query_year}.csv')
    asset_invest_df.to_csv(file_name, encoding='gbk')