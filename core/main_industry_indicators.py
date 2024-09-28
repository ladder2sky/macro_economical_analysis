import pandas as pd
from conf.settings import industry_l3_main_indicators
from datetime import *
from core.nbos_api import *


def get_industry_main_indicators_path(year, l3_path):
    industry_l2_main_indicators_paths =[
        '工业 > 按行业分工业企业主要经济指标(2001-2002)',
        '工业 > 按行业分工业企业主要经济指标(2003-2011)',
        '工业 > 按行业分工业企业主要经济指标(2012-2017)',
        '工业 > 按行业分工业企业主要经济指标(2018-至今)',
    ]
    if year < 2001:
        print('Data source Only has data from 2014 till now. Data from 2014 will be collected.')
        year = 2001
    elif year >= date.today().year + 1:
        print('your input is year {}, however now is only year {}. wrong input.'.format(year, date.today().year))
        year = date.today().year
    full_path_list = []
    for l2_path in industry_l2_main_indicators_paths:
        start_year_in_menu = int(l2_path.split('-')[0][-4:])
        if '至今' not in l2_path.split('-')[1][:4]:
            end_year_in_menu = int(l2_path.split('-')[1][:4])
        else:
            end_year_in_menu = date.today().year

        if start_year_in_menu > year:
            period = str(start_year_in_menu) + '-' + str(end_year_in_menu)
            path = l2_path + ' > ' + l3_path
            full_path_list.append({'path':path, 'period':period})
        elif start_year_in_menu <= year <= end_year_in_menu:
            period = str(year) + '-' + str(end_year_in_menu)
            path = l2_path + ' > ' + l3_path
            full_path_list.append({'path':path, 'period':period})
    return full_path_list

def get_industry_main_indicators_data(year, l3_path, indicator='all'):
    kind = "月度数据"
    path_para_lst = get_industry_main_indicators_path(year, l3_path)
    industry_main_indicators_df = pd.DataFrame()

    for path_para in path_para_lst:
        tmp_df = get_each_data(path=path_para['path'], period=path_para['period'],
                               indicate=indicator, kind=kind)
        industry_main_indicators_df = pd.concat([industry_main_indicators_df, tmp_df], ignore_index=True)
    industry_main_indicators_df.sort_values(by='date', inplace=True)
    industry_main_indicators_df.set_index('date', inplace=True)
    return industry_main_indicators_df
