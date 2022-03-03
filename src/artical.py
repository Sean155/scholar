from typing import Dict
from get_abstract import get_abstract
from google_translator import google_translator

class abstrcat():
        
        def __init__(self):
            self.en: str = ''
            self.ch: str = ''
            
        def get(self, params: Dict[str, str]) -> None:
            
            try:
                name = params['name']
                database = params['database']
                url = params['url']
            except KeyError:
                raise 'Wrong params'
            
            self.en = get_abstract.get(database=database, url=url)
            
            self.ch = google_translator.trans(words=self.en) if len(self.en) > 50 else self.en


class artical(abstrcat):
    '''
    Artical 类
    
    文章的基本属性：
    Name, Doi, Url, Time, Journal, Database, Abstract...
    '''
    
    def __init__(self, params: Dict[str, str]):
            
        self.name: str = params['name']
        self.doi: str = params['doi']
        self.url: str = params['url']
        self.time: str = params['time']
        self.journal: str = params['journal']
        self.database: str = params['database']
    
    def get_abstract(self) -> 'artical':
        self.get(params={
            'name': self.name,
            'database': self.database,
            'url': self.url
        })
        return self

if __name__ == '__main__':
    a = artical(params={
        'name': 'test',
        'doi': 'doi',
        'url': 'url',
        'time': 'time',
        'journal': 'journal',
        'database': 'database'
    }).get_abstract()
    print(a.en, a.ch)
    
    
        
        