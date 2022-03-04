from httpx import Client, Response
from typing import Dict

class client():
    
    def __init__(self):

        self.headers: Dict = {
                "User-Agent": 'Mozilla/5.0 (iPhone; CPU iPhone OS 14_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.1.1 Mobile/15E148 Safari/604.1',
                "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
                }
        self.proxies: str = "http://127.0.0.1:7890"
    
    @classmethod
    def get(cls, url: str, proxy: bool = True) -> Response:
        
        api = cls().call(proxy=proxy)
        
        res = api.get(url=url, timeout=20)
        api.close()
        return res
    
    @classmethod
    def post(cls, url: str, json: Dict, proxy: bool = True) -> Response:
        
        api = cls().call(proxy=proxy)
        res = api.post(url=url, json=json, timeout=20)
        api.close()
        return res
    
    def call(self, proxy: bool) -> Client:
        if proxy:
            return Client(proxies=self.proxies, headers=self.headers)
        return Client(headers=self.headers)
