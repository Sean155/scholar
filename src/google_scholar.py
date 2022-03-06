from bs4 import BeautifulSoup
from utils import bs_find, str_replace, bs, T
from typing import List, Tuple, Dict, Union
import re
from artical import get_artical, Artical


class Scholar():
    '''
    Scholar 类
    
    获取谷歌学术搜索的结果、整合文章信息
    
    类变量：
    
    search_result_nums：
    结果条目数
    
    artical：
    一页搜索结果的 Artical 类列表
    
    statu:
    搜索状态，若为False，则搜索失败
    '''
    
    search_result_nums: int
    artical: List[Artical] = []
    statu: bool = True
    text: str = ''
    
    def search_results(self, key_words: str, artical_num: str) -> 'Scholar':
        '''
        获取搜索结果
        
        返回一页（10条）结果
        '''
        artical_num = (int(artical_num)-1)
        key_words = str_replace([' '], key_words, '+')
        scholar_link = f'https://scholar.google.com/scholar?start={artical_num}&q={key_words}&hl=zh-CN&as_sdt=0,5' 
        #谷歌学术镜像https://xs2.dailyheadlines.cc/scholar?start={artical_num}&q={key_words}&hl=zh-CN&as_sdt=0,5
        #https://scholar.google.com/scholar?start={artical_num}&q={key_words}&hl=zh-CN&as_sdt=0,5
        #https://scholar.lanfanshu.cn/
        #https://xs.dailyheadlines.cc/
        scholar_result_soup = bs(scholar_link)
        
        if not bs_find(scholar_result_soup, 'div', 'id', 'gs_res_ccl'):
            self.statu = False
            self.text = f'Failed to get results from google scholar, please check the Internet.:\n{scholar_result_soup.text}'
            return self
        
        self.search_result_nums = self.get_result_nums(scholar_result_soup)
        self.artical = []
        for i in range(artical_num, artical_num + 10):
            artical_info_all = bs_find(scholar_result_soup, 'div', ['class', 'data-rp'], ['gs_r gs_or gs_scl', i])
            info = self.get_artical_base_info(artical_info_all)
            name, url, statu, text = self.get_artical_name_url(artical_info_all)
            info['name'] = name
            info['url'] = url
            info['text'] += text
            info['statu'] = statu if info['statu'] else False

            self.artical.append(get_artical(info))
            
        return self
    
    
    def get_artical_base_info(self, artical_info_all: T) -> Dict:
        '''
        获取文章基本属性：
        
        作者、年份、期刊、数据库
        '''
        artical_time = bs_find(artical_info_all, 'div', 'class', 'gs_a').contents
        artical_time = ''.join(i.string for i in artical_time if i)
        
        return self.format_base_info(artical_time)
            
    def get_result_nums(self, scholar_result_soup: BeautifulSoup) -> int:
        '''
        获取搜索结果条目数
        '''
        search_result_nums = bs_find(scholar_result_soup, 'div', 'id', 'gs_ab')
        
        try:
            search_result_nums = bs_find(search_result_nums, 'div', 'id', 'gs_ab_md')
            search_result_nums = bs_find(search_result_nums, 'div', 'class', 'gs_ab_mdw')
            search_result_nums = search_result_nums.contents
        except AttributeError:
            return 1
        else:
            search_result_nums = ''.join(i.string for i in search_result_nums if i)
            search_result_nums = re.compile(r'约\s(.*)\s条').search(search_result_nums)
        
        return int(str_replace([','], search_result_nums[1], ''))
    
    def get_artical_name_url(self, artical_info_all: T) -> Tuple[str, Union[str, None], bool, str]:
        '''
        获取文章标题、链接
        '''        
        artical_name = bs_find(artical_info_all, 'h3', 'class', 'gs_rt')
        
        name = artical_name.text
        #name = ''.join(i.string for i in artical_name.contents if i)
        name = str_replace(['/', '\\', ':', '*', '"', '?', '>', '<', '|'], name,'_')
        name = str_replace(['[图书][B] ', '[引用][C] ', '[HTML][HTML] '], name,'')
        artical_url = artical_name.find('a')
        try:
            url = artical_url.attrs["href"]
            statu = True
            text = ''
        except:
            statu = False
            text = f'Failed to get url: {name}\n'
            url = None
        return name, url, statu, text
    
    def format_base_info(self, string: str) -> Dict:
        '''
        格式化文章基本属性
        '''
        partern = re.compile(r'(.*)\s-\s(.*)\s-\s(.*)')

        res = partern.search(string)
        if not res:
            return {
                'author': 'None',
                'year': 'None',
                'journal': 'None',
                'database': 'None',
                'statu': False,
                'text': f'Failed to get base info: {string}\n'
            }
        author = res[1]
        year = res[2]
        database = res[3]
        if re.search(',', year):
            p = re.compile(r'(.*),\s(.*)')
            res_p = p.search(year)
            journal = res_p[1]
            year = res_p[2]
        else:
            journal = 'book'
        return {
            'author': author,
            'year': year,
            'journal': journal,
            'database': database,
            'statu': True,
            'text': ''
        }


def get_scholar(key_words: str, search_page: str) -> 'Scholar':
    '''
    初始化 Scholar 类
    '''
    return Scholar().search_results(key_words, search_page)

if __name__ == '__main__':
    a = get_scholar('thermal', 2)
    #en, ch = a.artical[0].abstract()
    #nums = a.search_result_nums
    pass
    #print(en, ch)
