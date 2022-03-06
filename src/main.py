from PyQt5.QtWidgets import QMainWindow, QTableWidget, QTableWidgetItem, QApplication, QFileDialog,QMessageBox, QInputDialog
from PyQt5.QtGui import *
from PyQt5.QtCore import *
import sys
import time
from typing import List, Tuple, Dict
from PyQt5 import QtCore, QtGui, QtWidgets
from google_scholar import get_scholar, Scholar
from utils import save_file
from typing import Optional
from mainwindow import *

class Thread1(QThread):
    send_scholar = pyqtSignal(Scholar)
    def __init__(self, parent: Optional[QObject] = ...) -> None:
        super().__init__()
    
    def run(self):
        scholar = get_scholar(self.key_words, self.artical_num)
        self.send_scholar.emit(scholar)
        print('scholar')
        pass

    def save_kw_artical_num(self, kw_artical_num: list):
        self.key_words = kw_artical_num[0]
        self.artical_num = kw_artical_num[1]
        
class Thread2(QThread):
    send_artical_database = pyqtSignal(dict)
    send_reflash_main = pyqtSignal(int)
    def __init__(self, schloar: Scholar, artical_num: int, i: int, artical_datebase: Dict) -> None:
        self.scholar, self.artical_num, self.i, self.artical_datebase = schloar, artical_num, i, artical_datebase
        super().__init__()
    
    def run(self):
        for j in range(self.artical_num, self.artical_num+10):
            self.artical_datebase[str(j)] = [self.scholar.artical[self.i], self.scholar.artical[self.i].abstract()]#访问变量修改
            self.i +=1              
            if self.i < 10:
                time.sleep(4)
            self.send_reflash_main.emit(self.i)
        self.send_artical_database.emit(self.artical_datebase)
    
class main_w2(QMainWindow, Ui_MainWindow):
    send_kw_artical_num = pyqtSignal(list)
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.download.clicked.connect(self.Download)
        self.search.clicked.connect(lambda :self.Search(self.keyword1.toPlainText()))
        self.up.clicked.connect(lambda :self.Up(self.keyword1.toPlainText(),self.num_gui.toPlainText()))
        self.next.clicked.connect(lambda :self.Next(self.keyword1.toPlainText(),self.num_gui.toPlainText()))
        self.go.clicked.connect(lambda :self.Go(self.keyword1.toPlainText(),self.num_gui.toPlainText()))
        self.button_is_close=False
        self.scholar : Scholar
        self.artical_datebase = {}
        self.thread = Thread1()
        self.thread.send_scholar.connect(self.save_scholar)
        self.send_kw_artical_num.connect(self.thread.save_kw_artical_num)

    
    def send_kw_(self):
        self.send_kw_artical_num.emit([self.key_words, self.artical_num])
        
    
    
    
    def loading(self, artical_num) -> None:
        '''
        缓存摘要
        '''
        def reflash(i: int, self=self):
            self.progressBar.setValue(i*10)
            QApplication.processEvents()
        
        def save_artical_datebase(artical_datebase: Dict, self=self):
            self.artical_datebase = artical_datebase
            self.redisplay(self.artical_num)
            self.button_is_close = False
            self.button_statu()
              
        self.results_gui.setText(str(self.scholar.search_result_nums))
        self.button_is_close = True
        self.button_statu()
        i = 0
        self.thread2 = Thread2(self.scholar, artical_num, i, self.artical_datebase)
        self.thread2.send_reflash_main.connect(reflash)
        self.thread2.send_artical_database.connect(save_artical_datebase)
        self.thread2.start()
        
        
        # for j in range(artical_num, artical_num+10):
        #     self.artical_datebase[str(j)] = [self.scholar.artical[i], self.scholar.artical[i].abstract()]#访问变量修改
        #     i +=1              
        #     if i < 10:
        #         time.sleep(4)
        #     self.progressBar.setValue(i*10)
        #     QApplication.processEvents()
            
            

    def button_statu(self) -> None:
        '''
        改变按钮状态
        '''
        self.download.setDisabled(self.button_is_close)
        self.search.setDisabled(self.button_is_close)
        self.up.setDisabled(self.button_is_close)
        self.next.setDisabled(self.button_is_close)
        self.go.setDisabled(self.button_is_close)
    

    def redisplay(self, artical_num: int) -> None:
        '''
        根据论文号更新显示文献名、中英文摘要、第几篇文献、期刊、年份、数据库、作者
        '''
        a = self.artical_datebase[str(artical_num)][0]
        artical_abstract = self.artical_datebase[str(artical_num)][1]
        self.article_name.setText(a.name)
        self.Abstract_1.setText(artical_abstract[0])
        self.Abstract_2.setText(artical_abstract[1])
        self.num_gui.setPlainText(str(artical_num))
        self.journal_gui.setPlainText(a.journal)
        self.year_gui.setText(a.year)
        self.datebase_gui.setPlainText(a.database)
        self.author_gui.setPlainText(a.author)


    def Download(self, artical_num):
        '''
        定义下载按钮
        '''
        a = self.artical_datebase[artical_num][0]
        name = a.name
        fname, _ = QFileDialog.getSaveFileName(self, 'save file', name)
        saved = save_file(a.url, fname)
        if saved:
            print("download successful")
        else:
            print("download failed")

    def save_scholar(self, scholar: Scholar):
            self.scholar = scholar
            if self.scholar.statu:
                self.loading(self.artical_num)           
            else:
                self.Abstract_1.setText(self.scholar.text)
    
    def Search(self, key_words: str) -> None:
        '''
        定义搜索按钮
        '''
        self.key_words = key_words
        self.msg()
        self.search.setDisabled(True)
        self.artical_num = 1
        self.scholar = ''
        self.send_kw_()
        self.thread.start()
    
        


    def Up(self,key_words: str,artical_num: str) -> None :
        '''
        定义上按钮
        '''
        self.up.setDisabled(True)
        artical_num= int(artical_num)-1
        if artical_num >0:
            if not self.artical_datebase.get(str(artical_num)):
                self.scholar = ''
                self.scholar = get_scholar(key_words, artical_num)
                if self.scholar.statu:
                    self.loading(self) 
                else:
                    self.Abstract_1.setText(self.scholar.text)
            self.redisplay(artical_num)
            self.button_is_close = False
            self.button_statu()


    def Next(self,key_words: str, artical_num: str) -> None:
        '''
        定义下按钮
        '''
        self.next.setDisabled(True)
        artical_num = int(artical_num)+1
        if not self.artical_datebase.get(str(artical_num)):
            self.msg()
            self.scholar = ''
            self.scholar = get_scholar(key_words, artical_num)
            if self.scholar.statu:
                self.loading(artical_num) 
            else:
                self.Abstract_1.setText(self.scholar.text)
        self.redisplay(artical_num)
        self.button_is_close = False
        self.button_statu()


    def Go(self,key_words: str, artical_num: str):
        '''
        定义跳转按钮
        '''
        self.go.setDisabled(True)
        artical_num = int(artical_num)
        if not self.artical_datebase.get(str(artical_num)):
            self.scholar = ''
            self.scholar = get_scholar(key_words, artical_num)
            if self.scholar.statu:
                self.loading(self) 
            else:
                self.Abstract_1.setText(self.scholar.text)
        self.redisplay(artical_num)
        self.button_is_close = False
        self.button_statu()



    def msg(self):
        reply = QMessageBox.about(self,'提示','Waiting for loading abstract')


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
