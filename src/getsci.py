from bs4 import BeautifulSoup
from client import client
import time
from typing import List, Tuple, Dict
import re
from artical import get_artical, Artical


s = client()


def str_repalce(char_list: List[str], string: str, re_string: str) -> str:
    '''
    替换字符
    '''
    for i in char_list:
        string = string.replace(i, re_string)
    return string


def google_scholar(key_words: str, artical_page: str) -> List[Artical]:
    '''
    获取文献名称和链接,time,journal,database
    '''
    #key_words = 'thermoelectric+and+Cu2Se+-film'
    artical: List[Artical] = []
    artical_num = (int(artical_page)-1)*20
    scholar_link = f'https://scholar.google.com/scholar?start={artical_page}&q={key_words}&hl=zh-CN&num=20&as_sdt=0,5'
    scholar_result_soup = BeautifulSoup(s.get(scholar_link).content, features="html.parser")
    for i in range(artical_num,artical_num+20):
        artical_info = scholar_result_soup.find(
                'div', 
                {
                    'class': 'gs_r gs_or gs_scl', 
                    'data-rp': i
                }
            )
        artical_time=artical_info.find(
                'div',
                {
                    'class': 'gs_a'
                }
            ).contents

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
        artical_time = ''.join(i.string for i in artical_time)
        info = get_base_info(artical_time)
        info['name'] = name
        info['url'] = artical_info.attrs["href"]
        artical.append(get_artical(info))   
    return artical
   

def get_base_info(string: str) -> Dict:

    get_partern = re.compile(r'(.*)\s-\s(.*)\s-\s(.*)')
    print(string)
    res = get_partern.search(string)
    author = res[1]
    year = res[2]
    database = res[3]
    if re.search(',', year):
        get_p = re.compile(r'(.*),\s(.*)')
        res_p = get_p.search(year)
        journal = res_p[1]
        year = res_p[2]
    else:
        journal = 'book'
    return {
        'author': author,
        'year': year,
        'journal': journal,
        'database': database
    }

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
    return True, dl_link




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
    a = google_scholar('thermal', 3)
    en, ch = a[0].abstract()
    print(en, ch)
    


