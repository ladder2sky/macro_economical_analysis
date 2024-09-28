"""
common functions to collect data from national stats bureau.
"""
import akshare as ak
from datetime import *
import sys
import os


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

def save_to_csv(df, path, csv_file_name):
    """
    Saves the given DataFrame to a CSV file.

    Args:
        df (DataFrame): DataFrame to be saved.
        path (str): Directory path to save the file.
        csv_file_name (str): Name of the CSV file.
    """
    full_path = os.path.join(path, csv_file_name)
    try:
        df.to_csv(full_path, encoding='gbk')
        print(f'Data was saved to file: {full_path}')
    except Exception as e:
        print(f"Error saving file: {e}")