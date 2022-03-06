import re
import time
from bs4 import BeautifulSoup
from bs4.element import PageElement
from typing import Any, List, Dict, Union
from utils import client, Response, str_replace, bs, bs_find


db_list = ['aip', 'elsevier', 'iop', 'wiley', 'springer']

over_five_Wall_url = 'http://10.141.5.152:8191/v1'

class get_abstract():
    
    def __init__(self, url: str) -> None:
        self.url: str = url
        self.text: str = None
        self.statu: bool = True
    
    
    def get(self, database: str, tag: str) -> 'get_abstract':
        '''
        Get abstract
        
        Database: tag of Inputed Database
        Url: Link of Artical
        
        Notice! IOP Seems Proxy Forbiden!
        '''
        for i in db_list:
            if re.match(i, database.lower()):
                self.text = getattr(self, i)()
                return self
        try:
            self.text = get_abstract_baidu(tag) + 'BD'
        except:
            try:
                self.text = get_abstract_google(tag) + 'GG'
            except:
                self.statu = False
                self.text = f'Failed to get abstract from google scholar, baidu scholar.'
        return self
    
    def abstract_format(self, abstract: List[PageElement]) -> str:
        '''
        格式化摘要文本
        '''
        p_abstract = ''
        for i in abstract:
            if i:
                if i.string:
                    if not re.match('Abstract', i.string):
                        p_abstract = p_abstract + i.string
                elif i.text:
                    p_abstract = p_abstract + i.text
        return p_abstract
    
    def five_wall_check(self, res: Response) -> bool:
        '''
        检测是否5s墙
        '''
        if re.search('Please allow up to 5 seconds', res.text):
            return True
        return False
    
    def abstract_find(self, 
                      tag: str = 'div', 
                      attr_key: str = 'class', 
                      attr_value: str = ..., 
                      is_cloud: bool = False) -> str:
        '''
        搜索摘要文本
        '''
        if is_cloud:
            res = self.over_five_wall()
        else:
            res = bs(self.url)
            
        try:
            abstract = bs_find(res, tag, attr_key, attr_value).contents
        except:
            self.statu = False
            if self.five_wall_check(res):
                return f'Get abstract failed! \nThis website has Cloudflare defender, please change the access way.\n{self.url}'
            return f'Get abstract failed, please check tags of the website: {self.url}'
        else:
            return self.abstract_format(abstract=abstract)
        
    def over_five_wall(self) -> BeautifulSoup:
        '''
        Require FlareSolverr/FlareSolverr
        '''
        res = client.post(
            url=over_five_Wall_url, 
            json={
                    'cmd': 'request.get',
                    'url': self.url,
                    'session': 'five_wall',
                    'maxTimeout': 60000
                    }
            ).json()["solution"]["response"]
        return BeautifulSoup(res, features='html.parser')
    
    
    def aip(self) -> str:
        '''
        Database tag: AIP
        '''
        
        return self.abstract_find(attr_value='NLM_paragraph')

    
    def elsevier(self) -> str:
        '''
        Database tag: Elsevier
        '''
        
        return self.abstract_find(attr_value='abstract author', is_cloud=False)

    
    def iop(self) -> str:
        '''
        Database tag: IOP
        Notice! Proxy forbiden
        '''
        #return self.abstract_find(attr_value='article-text wd-jnl-art-abstract cf')
        return self.abstract_find(attr_value='article-text wd-jnl-art-abstract cf', is_cloud=True)

    
    def wiley(self) -> str:
        '''
        Database tag: Wiley
        Notice! Cloudflare Wall 
        '''
        return self.abstract_find(tag='section', attr_value='article-section article-section__abstract', is_cloud=True)


    def springer(self) -> str:
        '''
        Database tag: springer 
        '''
        return self.abstract_find(attr_value='c-article-section__content')


def get_abstract_google(artical_name: str) -> str:
    '''
    从谷歌学术获取英文摘要
    '''
    artical_name = str_replace([' '], artical_name, '+')
    artical_link = f'https://scholar.google.com/scholar?hl=zh-CN&as_sdt=0%2C5&q={artical_name}&btnG='
    scholar_result_soup = bs(artical_link)
    
    abstract = bs_find(scholar_result_soup, 'div', 'class', 'gs_rs').contents

    if not abstract:
        raise 
    
    abstract=''.join(i.string for i in abstract if i.string)
    
    return abstract

def get_abstract_baidu(name: str) -> str:
    '''
    从百度学术获取摘要
    '''
    name = str_replace([' '], name, '+')
    a = bs(f'https://xueshu.baidu.com/s?wd={name}')
    b = a.find('head').find('script').string

    p = re.compile(r"\('//(.*)'\);}").search(b)[1]
    time.sleep(3)
    c = bs('https://' + p)
    d = bs_find(c, 'p', 'class', 'abstract')
    return d.string


if __name__ == '__main__':
    ...
    print(get_abstract().get('wiley.....', 'https://onlinelibrary.wiley.com/doi/full/10.1002/eahr.500120', 'tag'))
