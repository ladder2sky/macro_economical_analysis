import pandas as pd
from conf.settings import fix_asset_invest_category
from datetime import *
from core.nbos_api import *

def filter_invest_increment_ratio_menu():
    invest_increment_menu = []
    for item in fix_asset_invest_category:
        if '行业' in item and '固定资产投资' in item and '-' in item:
            invest_increment_menu.append(item)
    return invest_increment_menu


def get_fix_asset_invest_path_para(year):
    if year < 1998:
        print('Data source Only has data from 1998 till now. Data from 1998 will be collected.')
        year = 1998
    elif year >= date.today().year + 1:
        print('your input is year {}, however now is only year {}. wrong input.'.format(year, date.today().year))
        year = date.today().year
    # return ['固定资产投资(不含农户) > 按行业分固定资产投资增速（2018-）']
    l2_menu_lst = filter_invest_increment_ratio_menu()

    full_path_list = []
    for l2_menu in l2_menu_lst:
        start_year_in_menu = int(l2_menu.split('-')[0][-4:])
        if len(l2_menu.split('-')[1][:4]) < 4:
            end_year_in_menu = date.today().year
        else:
            end_year_in_menu = int(l2_menu.split('-')[1][:4])
        if start_year_in_menu > year:
            period = str(start_year_in_menu) + '-' + str(end_year_in_menu)
            path = '固定资产投资(不含农户) > ' + l2_menu
            full_path_list.append({'path':path, 'period':period})
        elif start_year_in_menu <= year <= end_year_in_menu:
            period = str(year) + '-' + str(end_year_in_menu)
            path = '固定资产投资(不含农户) > ' + l2_menu
            full_path_list.append({'path':path, 'period':period})
    return full_path_list

def get_fix_asset_invest_data(year, indicator='all'):
    kind = "月度数据"
    path_para_lst = get_fix_asset_invest_path_para(year)
    fix_asset_invest_df = pd.DataFrame()


    for path_para in path_para_lst:
        tmp_df = get_each_data(path=path_para['path'], period=path_para['period'],
                               indicate=indicator, kind=kind)
        fix_asset_invest_df = pd.concat([fix_asset_invest_df, tmp_df], ignore_index=True)
    fix_asset_invest_df.sort_values(by='date', inplace=True)
    fix_asset_invest_df.set_index('date', inplace=True)
    return fix_asset_invest_df

