import pandas as pd
from conf.settings import industry_l2_category_2018
from datetime import *
from core.nbos_api import *


def get_cpi_path_para(year, category):
    upper_path = '价格指数 > 居民消费价格分类指数(上年同期=100)'
    l3_path_list = [
        '全国居民消费价格分类指数(上年同期=100)(2016-)',
        '全国居民消费价格分类指数(上年同期=100)(-2015)',
        '全国食品类居民消费价格指数(上年同期=100)',
        '城市居民消费价格分类指数(上年同期=100)(2016-)',
        '城市居民消费价格分类指数(上年同期=100)(-2015)',
        '食品类城市居民消费价格指数(上年同期=100)',
        '农村居民消费价格分类指数(上年同期=100)(2016-)',
        '农村居民消费价格分类指数(上年同期=100)(-2015)',
        '食品类农村居民消费价格指数(上年同期=100)',
        '全国衣着类居民消费价格指数(上年同期=100)',
        '全国居住类居民消费价格指数(上年同期=100)',
        '全国生活用品及服务类居民消费价格指数(上年同期=100)  ',
        '全国交通通信类居民消费价格指数(上年同期=100)',
        '全国教育文化娱乐类居民消费价格指数(上年同期=100)',
        '全国医疗保健类居民消费价格指数(上年同期=100)'
    ]
    temp_l3_path_list = []
    full_path_list = []
    for l3_path in l3_path_list:
        if category in l3_path:
            temp_l3_path_list.append(l3_path)
    if not temp_l3_path_list:
        print('input category was not found in database. please check the input. an empty list will be returned.')
    else:
        if len(temp_l3_path_list) >= 2:
            if year >= 2016:
                temp_l3_path_list = temp_l3_path_list[:1]
        # print(temp_l3_path_list)
        if len(temp_l3_path_list) == 1:
            full_path = upper_path + ' > ' + temp_l3_path_list[0]
            path_dict = {'path':full_path, 'period': str(year) + '-'}
            full_path_list.append(path_dict)
        else:
            for temp_l3_path in temp_l3_path_list:
                full_path = upper_path + ' > ' + temp_l3_path
                if temp_l3_path[-2:] != '-)':
                    end_year = temp_l3_path[-5:-1]
                    start_year = str(year)
                else:
                    start_year = temp_l3_path[-6:-2]
                    end_year = str(date.today().year)
                path_dict = {'path': full_path, 'period': start_year + '-' + end_year}
                full_path_list.append(path_dict)

    return full_path_list


def get_cpi_data(year, category, indicator):
    kind = '月度数据'
    cpi_df = pd.DataFrame()
    cpi_path_list = get_cpi_path_para(year, category)
    for item in cpi_path_list:
        temp_df = get_each_data(item['path'], item['period'], indicator, kind)
        cpi_df = pd.concat([cpi_df, temp_df], ignore_index=True)
    cpi_df.sort_values(by='date', inplace=True)
    cpi_df.set_index('date', inplace=True)
    return cpi_df

