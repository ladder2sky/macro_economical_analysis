import sys
import os
from conf.settings import industry_l2_category_2018
import core.central_bank_data as cent_bank

base_path = os.path.dirname(os.path.dirname(__file__))
sys.path.append(base_path)

df = cent_bank.get_central_bank_data(2023, '货币统计概览', '货币供应量')
print(df.head())
