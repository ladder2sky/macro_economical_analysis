"""
主函数是get_l2_ppi(year, l2_industry)，返回dataframe结构的分行业中类ppi数据
"""
import pandas as pd
from conf.settings import industry_l2_category_2018
import akshare as ak
from datetime import *


def month_format_convert(month_str):
    """将月度转换为日期，即该月度最后一天
       :param month_str 例如 '2020年3月'
       :return month_str 日期，例如 '2020-3-31'
       :rtype datetime.date
       """
    fmt = '%Y年%m月%d日'
    date_str = month_str + '1日'
    temp_date = datetime.strptime(date_str, fmt)
    if temp_date.month < 12:
        last_date = date(temp_date.year, temp_date.month + 1, 1) - timedelta(days=1)
    else:
        last_date = date(temp_date.year, 12, 31)
    return last_date


def quarter_format_convert(quarter):
    """将季度转换为日期，即该季度最后一天
       :param 例如 '2020年一季度'
       :return 日期，例如 '2020-3-31'
       :rtype datetime.date
       """
    year = int(quarter[:4])
    if quarter[6] == '二':
        month, day = 6, 30
    elif quarter[6] == '一':
        month, day = 3, 31
    elif quarter[6] == '三':
        month, day = 9, 30
    else:
        month, day = 12, 31
    return date(year, month, day)


def year_format_convert(year_str):
    """将年份转换为日期，即该年最后一天12月31日
    :param 例如 '2020年'
    :return 日期
    :rtype datetime.date
    """
    year = int(year_str[:4])
    return date(year, 12, 31)


def get_each_data(path, period, indicate, kind="月度数据"):
    """获取指定的指标，并返回dataframe结构
    :param path 中分类行业名称
    :param period 字符串， 例如：‘2018-’，‘2016-2020’
    :param indicate 数据结构中的某一列，即某一指标，如果是全部则为 'all'
    :param kind 字符串，月度数据、季度数据、年度数据
    :return 返回宏观经济数据的dataframe结构
    :rtype dataframe
    """
    print('Getting data from {}.'.format(path))
    macro_df = ak.macro_china_nbs_nation(kind=kind, path=path, period=period)
    print('done.')
    macro_df = macro_df.T
    macro_df.index.name = '月份'
    macro_df = macro_df.reset_index()
    if kind == '月度数据':
        macro_df['date'] = macro_df['月份'].apply(month_format_convert)
    elif kind == '季度数据':
        macro_df['date'] = macro_df['月份'].apply(quarter_format_convert)
    else:
        macro_df['date'] = macro_df['月份'].apply(year_format_convert)
    if indicate != 'all':
        macro_df = macro_df[['date', indicate]]
        macro_df.rename(columns={indicate: "indicate"}, inplace=True)
    macro_df.drop(columns='月份', inplace=True)
    # macro_df.sort_values(by='date', inplace=True)
    # macro_df.set_index('date', inplace=True)
    return macro_df


def get_path_para(year, l2_industry):
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

