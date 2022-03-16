from httpx import Client, Response
from httpx._exceptions import *
from typing import Dict, List, Union, Tuple
from bs4 import BeautifulSoup, PageElement, NavigableString, Tag
import re
from .config import Config

T = Union[BeautifulSoup, Tag, NavigableString]
config = Config()

class client():
    
    proxy_statu: bool = config.proxy_statu
    
    def __init__(self):
        self.headers: Dict = {
                    "User-Agent": 'Mozilla/5.0 (iPhone; CPU iPhone OS 15_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.1.1 Mobile/15E148 Safari/604.1',
                    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
                }
        
        if self.proxy_statu:
            self.proxies: str = config.proxies
    
    @classmethod
    def get(cls, url: str) -> Response:
        
        api = cls().call()
        res = api.get(url=url, timeout=25)
        if res.status_code == 302:
            res = api.send(res.next_request)
        api.close()
        return res
    
    @classmethod
    def get_with_headers(cls, url: str, headers: Dict = None) -> Response:
        api = cls().call(headers=headers)
        res = api.get(url=url, timeout=25)
        api.close()
        return res
    
    @classmethod
    def get_no_headers(cls, url: str) -> Response:
        api = Client()
        res = api.get(url=url, timeout=25)
        api.close()
        return res
    
    @classmethod
    def post(cls, url: str, json: Dict) -> Response:
        
        api = cls().call()
        res = api.post(url=url, json=json, timeout=25)
        api.close()
        return res
    
    
    def call(self, headers: Dict = None) -> Client:
        if not headers:
            headers=self.headers
        if self.proxy_statu:
            return Client(proxies=self.proxies, headers=headers)
        return Client(headers=self.headers)


def str_replace(char_list: List[str], string: str, re_string: str) -> str:
    '''
        替换字符
        
          * ``char_list: Lsit[str]``: 需要替换的字符
            
          * ``string: str``: 需要替换字符的字符串
            
          * ``re_string: str``: 替换的目标
        
        例如：
        
            str_replace ([ '?' ], 'test?', '' )
            
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


def save_file(link: str, dir: str) -> None:
    '''
        下载文献
    '''
    dir = str_replace(['/', '\\', ':', '*', '"', '?', '>', '<', '|'], dir,'_')
    statu, url = get_dl_link(link)
    if statu:
        with open(dir + '.pdf', 'wb') as f:
            f.write(client.get(url).content)
        print(dir + '     successful')
    else:
        with open('error.txt', 'a+', encoding='utf-8') as f:
            f.write(f'{dir}  {url}  \n')
        print(dir + '     failed')
