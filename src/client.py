from httpx import Client, Response
from typing import Dict

class client():
    
    def __init__(self, proxy: bool = False) -> None:
        self.client = Client
        self.headers: Dict = {
                "User-Agent": 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:98.0) Gecko/20100101 Firefox/98.0',
                #"Accept-Language": "zh-cn",
                "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
                }
        self.proxies_: bool = proxy
        if not self.proxies_:
            self.proxies: str = None
        else:
            self.proxies: str = "http://127.0.0.1:7890"
    
    @classmethod     
    def get(cls, url: str, proxy: bool) -> Response:
        
        return cls(proxy=proxy)._get(url=url)
    
    @classmethod
    def post(cls, url: str, json: Dict, proxy: bool) -> Response:
        
        return cls(proxy=proxy)._post(url=url, json=json)
    
    def _get(self, url: str, **kwargs) -> Response:
        
        if self.proxies:
            api = self.client(proxies=self.proxies, headers=self.headers)
        else:
            api = self.client(headers=self.headers)
        res = api.get(url=url, timeout=20)
        api.close()
        return res

    def _post(self, url: str, json: Dict) -> Response:
        
        if self.proxies:
            api = self.client(proxies=self.proxies)
        else:
            api = self.client()
        res = api.post(url=url, json=json)
        api.close()
        
        return res
    
    
