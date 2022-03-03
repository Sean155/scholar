from client import client
from typing import Dict, List

is_proxy = False

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
    
    
    def trans(self, words: str = ..., s_: str = 'auto', t_: str = 'zh-CN') -> str:
        '''
        调用谷歌翻译api
        words: 待翻译内容
        s_: 源语言，默认auto
        t_: 目标语言，默认zh-CN
        '''
        return self._trans(words, s_, t_)
    
    def _trans(self, words: str, s_: str, t_: str) -> str:
        
        if len(words) > 4000:
            return 'Too long to trans'
        trans_result = client.get(url=self.api_url.format(self.s_lan(s_), self.t_lan(t_), words), proxy=is_proxy)
        if trans_result.json():
            return self._json(trans_result.json())
        else:
            return trans_result.text
        

if __name__ == '__main__':
    t = google_translator()
    '''t.proxies = {
        "http": "127.0.0.1",
        "port": "7890"
    }'''
    x = t.trans("AFRIMETS.EM-S1 supplementary comparison on resistance standards at 1 Ω, 10 Ω, 100 Ω, 1 kΩ and 10 kΩ commenced November 2015 and ended June 2018. The comparison approved by AFRIMETS technical committee for Electricity and Magnetism (TC-EM) and Consultative Committee for Electricity and Magnetism (CCEM). Seven National Metrology Institutes participated including National Metrology Institute of South Africa (NMISA)the pilot laboratory. The primary objective of the comparison is aimed to underpin and strengthen the capabilities of the National Metrology Institutes and establish the degree of equivalence and comparability. The results of the participants are found to be equivalent, comparable and in agreement with the comparison reference values within stated uncertainties of measurements.To reach the main text of this paper, click on Final Report. Note that this text is that which appears in Appendix B of the BIPM key comparison database https://www.bipm.org/kcdb/.The final report has been peer-reviewed and approved for publication by the CCEM, according to the provisions of the CIPM Mutual Recognition Arrangement (CIPM MRA)")
    print(x)