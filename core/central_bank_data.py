
import pandas as pd
import requests
import re
import datetime
from bs4 import BeautifulSoup

def get_year_data_link():
    """get a dictionary of year and related link to yearly data page
    :param, none
    :return, address_dict, a dict contains year and hyperlink. example: {'2016': 'http://www.pbc.gov.cn/diaochatongji
    si/116219/116319/3013637/index.html'}"""
    central_bank_year_list_page = 'http://www.pbc.gov.cn/diaochatongjisi/116219/116319/index.html'
    upper_address = 'http://www.pbc.gov.cn'
    header = {"user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
                          "Chrome/128.0.0.0 Safari/537.36 Edg/128.0.0.0"}
    resp = requests.get(central_bank_year_list_page, headers=header)
    resp.encoding = 'utf-8'
    #print(resp.text)
    obj = re.compile('<div class="wengao2"><a href=\'(?P<address>.*?)\'>(?P<year>.*?)年统计数据</a></div>')
    result = obj.finditer(resp.text)
    l1_address_dict = {}
    for it in result:
        address = upper_address + it.group('address')
        year = it.group('year')
        l1_address_dict[year] = address
    return l1_address_dict


def get_l2_data_link(year, category_name):
    """返回指定年丰和指标的二级数据网页地址。找不到相应网址，将返回空字符串。
    :param year, 年份， must above 2008 and till now
    :param category_name, name of indicator category, string format
    :return l2_hyper_link, a hyperlink, string format."""

    upper_address = 'http://www.pbc.gov.cn'
    header = {"user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
                          "Chrome/128.0.0.0 Safari/537.36 Edg/128.0.0.0"}

    l2_hyper_link = ''
    current_year = datetime.date.today().year
    if 2015 <= year <= current_year:
        l1_address_dict = get_year_data_link()
        year_page_link  = l1_address_dict[str(year)]
        resp = requests.get(year_page_link, headers=header)
        resp.encoding = 'utf-8'
        obj = re.compile(r"<td width='181' colspan='2' class='guidlevel01_style1' {2}><a href='"
                         r"(?P<address>.*?)' class='guidlevel01_style1'>(?P<name>.*?)</a></td>")
        result = obj.finditer(resp.text)
        #print(resp.text)
        l2_address_dict = {}
        for it in result:
            address = upper_address + it.group('address')
            name = it.group('name')
            l2_address_dict[name] = address

        if category_name in l2_address_dict.keys():
            l2_hyper_link = l2_address_dict[category_name]
        else:
            print('所选年份没有找到相应指标。 get_l2_data_link函数将返回一个空的字符串。')
    else:
        print('年份不能小于2015，不能大于{}。get_l2_data_link函数将返回一个空的字符串。'.format(current_year))
    return l2_hyper_link


def get_l3_data_link(l2_hyper_link, indicator):
    """
        Get the URL of a specific indicator within a category. If the indicator is not found, return an empty string.

        :param l2_hyper_link: The URL of the category page.
        :param indicator: The name of the indicator (as a string).
        :return: The URL of the indicator page, or an empty string if not found.
        """
    upper_address = 'http://www.pbc.gov.cn'
    header = {"user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
                            "Chrome/128.0.0.0 Safari/537.36 Edg/128.0.0.0"}

    l3_hyper_link = ''
    if l2_hyper_link !='':
        resp = requests.get(l2_hyper_link, headers=header)
        resp.encoding = 'utf-8'
        #print(resp.text)
        obj = re.compile('<div class="titp20">\s*(?P<name>.*?)\s*<br />.*?\s*</div></td>\s*'
                         '<td width="40" height="55" align="center" valign="middle"><a href="(?P<address>.*?)'
                         '" target="_blank">htm</a></td>')
        result = obj.finditer(resp.text)
        l3_address_dict = {}
        for it in result:
            indicator_name = it.group('name').strip()
            address = upper_address + it.group('address')
            # print(indicator_name, address)
            l3_address_dict[indicator_name] = address
        if l3_address_dict == {}:
            print('dict is blank.')
        if indicator in l3_address_dict.keys():
            l3_hyper_link = l3_address_dict[indicator]
        else:
            print('indicator is not found in l3 page. a blank string will be returned.')
    else:
        print('l2 address is blank. a blank string will be returned. ')
    return l3_hyper_link


def get_original_data(l3_hyper_link, indicator):
    """
        Fetches the actual data from the specified indicator page.

        :param l3_hyper_link: The URL for the indicator page.
        :param indicator: The name of the indicator (used to determine how to parse the page).
        :return: A pandas DataFrame containing the extracted data.
        """
    if indicator == '社会融资规模增量统计表':
        df = get_aggregate_financing_to_economy_data(l3_hyper_link)
    elif indicator == '货币供应量':
        df = get_money_supply_data(l3_hyper_link)
    else:
        print("The indicator, {}, isn't developed yet. a empty df will be return.".format(indicator))
        df = pd.DataFrame()
    return df


def get_money_supply_data(l3_hyper_link):
    """
        Extracts the money supply data from the indicator page and returns it as a DataFrame.

        :param l3_hyper_link: The URL for the money supply indicator page.
        :return: A pandas DataFrame containing the money supply data.
        """
    resp = requests.get(l3_hyper_link)
    resp.encoding = 'gbk'
    page = BeautifulSoup(resp.text, 'html.parser')
    table = page.find('table')
    trs = table.find_all('tr')
    columns_td = trs[5].find_all('td')
    columns = []
    df = pd.DataFrame()
    for col in columns_td:
        if col.text != '':
            columns.append(col.text)
    #print(trs[7:12:2])
    data_lst = []
    for tr in trs[7:12:2]:
        tds = tr.find_all('td')
        data_dict = {}
        for i in range(len(columns)):
            data_dict[columns[i]] = tds[i + len(data_lst)].text # 网页中每行都往后错一位，所以加len(data_lst)
        data_lst.append(data_dict)
    df = pd.DataFrame(data_lst)
    return df


def get_aggregate_financing_to_economy_data(l3_hyper_link):
    """
        Extracts aggregate financing to the economy data and returns it as a DataFrame.

        :param l3_hyper_link: The URL for the aggregate financing indicator page.
        :return: A pandas DataFrame containing the aggregate financing data.
        """
    resp = requests.get(l3_hyper_link)
    resp.encoding = 'gbk'
    page = BeautifulSoup(resp.text, 'html.parser')
    table = page.find('table')
    trs = table.find_all('tr')
    columns_td = trs[5].find_all('td')
    columns = ['年月']
    for col in columns_td:
        if col.text != '':
            columns.append(col.text)
    data_lst = []
    for tr in trs[7: 19]:
        tds = tr.find_all('td')
        data_dict = {}
        for i in range(len(columns)):
            data_dict[columns[i]] = tds[i].text
        data_lst.append(data_dict)
    df = pd.DataFrame(data_lst)
    return df


def get_central_bank_data(year, category, indicator):
    """
        Main function to retrieve central bank data for a specified year, category, and indicator.

        :param year: The year of the data (must be between 2008 and the current year).
        :param category: The category of the data.
        :param indicator: The specific indicator within the category.
        :return: None, but prints the resulting DataFrame or an empty message.
        """
    l2_hyper_link = get_l2_data_link(year, category)
    if l2_hyper_link !='':
        l3_hyper_link = get_l3_data_link(l2_hyper_link, indicator)
        if l3_hyper_link !='':
            result = get_original_data(l3_hyper_link, indicator)
            if not result.empty:
                return result
            else:
                print('Sorry, result is empty.')
                return None


