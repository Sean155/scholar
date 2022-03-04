import re
from bs4 import BeautifulSoup
from bs4.element import PageElement
from typing import Any, List, Dict, Union
from client import client, Response

s = client()

db_list = ['aip', 'elsevier', 'iop', 'wiley']

over_five_Wall_url = 'http://10.141.5.152:8191/v1'

class get_abstract():
    
    def __init__(self, url: str) -> None:
        self.url: str = url
        self.text: str = None
        self.statu: bool = True
    
    
    def get(self, database: str, name: str) -> 'get_abstract':
        '''
        Get abstract
        
        Database: Name of Inputed Database
        Url: Link of Artical
        
        Notice! IOP Seems Proxy Forbiden!
        '''
        for i in db_list:
            if re.match(i, database.lower()):
                self.text = getattr(self, i)()
                return self
        self.text = get_abstract_google(name)
        return self
    
    def abstract_format(self, abstract: List[PageElement]) -> str:
        p_abstract = ''
        for i in abstract:
            if i.string:
                if not re.match('Abstract', i.string):
                    p_abstract = p_abstract + i.string
            elif i.text:
                p_abstract = p_abstract + i.text
        return p_abstract
    
    
    def soup(self) -> BeautifulSoup:

        return BeautifulSoup(client.get(self.url).content, features="html.parser")
    
    def five_wall_check(self, res: Response) -> bool:
        
        if re.search('Please allow up to 5 seconds', res.text):
            return True
        return False
    
    def abstract_find(self, 
                      name: str = 'div', 
                      attr_name: str = 'class', 
                      attr_key: str = ..., 
                      is_cloud: bool = False) -> str:
        if is_cloud:
            res = self.over_five_wall()
        else:
            res = self.soup()
        try:
            abstract = res.find(
                name,
                {
                    attr_name: attr_key
                }
            ).contents
        except:
            self.statu = False
            if self.five_wall_check(res):
                return f'Get abstract failed! \nThis website has Cloudflare defender, please change the access way.\n{self.url}'
            return f'Get abstract failed, please check tags of the website: {self.url}'
        else:
            return self.abstract_format(abstract=abstract)
        
    def over_five_wall(self) -> BeautifulSoup:
        '''
        Use FlareSolverr/FlareSolverr
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
        Database name: AIP
        '''
        
        return self.abstract_find(attr_key='NLM_paragraph')

    
    def elsevier(self) -> str:
        '''
        Database name: Elsevier
        '''
        
        return self.abstract_find(attr_key='abstract author')

    
    def iop(self) -> str:
        '''
        Database name: IOP
        Notice! Proxy forbiden
        '''
        #return self.abstract_find(attr_key='article-text wd-jnl-art-abstract cf')
        return self.abstract_find(attr_key='article-text wd-jnl-art-abstract cf', is_cloud=True)

    
    def wiley(self) -> str:
        '''
        Database name: Wiley
        Notice! Cloudflare Wall 
        '''
        return self.abstract_find(name='section', attr_key='article-section article-section__abstract', is_cloud=True)

def str_repalce(char_list: List[str], string: str, re_string: str) -> str:
    '''
    替换字符
    '''
    for i in char_list:
        string = string.replace(i, re_string)
    return string

#获取摘要
def get_abstract_google(artical_name: str) -> str:
    '''
    从谷歌获取英文摘要
    '''
    artical_name = str_repalce([' '], artical_name, '+')
    artical_link = f'https://scholar.google.com/scholar?hl=zh-CN&as_sdt=0%2C5&q={artical_name}&btnG='
    scholar_result_soup = BeautifulSoup(s.get(artical_link).content, features="html.parser")
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

if __name__ == '__main__':
    ...
    print(get_abstract().get('wiley.....', 'https://onlinelibrary.wiley.com/doi/full/10.1002/eahr.500120', 'name'))
