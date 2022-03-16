from .utils import client
from typing import Dict, List


class google_translator():


    def __init__(self) -> None:
        
        self.api_url = 'https://translate.googleapis.com/translate_a/single?client=gtx&sl={}&tl={}&dt=t&q={}&ie=UTF-8&oe=UTF-8'

    
    def s_lan(self, lan: str = ..., **kwargs) -> str:
        '''
            源语言
        '''
        if lan not in ['auto', 'en', 'ja', 'ru']:
            raise
        return lan
    
    
    def t_lan(self, lan: str = ..., **kwargs) -> str:
        '''
            目标语言
        '''
        if lan not in ['zh-CN', 'en', 'ja', 'ru']:
            raise
        return lan
    
    
    def _json(self, results: List, **kwargs) -> str:
        res = ''
        for i in results[0]:
            res = res + i[0]
        return res
    
    
    @classmethod
    def trans(cls, words: str = ..., s_: str = 'auto', t_: str = 'zh-CN') -> str:
        '''
            调用谷歌翻译api
            
            ``words: srt``: 待翻译内容
            ``s_: str``: 源语言, 默认auto
            ``t_: str``: 目标语言, 默认zh-CN
        '''
        return cls()._trans(words, s_, t_)
    
    
    def _trans(self, words: str, s_: str, t_: str) -> str:
        
        if len(words) > 4000:
            return 'Too long to trans'
        url=self.api_url.format(self.s_lan(s_), self.t_lan(t_), words)
        trans_result = client.get(url=url)
        try:
            return self._json(trans_result.json())
        except:
            return trans_result.text
        

if __name__ == '__main__':
    t = google_translator()
    x = t.trans("supplementary comparison on resistance standards at")
    print(x)
