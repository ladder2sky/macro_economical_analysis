import sys
import os
from datetime import datetime
import numpy as np
import pandas as pd

from conf.settings import industry_l2_category_2018
import core.central_bank_data as cent_bank
from core.nbos_api import month_format_convert

base_path = os.path.dirname(os.path.dirname(__file__))
sys.path.append(base_path)


if __name__ == '__main__':
    start_year = 2015
    money_supply_df = pd.DataFrame()
    for query_year in range(start_year, datetime.today().year + 1):
        temp_df = cent_bank.get_central_bank_data(query_year, '货币统计概览', '货币供应量')
        print('Data of {} year was collected.'.format(query_year))
        col_0 = temp_df.columns[0]

        # temp_df第一列都是中文，但是有乱码的情况，下面两行处理乱码，替换成可识别的中英文
        temp_df.rename(columns={col_0: '项目 Item'}, inplace=True)
        temp_df['项目 Item'] = temp_df['项目 Item'].apply(lambda x:  np.where('M0' in x, 'M0',
                                          np.where('M1' in x, 'M1', 'M2')))
        temp_df.set_index('项目 Item', inplace=True)
        temp_df = temp_df.T
        temp_df.columns.name = ''
        temp_df.index.name = '日期'
        temp_df.reset_index(inplace=True)
        temp_df['日期'] = temp_df['日期'].apply(lambda x: x.split('.')[0]+'年'+x.split('.')[1].strip()+'月')
        temp_df['日期'] = temp_df['日期'].apply(month_format_convert)
        money_supply_df = pd.concat([money_supply_df, temp_df], ignore_index=True)


    data_path = os.path.join(base_path, 'db')
    os.makedirs(data_path, exist_ok=True)  # Ensure the directory exists
    file_name = os.path.join(data_path, f'money_supply_{str(start_year)}_{str(datetime.today().year)}.csv')
    money_supply_df.to_csv(file_name, encoding = 'gb2312')
    print('Data was saved to {}.'.format(file_name))
