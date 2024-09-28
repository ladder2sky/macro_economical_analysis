import sys
import os
from conf.settings import industry_l2_category_2018
import core.central_bank_data as cent_bank

base_path = os.path.dirname(os.path.dirname(__file__))
sys.path.append(base_path)


if __name__ == '__main__':
    money_supply_df = cent_bank.get_central_bank_data(2023, '货币统计概览', '货币供应量')
    print(money_supply_df.head())
    financing_increment_df = cent_bank.get_central_bank_data(2024, '社会融资规模', '社会融资规模增量统计表')
    print(financing_increment_df.head())
