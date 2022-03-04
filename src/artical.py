from typing import Dict, Tuple
from pydantic import BaseModel, ValidationError
from get_abstract import get_abstract
from google_translator import google_translator
import time 

class Artical(BaseModel):
    '''
    Artical 类
    
    文章的基本属性：
    Author, Name, Url, Time, Journal, Database...
    '''
    author: str
    name: str
    url: str
    year: str
    journal: str
    database: str

    def abstract(self) -> Tuple[str, str]:
        '''
        获取摘要并翻译
        '''
        abstract_res = get_abstract(url=self.url).get(database=self.database, name=self.name)
        en = abstract_res.text
        
        if abstract_res.statu:
            ch = google_translator.trans(words=en)
        else:
            ch = en
        return en, ch

def get_artical(params: Dict[str, str]) -> 'Artical':
    '''
    初始化 Artical 类
    
    params:
    {
        'author': value,
        'name': value, 
        'url': value, 
        'year': value, 
        'journal': value, 
        'database': value
    }
    '''
    
    try:
        return Artical.parse_obj(params)
    except ValidationError as e:
        print(f'Wrong params:{params}')
        print(f'{e.errors()}')
    raise ValueError('Falied to initalize class Artical')

if __name__ == '__main__':
    print(time.localtime())
    a = get_artical({
        'name': 'name1',
        'url': 'https://onlinelibrary.wiley.com/doi/full/10.1002/er.5313',
        'time': 'time1',
        'journal': 'journal1',
        'database': 'Wiley Online Library'
    })
    en, ch = a.abstract()
    print(time.localtime())
    print(en, ch)
