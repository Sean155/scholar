import re
from bs4 import BeautifulSoup
from bs4.element import PageElement
from typing import Any, List, Dict
from client import client

db_list = ['aip', 'elsevier', 'iop', 'wiley']

over_five_Wall_url = 'http://10.141.5.152:8191/v1'

is_proxy = False

class abstract():
    
    def __init__(self) -> None:
        self.url: str = ''
    
    def get(self, database: str, url: str, **kwargs) -> Any:
        '''
        Get abstract
        
        Database: Name of Inputed Database
        Url: Link of Artical
        
        Notice! IOP Seems Proxy Forbiden!
        '''
        for i in db_list:
            if re.match(i, database.lower()):
                self.url = url
                return getattr(self, i)
        raise 
    
    def abstract_fromat(self, abstract: List[PageElement]) -> str:
        p_abstract = ''
        for i in abstract:
            if i.string:
                if not re.match('Abstract', i.string):
                    p_abstract = p_abstract + i.string
            elif i.text:
                p_abstract = p_abstract + i.text
        return p_abstract
    
    
    def soup(self) -> BeautifulSoup:
        
        return BeautifulSoup(client.get(self.url, proxy=is_proxy).content, features="html.parser")
    
    def abstract_find(self, 
                      name: str = 'div', 
                      attr_name: str = 'class', 
                      attr_key: str = ..., 
                      is_cloud: bool = False) -> str:
        if is_cloud:
            res = self.over_five_wall()
        else:
            res = self.soup()
        print(res.contents)
        abstract = res.find(
            name,
            {
                attr_name: attr_key
            }
        ).contents
        
        return self.abstract_fromat(abstract=abstract)
        
    def over_five_wall(self):
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
    
    @property
    def aip(self) -> str:
        '''
        Database name: AIP
        '''
        
        return self.abstract_find(attr_key='NLM_paragraph')

    @property
    def elsevier(self) -> str:
        '''
        Database name: Elsevier
        '''
        
        return self.abstract_find(attr_key='abstract author')

    @property
    def iop(self):
        '''
        Database name: IOP
        Notice! Proxy forbiden
        '''
        return self.abstract_find(attr_key='article-text wd-jnl-art-abstract cf')

    @property
    def wiley(self):
        '''
        Database name: Wiley
        '''
        return self.abstract_find(attr_key='article-section__content en main', is_cloud=True)

if __name__ == '__main__':
    print(abstract().get('wiley.....', 'https://onlinelibrary.wiley.com/doi/full/10.1002/eahr.500120'))