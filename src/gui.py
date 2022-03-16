import sys
import time
from PyQt5.QtWidgets import QMainWindow, QTableWidget, QTableWidgetItem, QApplication, QFileDialog,QMessageBox, QInputDialog
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from typing import List, Tuple, Dict, Optional, Union
from PyQt5 import QtCore, QtGui, QtWidgets
from .google_scholar import get_scholar, Scholar, Article
from .utils import save_file
from .main_gui import *
#import ptvsd

class Thread1(QThread):
    send_scholar = pyqtSignal(Scholar)
    def __init__(self, key_words: str, article_num: str) -> None:
        self.key_words, self.article_num = key_words, article_num
        super().__init__()
    
    def run(self) -> None:
        #ptvsd.debug_this_thread()
        scholar = get_scholar(self.key_words, self.article_num)
        self.send_scholar.emit(scholar)
        
        
class Thread2(QThread):
    send_article_database = pyqtSignal(dict)
    send_reflash_main = pyqtSignal(float)
    def __init__(self, schloar: Scholar, article_num: int, article_datebase: Dict) -> None:
        self.scholar, self.article_num, self.article_datebase = schloar, article_num, article_datebase
        super().__init__()
    
    
    #这里有问题！！！！！！！！！！！不能这样写，可能要改成数字！！！！！
    def run(self):
        i = self.article_num
        max = self.scholar.items + i
        for j in range(self.article_num, max):
            if not self.article_datebase.__contains__(str(j)):
                x = self.scholar.article[j - 1]
                self.article_datebase[str(j)] = [x, x.abstract()]
            self.article_datebase['statu'] -= 1
            self.send_reflash_main.emit(j/self.scholar.items)
            time.sleep(4)
        self.send_article_database.emit(self.article_datebase)     
    
    
