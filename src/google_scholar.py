from bs4 import BeautifulSoup
from utils import bs_find, str_replace, bs, T
from typing import List, Tuple, Dict
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
    
    def search_results(self, key_words: str, search_page: str) -> 'Scholar':
        '''
        获取搜索结果
        
        返回一页（20条）结果
        '''
        artical_num = (int(search_page)-1)*20
        key_words = str_replace([' '], key_words, '+')
        scholar_link = f'https://scholar.google.com/scholar?start={search_page}&q={key_words}&hl=zh-CN&num=20&as_sdt=0,5'
        
        
        scholar_result_soup = bs(scholar_link)
        
        try:
            bs_find(scholar_result_soup, 'div', 'class', 'gs_res_ccl')
        except:
            self.statu = False
            self.text = 'Failed to get results from google scholar, please check the Internet.'
            return self
        
        self.search_result_nums = self.get_result_nums(scholar_result_soup)
        
        for i in range(artical_num, artical_num + 20):
            artical_info_all = bs_find(scholar_result_soup, 'div', ['class', 'data-rp'], ['gs_r gs_or gs_scl', i])
            
            info = self.get_artical_base_info(artical_info_all)
            info['name'], info['url'] = self.get_artical_name_url(artical_info_all)
            
            self.artical.append(get_artical(info))
            
        return self
    
    
    def get_artical_base_info(self, artical_info_all: T) -> Dict:
        '''
        获取文章基本属性：
        
        作者、年份、期刊、数据库
        '''
        artical_time = bs_find(artical_info_all, 'div', 'class', 'gs_a').contents
        artical_time = ''.join(i.string for i in artical_time)
        
        return self.format_base_info(artical_time)
            
    def get_result_nums(self, scholar_result_soup: BeautifulSoup) -> int:
        '''
        获取搜索结果条目数
        '''
        try:
            search_result_nums = bs_find(scholar_result_soup, 'div', 'class', 'gs_ab_mdw').contents
            search_result_nums = re.compile(r'约\s(.*)\s条').search(search_result_nums)
        except:
            return 1
        
        return int(str_replace([','], search_result_nums, ''))
    
    def get_artical_name_url(self, artical_info_all: T) -> Tuple[str, str]:
        '''
        获取文章标题、链接
        '''        
        artical_name = bs_find(artical_info_all, 'div', 'class', 'gs_ri')
        artical_name = artical_name.find('a')
        name = ''.join(i.string for i in artical_name.contents)
        name = str_replace(['/', '\\', ':', '*', '"', '?', '>', '<', '|'], name,'_')
        url = artical_name.attrs["href"]
        
        return name, url
    
    def format_base_info(string: str) -> Dict:
        '''
        格式化文章基本属性
        '''
        partern = re.compile(r'(.*)\s-\s(.*)\s-\s(.*)')

        res = partern.search(string)
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
            'database': database
        }


def get_scholar(key_words: str, search_page: str) -> 'Scholar':
    '''
    初始化 Scholar 类
    '''
    return Scholar().search_results(key_words, search_page)

if __name__ == '__main__':
    a = get_scholar('thermal', 3)
    en, ch = a.artical[0].abstract()
    nums = a.search_result_nums
    print(en, ch)
