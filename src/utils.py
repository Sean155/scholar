from httpx import Client, Response
from typing import Dict, List, Union, Tuple
from bs4 import BeautifulSoup, PageElement, NavigableString, Tag
import re

T = Union[BeautifulSoup, Tag, NavigableString]

class client():
    
    def __init__(self):

        self.headers: Dict = {
                "User-Agent": 'Mozilla/5.0 (iPhone; CPU iPhone OS 15_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.1.1 Mobile/15E148 Safari/604.1',
                "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
                }
        self.proxies: str = "http://127.0.0.1:7890"
    
    @classmethod
    def get(cls, url: str, proxy: bool = True) -> Response:
        
        api = cls().call(proxy=proxy)
        
        res = api.get(url=url, timeout=20)
        api.close()
        return res
    
    @classmethod
    def post(cls, url: str, json: Dict, proxy: bool = True) -> Response:
        
        api = cls().call(proxy=proxy)
        res = api.post(url=url, json=json, timeout=20)
        api.close()
        return res
    
    def call(self, proxy: bool) -> Client:
        if proxy:
            return Client(proxies=self.proxies, headers=self.headers)
        return Client(headers=self.headers)

def str_replace(char_list: List[str], string: str, re_string: str) -> str:
    '''
    替换字符
    
    char_list: 需要替换的字符
    
    string: 需要替换字符的字符串
    
    re_string: 替换的目标
    
    例如：
    
    str_replace ( [ '?' ] , 'test?' , '' )
    
    ==> 'test'
    '''
    for i in char_list:
        string = string.replace(i, re_string)
    return string

def bs(url: str) -> BeautifulSoup:
    
    return BeautifulSoup(client.get(url).content, features="html.parser")

def bs_find(bs: T, 
            tag: str, 
            attr_key: Union[List[str], str], 
            attr_value: Union[List[str], str]
            ) -> Union[Tag, NavigableString, None]:
    
    if isinstance(attr_key, List) and isinstance(attr_value, List):
        attr = {}
        for i in range(len(attr_key)):
            attr[attr_key[i]] = attr_value[i]
    elif isinstance(attr_key, str) and isinstance(attr_value, str):
        attr = {attr_key: attr_value}
    else:
        raise ValueError(f'Wrong attr_key, attr_value:{attr_key}, {attr_value}')
    
    return bs.find(tag, attr)



#获取sci_hub下载链接
def get_dl_link(artical_link: str) -> Tuple[bool, str]:
    '''
    获取sci_hub下载链接
    '''
    sci_hub_link = "https://sci-hub.se/" + artical_link
    soup2 = BeautifulSoup(client.get(sci_hub_link).content, features="html.parser")
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
            f.write(client.get(url).content)
        print(name + '     successful')
    else:
        with open('error.txt', 'a+') as f:
            f.write(f'{name}  {url}  \n')
        print(name + '     failed')
