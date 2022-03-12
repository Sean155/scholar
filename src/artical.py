from typing import Dict, Tuple
from pydantic import BaseModel, ValidationError
from .abstract import get_abstract
from .google_translator import google_translator
import time 


class Artical(BaseModel):
    '''
        :说明:
          枚举论文的基本属性：
          ``author``, ``name``, ``url``, ``year``, ``journal``, ``database``, 
          
          提供``abstract``方法获取当前论文的摘要及反应
    
          ``Artical.statu``若为``False``则表示获取论文基本属性失败
        
          ``Artical.text``: 获取基本属性失败的反馈
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
            :说明:
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
        :说明:
          初始化 Artical 类
          
        :参数:
          * ``params: Dict[str, str]``: 论文基本信息
          
            params = {
        
                    'author': str,
                    'name': str, 
                    'url': str, 
                    'year': str, 
                    'journal': str, 
                    'database': str,
                    'statu': True | False,
                    'text': str | None
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