class main_w2(QMainWindow, Ui_MainWindow):

    def __init__(self, session_error: Union[str, None]):
        super().__init__()
        self.setupUi(self)
        self.download.clicked.connect(lambda :self.Download(self.num_gui.toPlainText()))
        self.search.clicked.connect(lambda :self.Search(self.keyword1.toPlainText()))
        self.up.clicked.connect(lambda :self.Up(self.keyword1.toPlainText(),self.num_gui.toPlainText()))
        self.next.clicked.connect(lambda :self.Next(self.keyword1.toPlainText(),self.num_gui.toPlainText()))
        self.go.clicked.connect(lambda :self.Go(self.keyword1.toPlainText(),self.num_gui.toPlainText()))
        self.button_is_close = False
        self.scholar : Scholar
        self.article_datebase: Dict[str, Union[List[Article, Tuple[str, str]], int]] = {}
        self.error_msg = session_error
    
    
    def loading(self, article_num: int) -> None:
        '''
        缓存摘要
        '''
        def reflash(statu: float, self=self):
            self.progressBar.setValue(int(statu*100))
            QApplication.processEvents()
        
        def save_article_datebase(article_datebase: Dict, self=self):
            self.article_datebase = article_datebase
            self.redisplay(article_num)
            self.button_is_close = False
            self.button_statu()

        self.results_gui.setText(str(self.scholar.search_result_nums))
        item_list = [str(i) for i in range(1, self.article_datebase['statu'] + 1)]
        items, ok = self.msg(item_list)
        if ok:
            self.button_is_close = True
            self.button_statu()
            if self.scholar.items > int(items):
                self.scholar.items = int(items)
            self.thread2 = Thread2(self.scholar, article_num, self.article_datebase)
            self.thread2.send_reflash_main.connect(reflash)
            self.thread2.send_article_database.connect(save_article_datebase)
            self.thread2.start()                  
            

    def button_statu(self) -> None:
        '''
        改变按钮状态
        '''
        self.download.setDisabled(self.button_is_close)
        self.search.setDisabled(self.button_is_close)
        self.up.setDisabled(self.button_is_close)
        self.next.setDisabled(self.button_is_close)
        self.go.setDisabled(self.button_is_close)
    

    def redisplay(self, article_num: int) -> None:
        '''
        根据论文号更新显示文献名、中英文摘要、第几篇文献、期刊、年份、数据库、作者
        '''
        a = self.article_datebase[str(article_num)][0]
        article_abstract = self.article_datebase[str(article_num)][1]
        self.article_name.setText(a.name)
        self.Abstract_1.setText(article_abstract[0])
        self.Abstract_2.setText(article_abstract[1])
        self.num_gui.setPlainText(str(article_num))
        self.journal_gui.setPlainText(a.journal)
        self.year_gui.setText(a.year)
        self.datebase_gui.setPlainText(a.database)
        self.author_gui.setPlainText(a.author)


    def Download(self, article_num):
        '''
        定义下载按钮
        '''
        a = self.article_datebase[article_num][0]
        name = a.name
        fname, _ = QFileDialog.getSaveFileName(self, 'save file', name)
        saved = save_file(a.url, fname)
        if saved:
            print("download successful")
        else:
            print("download failed")
 
    
    def Search(self, key_words: str) -> None:
        '''
        定义搜索按钮
        '''
        def save_scholar(scholar: Scholar, self: 'main_w2'=self):
            self.scholar = scholar
            self.article_datebase['statu'] = self.scholar.items
            if self.scholar.statu:
                self.loading(1)
            else:
                self.Abstract_1.setText(self.scholar.text)
        
        if self.error_msg:
            self.error()
            QApplication.quit()
        
        self.search.setDisabled(True)
        self.scholar = ''
        self.article_num_old = 1
        self.thread = Thread1(key_words, '1')
        self.thread.send_scholar.connect(save_scholar)
        self.thread.start()
    

    def Up(self,key_words: str,article_num: str) -> None :
        '''
        定义上按钮
        '''
        self.up.setDisabled(True)
        article_num= int(article_num) - 1
        if article_num > 0:
            if not self.article_datebase.get(str(article_num)):
                pass
            else:
                self.redisplay(article_num)
                self.button_is_close = False
                self.button_statu()


    def Next(self,key_words: str, article_num: str) -> None:
        '''
        定义下按钮
        '''
        self.next.setDisabled(True)
        self.article_num_old = int(article_num)
        article_num = int(article_num) + 1
        self.check_get_scholar(key_words, article_num)


    def Go(self,key_words: str, article_num: str):
        '''
        定义跳转按钮
        '''
        self.go.setDisabled(True)
        article_num = int(article_num)
        self.article_datebase['statu'] = self.article_datebase['statu'] - (article_num - self.article_num_old) + 1
        self.article_num_old = int(article_num)
        self.check_get_scholar(key_words, article_num)


    def check_get_scholar(self, key_words: str, article_num: int) -> None:
        if not self.article_datebase.get(str(article_num)):
            if self.article_datebase['statu'] <= 0: 
                self.scholar = ''
                self.scholar = get_scholar(key_words, str(article_num))
                self.article_datebase['statu'] = self.scholar.items
            if self.scholar.statu:
                self.loading(article_num)
            else:
                self.Abstract_1.setText(self.scholar.text)
        else:
            self.redisplay(article_num)
            self.button_is_close = False
            self.button_statu()


    def msg(self, items: List[str]):
        items = tuple(items)
        item, ok = QInputDialog.getItem(self, 'Tip', '缓存数量', items, 0, False)
        return item, ok


    def error(self):
        QMessageBox.warning(self, 'Error!', self.error_msg, QMessageBox.StandardButton.Yes)


#导入数据库,并存为data
    def opendata(self):
        fname = QFileDialog.getOpenFileName(self, 'Open data', '.')
        try:
            with open(fname[0], 'r', encoding='UTF-8')as f:
                startdata = f.read()
                self.getalldata(startdata)
                QMessageBox.about(self, '提示', '成功导入...')
        except:
            QMessageBox.about(self, '警告', '导入失败！')


if __name__ == "__main__":
    app = QApplication(sys.argv)
    gui = main_w2()
    gui.show()
    sys.exit(app.exec_())
