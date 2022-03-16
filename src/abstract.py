import re
import time
from bs4 import BeautifulSoup
from bs4.element import PageElement
from typing import Any, List, Dict, Union
from .utils import client, Response, str_replace, bs, bs_find, config, ConnectTimeout, HTTPError
# import ptvsd

db_list = ['aip', 'elsevier', 'wiley', 'springer']

# ptvsd.debug_this_thread()
class get_abstract():
    '''
        :说明:
          提供获取论文摘要的方法
          
          ``get_abstract.statu``若为``False``则表示获取摘要属性失败
        
          ``get_abstract.text``: 获取摘要失败的反馈
    '''
    def __init__(self, url: str) -> None:
        self.url: str = url
        self.text: str = None
        self.statu: bool = True
    
    
    def get(self, database: str, name: str, year: str) -> 'get_abstract':
        '''
            :说明:
              获取摘要
              
            :参数:
              * ``database: str``: 数据库
              * ``name: str``: 论文标题
              * ``year: str``: 论文发表年份
        '''
        for i in db_list:
            if re.match(i, database.lower()):
                self.text = getattr(self, i)()
                return self
        try:
            self.text = get_abstract_baidu(name+' '+year) + 'BD'
        except:
            try:
                self.text = get_abstract_google(name+' '+year) + 'GG'
            except:
                self.statu = False
                self.text = f'Failed to get abstract from google scholar, baidu scholar.'
        return self
    
    
    def abstract_format(self, abstract: List[PageElement]) -> str:
        '''
            格式化摘要文本
        '''
        p_abstract = ''
        for i in abstract:
            if i:
                if i.string:
                    if not re.match('Abstract', i.string):
                        p_abstract = p_abstract + i.string
                elif i.text:
                    p_abstract = p_abstract + i.text
        return p_abstract
    
    
    def five_wall_check(self, res: Response) -> bool:
        '''
            检测是否5s墙
        '''
        if re.search('Please allow up to 5 seconds', res.text):
            return True
        return False
    
    
    def abstract_find(self, 
                      tag: str = 'div', 
                      attr_key: str = 'class', 
                      attr_value: str = ..., 
                      is_cloud: bool = False) -> str:
        '''
            搜索摘要文本
        '''
        if is_cloud:
            try:
                res = self.over_five_wall()
            except ConnectTimeout as e:
                self.statu = False
                return f'Get abstract timeout, please check your FlareSolverr serve.\n {e.args}'
        else:
            try:
                res = bs(self.url)
            except HTTPError as e:
                self.statu = False
                return f'Get abstract failed, please check your Internet.\n {e.args}'
     
        try:
            abstract = bs_find(res, tag, attr_key, attr_value).contents
        except:
            self.statu = False
            if self.five_wall_check(res):
                return f'Get abstract failed! \nThis website may have Cloudflare defender, please change the access way.\n{self.url}'
            return f'Get abstract failed, please check html tags of the website: {self.url}'
        else:
            return self.abstract_format(abstract=abstract)
        
        
    def over_five_wall(self) -> BeautifulSoup:
        '''
            绕过5s墙, 依赖于: 
            
            FlareSolverr/FlareSolverr
        '''
        res = client.post(
            url = config.over_five_wall_url, 
            json={
                    'cmd': 'request.get',
                    'url': self.url,
                    'session': config.session,
                    'maxTimeout': 60000
                    }
            ).json()["solution"]["response"]
        return BeautifulSoup(res, features='html.parser')
    
    
    def aip(self) -> str:
        '''
            数据库: AIP
        '''
        
        return self.abstract_find(attr_value='NLM_paragraph', is_cloud=True)

    
    def elsevier(self) -> str:
        '''
            数据库: Elsevier
        '''

        if config.elsevier_api_key:
            pii = re.search(r'pii/(.*)', self.url)[1]
            res = client.get_with_headers(
                        url = f'https://api.elsevier.com/content/article/pii/{pii}?view=META_ABS',
                        headers={
                            'Accept': 'application/json',
                            'X-ELS-APIKey': config.elsevier_api_key,
                        }
            )
            text = res.json()['full-text-retrieval-response']['coredata']['dc:description']
            text = str_replace(['   '], text, '')
            return text + '    from api'
        else:
            return self.abstract_find(attr_value='abstract author', is_cloud=False)

    
    def iop(self) -> str:
        '''
            数据库: IOP
            
            可能禁止代理访问
        '''
        #return self.abstract_find(attr_value='article-text wd-jnl-art-abstract cf')
        return self.abstract_find(attr_value='article-text wd-jnl-art-abstract cf', is_cloud=True)

    
    def wiley(self) -> str:
        '''
            数据库: Wiley
            
            存在5s墙
        '''
        try:
            doi = re.search(r'abs/(.*)', self.url)[1]
            doi = '%22' + str_replace(['/'], doi, '%2F') + '%22'
            res = client.get_no_headers(
                        url = f'https://onlinelibrary.wiley.com/action/sru?query=dc.identifier%3D{doi}',
                    )
            res = BeautifulSoup(res, features='html.parser')
            return res.find('dc:description').string + '    from api'
        except:
            return self.abstract_find(tag='section', attr_value='article-section article-section__abstract', is_cloud=True)


    def springer(self) -> str:
        '''
            数据库: springer 
        '''
        if config.springer_api_key:
            doi = re.search(r'article/(.*)', self.url)[1]
            res = client.get_with_headers(
                        url = f'https://api.springernature.com/metadata/json/doi/{doi}?api_key={config.springer_api_key}'
                )
            return res.json()['records'][0]['abstract'] + '     from api'
        else:
            return self.abstract_find(attr_value='c-article-section__content')


def get_abstract_google(article_name: str) -> str:
    '''
        从谷歌学术获取英文摘要
    '''
    article_name = str_replace([' '], article_name, '+')
    article_link = config.scholar_link + '/scholar?hl=zh-CN&as_sdt=0%2C5&q={article_name}&btnG='
    scholar_result_soup = bs(article_link)
    
    abstract = bs_find(scholar_result_soup, 'div', 'class', 'gs_rs').contents

    if not abstract:
        raise 
    
    abstract=''.join(i.string for i in abstract if i if i.string)
    
    return abstract


def get_abstract_baidu(article_name: str) -> str:
    '''
        从百度学术获取摘要
    '''
    article_name = str_replace([' '], article_name, '+')
    
    res = client.post(
            url = config.over_five_wall_url, 
            json={
                    'cmd': 'request.get',
                    'url': f'https://xueshu.baidu.com/s?wd={article_name}',
                    'session': config.session,
                    'maxTimeout': 60000
                    }
            ).json()["solution"]["response"]
    
    a = BeautifulSoup(res, features='html.parser')
    b = a.find('head').find('script').string

    p = re.compile(r"\('//(.*)'\);}").search(b)[1]
    time.sleep(1)
    
    res2 = client.post(
            url = config.over_five_wall_url, 
            json={
                    'cmd': 'request.get',
                    'url': 'https://' + p,
                    'session': config.session,
                    'maxTimeout': 60000
                    }
            ).json()["solution"]["response"]
    
    c = BeautifulSoup(res2, features='html.parser')
    d = bs_find(c, 'p', 'class', 'abstract')
    #ptvsd.debug_this_thread()
    return d.string


if __name__ == '__main__':
    ...
    print(get_abstract().get('wiley.....', 'https://onlinelibrary.wiley.com/doi/full/10.1002/eahr.500120', 'tag'))
