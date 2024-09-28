"""
主函数是get_l2_ppi(year, l2_industry)，返回dataframe结构的分行业中类ppi数据
"""

import pandas as pd
from conf.settings import industry_l2_category_2018
from datetime import *
from core.nbos_api import *


def get_path_para(year, l2_industry):
    """

    :param year: int
    :param l2_industry: string name of l2 industry
    :return: list contains dictionary with path and period
    """
    l2_path_list = ['价格指数 > 分行业中类工业生产者出厂价格指数(上年同月=100)(2018 - 至今)',
                    '价格指数 > 分行业中类工业生产者出厂价格指数(上年同月=100)(2014 - 2017)']
    if year < 2014:
        print('Data source Only has data from 2014 till now. Data from 2014 will be collected.')
        year = 2014
    elif year >= date.today().year + 1:
        print('your input is year {}, however now is only year {}. wrong input.'.format(year, date.today().year))
        year = date.today().year

    full_path_list = []
    if l2_industry in industry_l2_category_2018:
        if year >= 2018:
            loop_num = 1
        else:
            loop_num = 2
        for i in range(loop_num):
            if i == 1:
                if l2_industry == '石油、煤炭及其他燃料加工业':
                    l2_industry = '石油加工、炼焦和核燃料加工业'
                elif l2_industry == '酒、饮料及精制茶制造业':
                    l2_industry = '酒、饮料和精制茶制造业'
                elif l2_industry == '开采专业及辅助性活动' or l2_industry == '燃气生产和供应业':
                    print('no data for 开采专业及辅助性活动 and 燃气生产和供应业 before 2018.')
                    break
            full_path = l2_path_list[i] + ' > ' + l2_industry + '工业生产者出厂价格指数(上年同月=100)'
            path_start_year = int(l2_path_list[i].split('(上年同月=100)(')[1][:4])  # 计算period参数
            if year > path_start_year:
                start_period = year
            else:
                start_period = path_start_year
            if l2_path_list[i].split(' - ')[1][:2] == '至今':
                end_period_str = ''
            else:
                end_period_str = l2_path_list[i].split(' - ')[1][:4]
            full_path_list.append({'path': full_path, 'period': str(start_period) + '-' + end_period_str})
        # print(full_path_list)
    else:
        print('industry name wrong.')
    return full_path_list


def get_l2_ppi(year, l2_industry):
    indicate = 'all'
    kind = '月度数据'
    ppi_df = pd.DataFrame()
    full_path_list = get_path_para(year, l2_industry)
    for item in full_path_list:
        temp_df = get_each_data(item['path'], item['period'], indicate, kind)
        old_col_list = list(temp_df.columns)
        col_dict = {}

        #2017年前和2018年以后， 列名上差了一个‘业’字。需要特殊处理
        for old_col in old_col_list:
            if old_col.split('工业生产者出厂价格指数')[0][-1] == '业':
                new_col = old_col.split('工业生产者出厂价格指数')[0][:-1] + '工业生产者出厂价格指数' + old_col.split('工业生产者出厂价格指数')[1]
                col_dict[old_col] = new_col
        if col_dict != {}:
            temp_df.rename(columns=col_dict, inplace=True)
        ppi_df = pd.concat([ppi_df, temp_df], ignore_index=True)
    ppi_df.sort_values(by='date', inplace=True)
    ppi_df.set_index('date', inplace=True)
    return ppi_df


'''
以下几个行业2018和2014的名称上有区别
['开采专业及辅助性活动' ： 2014以前没有, 
'石油、煤炭及其他燃料加工业'： , 2014叫：'石油加工、炼焦和核燃料加工业'
'燃气生产和供应业'： 2014前没有, 
'酒、饮料及精制茶制造业'： 2014前叫'酒、饮料和精制茶制造业']
'''

