import requests
from bs4 import BeautifulSoup
from client import client
import time
from typing import List, Tuple, Any
import re
from google_translator import google_translator


s = client(proxy=True)


def str_repalce(char_list: List[str], string: str, re_string: str) -> str:
    '''
    替换字符
    '''
    for i in char_list:
        string = string.replace(i, re_string)
    return string


def google_scholar(key_words: str, artical_num: str) -> Tuple[str, str]:
    '''
    获取文献名称和链接
    '''
    #key_words = 'thermoelectric+and+Cu2Se+-film'
    scholar_link = f'https://scholar.google.com/scholar?start={artical_num}&q={key_words}&hl=zh-CN&as_sdt=0,5'
    scholar_result_soup = BeautifulSoup(s._get(scholar_link).content, features="html.parser")
    artical_info = scholar_result_soup.find(
            'div', 
            {
                'class': 'gs_r gs_or gs_scl', 
                'data-rp': artical_num
            }
        )
    artical_info = artical_info.find(
            'div', 
            {
                'class': 'gs_ri'
            }
        )
    artical_info = artical_info.find('a')
    name_list = artical_info.contents
    name = ''.join(i.string for i in name_list)
    name = str_repalce(['/', '\\', ':', '*', '"', '?', '>', '<', '|'], name,'_')
    return name, artical_info.attrs["href"]


#获取sci_hub下载链接
def get_dl_link(artical_link: str) -> Tuple[bool, str]:
    '''
    获取sci_hub下载链接
    '''
    sci_hub_link = "https://sci-hub.se/" + artical_link
    soup2 = BeautifulSoup(s._get(sci_hub_link).content, features="html.parser")
    dl_link_info = soup2.find("div", {"id": "buttons"})
    
    if not dl_link_info:
        return False, artical_link
    
    dl_link_info = dl_link_info.find('button')
    loc = dl_link_info.attrs['onclick']
    
    pattern = re.compile(r"\'(.*)\'")
    if re.search(r'sci-hub', loc):
        dl_link = 'https:' + pattern.search(loc)[1]
    else:
        dl_link = 'https://sci-hub.se' + pattern.search(loc)[1]
        
    """ 
    try:
        _ = loc.index('sci-hub')
        a = loc.index("'")
        b = loc.index("'", a + 1)
        dl_link = 'https:' + loc[a + 1:b]
    except ValueError:
        a = loc.index("'")
        b = loc.index("'", a + 1)
        dl_link = 'https://sci-hub.se' + loc[a+1:b] 
    """
        
    return True, dl_link


#获取摘要
def get_abstract_google(artical_name: str) -> str:
    '''
    从谷歌获取英文摘要
    '''
    artical_name = str_repalce([' '], artical_name, '+')
    artical_link = f'https://scholar.google.com/scholar?hl=zh-CN&as_sdt=0%2C5&q={artical_name}&btnG='
    scholar_result_soup = BeautifulSoup(s._get(artical_link).content, features="html.parser")
    abstract = scholar_result_soup.find(
            'div',
            {
                'class': 'gs_rs',
            }
        )
    if not abstract:
        raise
    abstract=''.join(i.string for i in abstract.contents if i.string)
    
    return abstract

#储存文件
def save_file(link: str, name: str) -> None:
    '''
    下载文献
    '''
    statu, url = get_dl_link(link)
    if statu:
        with open(name + '.pdf', 'wb') as f:
            f.write(s._get(url).content)
        print(name + '     successful')
    else:
        with open('error.txt', 'a+') as f:
            f.write(f'{name}  {url}  \n')
        print(name + '     failed')


if __name__ == '__main__':
    start_num = 0
    for i in range(0, 2):
        artical_num = str(start_num + i)
        name, url = google_scholar('thermal', artical_num)
        #save_file(url, name)
        #get_abstract(name)
        print(name)
        time.sleep(10)