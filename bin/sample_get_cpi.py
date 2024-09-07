"""A sample of getting input industry ppi since 2015. data will be saved in a csv file."""

import sys
import os
from datetime import datetime
import core.cpi_data as cpi_data
from conf.settings import cpi_last_year_period_category

if __name__ == '__main__':

    for i in range(len(cpi_last_year_period_category)):
        print("{}.{}".format(i+1, cpi_last_year_period_category[i]))
    selection = input('please choice from above by input index from(1 to {}): '.format(len(cpi_last_year_period_category)+1))
    # get_cpi_data(2012, '全国居民消费', 'all')
    selected_category = cpi_last_year_period_category[int(selection) - 1]
    print('you have chose {}.'.format(selected_category))
    input_year = int(input('From which year do you want to collect data?(2000-{}): '.format(datetime.today().year)))
    cpi_df = cpi_data.get_cpi_data(input_year, selected_category, 'all')
    print(cpi_df.head())