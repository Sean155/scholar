from pydantic import BaseSettings


class Config(BaseSettings):
    
    over_five_wall_url: str = 'http://10.141.5.152:8191/v1'
    session: str = 'cloudflare_wall'
    
    proxies: str = 'http://127.0.0.1:7890'
    proxy_statu: bool = True
    
    scholar_link: str = 'https://scholar.google.com/'
    
    #谷歌学术https://scholar.google.com/
    #谷歌学术镜像https://xs2.dailyheadlines.cc/
    #谷歌学术镜像https://scholar.lanfanshu.cn/
    #谷歌学术镜像https://xs.dailyheadlines.cc/

    class Config:
        extra = "ignore"
