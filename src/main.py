from PyQt5.QtWidgets import QMainWindow, QTableWidget, QTableWidgetItem, QApplication, QFileDialog,QMessageBox, QInputDialog
from PyQt5.QtGui import *
from PyQt5.QtCore import *
import sys
import requests
import sys
import re
from bs4 import BeautifulSoup
import time
from typing import List, Tuple
from PyQt5 import QtCore, QtGui, QtWidgets
from getsci import *
from google_translator import google_translator
from mainwindow import *

class main_w2(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.download.clicked.connect(self.Download)
        self.search.clicked.connect(lambda :self.Search(self.keyword1.toPlainText()))
        self.up.clicked.connect(lambda :self.Up(self.keyword1.toPlainText(),self.article_num.toPlainText()))
        self.next.clicked.connect(self.Next)
        self.go.clicked.connect(self.Go)
#初始化设置
        #self.Keywords=self.keyword1.toPlainText()
        #self.articlenum=int(self.article_num.toPlainText())-1

    def Download(self):
        '''
        定义下载按钮
        '''
        print("download")
        pass


    def Search(self,key_words: str) -> None:
        '''
        定义搜索按钮
        '''
        print("search")
        name, url = google_scholar(key_words,str(0))
        abstract = get_abstract(name)
        abstract_tran = google_translator().trans(abstract)
        self.article_name.setText(name)
        self.Abstract_1.setText(abstract)
        self.Abstract_2.setText(abstract_tran)


    def Up(self,key_words: str,artical_num: str) -> None :
        '''
        定义上按钮
        '''
        print("up")
        artical_num= int(artical_num)-1
        if artical_num>0:
            name, url = google_scholar(key_words, str(artical_num-1))
            abstract = get_abstract(name)
            abstract_tran = google_translator().trans(abstract)
            self.article_name.setText(name)
            self.Abstract_1.setText(abstract)
            self.Abstract_2.setText(abstract_tran)
            self.article_num.setPlainText(str(artical_num))


    def Next(self):
        '''
        定义下按钮
        '''
        print("next")
        pass


    def Go(self):
        '''
        定义跳转按钮
        '''
        print("go")
        pass


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