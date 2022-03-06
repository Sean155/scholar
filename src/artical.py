from typing import Dict, Tuple
from pydantic import BaseModel, ValidationError
from abstract import get_abstract
from google_translator import google_translator
import time 

class Artical(BaseModel):
    '''
    Artical 类
    
    文章的基本属性：
    Author, Name, Url, Time, Journal, Database...
    
    statu: 若为False则表示获取基本属性失败
    
    text: 获取基本属性失败时反馈内容
    '''
    author: str
    name: str
    url: str
    year: str
    journal: str
    database: str
    statu: bool
    text: str
    
    def abstract(self) -> Tuple[str, str]:
        '''
        获取摘要并翻译
        '''
        if not self.statu:
            return self.text, self.text
        
        abstract_res = get_abstract(self.url).get(self.database, self.name, self.year)
        en = abstract_res.text 
        
        if abstract_res.statu:
            ch = google_translator.trans(words=en) + f'\nurl: {self.url}'
        else:
            ch = en + f'\nurl: {self.url}'
        return en, ch

def get_artical(params: Dict[str, str]) -> 'Artical':
    '''
    初始化 Artical 类
    
    params = {
        
        'author': value,
        'name': value, 
        'url': value, 
        'year': value, 
        'journal': value, 
        'database': value,
        'statu': True | False,
        'text': value
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
        'name1': 'name1',
        'url': 'https://onlinelibrary.wiley.com/doi/full/10.1002/er.5313',
        'time': 'time1',
        'journal': 'journal1',
        'database': 'Wiley Online Library',
        'statu': True,
        'text': ''
    })
    en, ch = a.abstract()
    print(time.localtime())
    print(en, ch)
