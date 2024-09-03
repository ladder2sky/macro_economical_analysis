import sys
import os
from conf.settings import industry_l2_category_2018
import core.l2_ppi as l2_ppi


base_path = os.path.dirname(os.path.dirname(__file__))
sys.path.append(base_path)

if __name__ == '__main__':
    for i in range(1, len(industry_l2_category_2018)+1):
        print('{}. {}'.format(i, industry_l2_category_2018[i-1]))
    selection = int(input('select a industry from above.[1 to {}]: '.format(len(industry_l2_category_2018))))
    l2_industry = industry_l2_category_2018[selection-1]

    start_year = 2015
    data_path = base_path + '\\db\\'
    file_name = data_path + l2_industry + str(start_year) + '起ppi同月.csv'
    l2_industry_df = l2_ppi.get_l2_ppi(start_year, l2_industry)
    l2_industry_df.to_csv(file_name, encoding='gbk')
    print('Data was saved to file: {}'.format(file_name))
