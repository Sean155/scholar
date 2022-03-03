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


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1540, 883)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.download = QtWidgets.QPushButton(self.centralwidget)
        self.download.setGeometry(QtCore.QRect(1430, 800, 100, 30))
        font = QtGui.QFont()
        font.setPointSize(18)
        self.download.setFont(font)
        self.download.setObjectName("download")
        self.keyword1 = QtWidgets.QTextEdit(self.centralwidget)
        self.keyword1.setGeometry(QtCore.QRect(130, 30, 1171, 43))
        font = QtGui.QFont()
        font.setPointSize(20)
        self.keyword1.setFont(font)
        self.keyword1.setObjectName("keyword1")
        self.label1 = QtWidgets.QLabel(self.centralwidget)
        self.label1.setGeometry(QtCore.QRect(20, 30, 100, 31))
        font = QtGui.QFont()
        font.setPointSize(18)
        self.label1.setFont(font)
        self.label1.setObjectName("label1")
        self.search = QtWidgets.QPushButton(self.centralwidget)
        self.search.setGeometry(QtCore.QRect(1320, 40, 100, 30))
        font = QtGui.QFont()
        font.setPointSize(18)
        self.search.setFont(font)
        self.search.setObjectName("search")
        self.Abstract_1 = QtWidgets.QTextBrowser(self.centralwidget)
        self.Abstract_1.setGeometry(QtCore.QRect(20, 190, 750, 601))
        font = QtGui.QFont()
        font.setPointSize(20)
        self.Abstract_1.setFont(font)
        self.Abstract_1.setObjectName("Abstract_1")
        self.label1_2 = QtWidgets.QLabel(self.centralwidget)
        self.label1_2.setGeometry(QtCore.QRect(40, 80, 61, 31))
        font = QtGui.QFont()
        font.setPointSize(18)
        self.label1_2.setFont(font)
        self.label1_2.setObjectName("label1_2")
        self.article_name = QtWidgets.QTextBrowser(self.centralwidget)
        self.article_name.setGeometry(QtCore.QRect(130, 80, 811, 43))
        font = QtGui.QFont()
        font.setPointSize(18)
        self.article_name.setFont(font)
        self.article_name.setObjectName("article_name")
        self.label1_4 = QtWidgets.QLabel(self.centralwidget)
        self.label1_4.setGeometry(QtCore.QRect(950, 90, 91, 31))
        font = QtGui.QFont()
        font.setPointSize(18)
        self.label1_4.setFont(font)
        self.label1_4.setObjectName("label1_4")
        self.journal = QtWidgets.QTextBrowser(self.centralwidget)
        self.journal.setGeometry(QtCore.QRect(1050, 80, 461, 43))
        font = QtGui.QFont()
        font.setPointSize(18)
        self.journal.setFont(font)
        self.journal.setObjectName("journal")
        self.up = QtWidgets.QPushButton(self.centralwidget)
        self.up.setGeometry(QtCore.QRect(590, 802, 40, 30))
        font = QtGui.QFont()
        font.setPointSize(18)
        self.up.setFont(font)
        self.up.setObjectName("up")
        self.next = QtWidgets.QPushButton(self.centralwidget)
        self.next.setGeometry(QtCore.QRect(650, 802, 55, 30))
        font = QtGui.QFont()
        font.setPointSize(18)
        self.next.setFont(font)
        self.next.setObjectName("next")
        self.results = QtWidgets.QLabel(self.centralwidget)
        self.results.setGeometry(QtCore.QRect(485, 807, 81, 30))
        font = QtGui.QFont()
        font.setPointSize(22)
        self.results.setFont(font)
        self.results.setObjectName("results")
        self.IF_3 = QtWidgets.QLabel(self.centralwidget)
        self.IF_3.setGeometry(QtCore.QRect(473, 805, 30, 30))
        font = QtGui.QFont()
        font.setPointSize(22)
        self.IF_3.setFont(font)
        self.IF_3.setObjectName("IF_3")
        self.article_num = QtWidgets.QTextEdit(self.centralwidget)
        self.article_num.setGeometry(QtCore.QRect(380, 800, 91, 41))
        font = QtGui.QFont()
        font.setPointSize(18)
        self.article_num.setFont(font)
        self.article_num.setLayoutDirection(QtCore.Qt.RightToLeft)
        self.article_num.setObjectName("article_num")
        self.label1_5 = QtWidgets.QLabel(self.centralwidget)
        self.label1_5.setGeometry(QtCore.QRect(20, 150, 101, 31))
        font = QtGui.QFont()
        font.setPointSize(18)
        self.label1_5.setFont(font)
        self.label1_5.setObjectName("label1_5")
        self.go = QtWidgets.QPushButton(self.centralwidget)
        self.go.setGeometry(QtCore.QRect(720, 802, 51, 30))
        font = QtGui.QFont()
        font.setPointSize(18)
        self.go.setFont(font)
        self.go.setObjectName("go")
        self.line = QtWidgets.QFrame(self.centralwidget)
        self.line.setGeometry(QtCore.QRect(10, 130, 1501, 16))
        self.line.setFrameShape(QtWidgets.QFrame.HLine)
        self.line.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line.setObjectName("line")
        self.Abstract_2 = QtWidgets.QTextBrowser(self.centralwidget)
        self.Abstract_2.setGeometry(QtCore.QRect(780, 190, 750, 600))
        font = QtGui.QFont()
        font.setPointSize(20)
        self.Abstract_2.setFont(font)
        self.Abstract_2.setObjectName("Abstract_2")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1540, 22))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)
        MainWindow.setTabOrder(self.keyword1, self.download)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.download.setText(_translate("MainWindow", "Download"))
        self.keyword1.setHtml(_translate("MainWindow", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'SimSun\'; font-size:20pt; font-weight:400; font-style:normal;\">\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><br /></p></body></html>"))
        self.label1.setText(_translate("MainWindow", "Keywords"))
        self.search.setText(_translate("MainWindow", "Serch"))
        self.Abstract_1.setHtml(_translate("MainWindow", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'SimSun\'; font-size:20pt; font-weight:400; font-style:normal;\">\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><br /></p></body></html>"))
        self.label1_2.setText(_translate("MainWindow", "Name"))
        self.article_name.setHtml(_translate("MainWindow", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'SimSun\'; font-size:18pt; font-weight:400; font-style:normal;\">\n"
"<p dir=\'rtl\' style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">...</p></body></html>"))
        self.label1_4.setText(_translate("MainWindow", "journal"))
        self.up.setText(_translate("MainWindow", "Up"))
        self.next.setText(_translate("MainWindow", "Next"))
        self.results.setText(_translate("MainWindow", "..."))
        self.IF_3.setText(_translate("MainWindow", "/"))
        self.article_num.setHtml(_translate("MainWindow", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'SimSun\'; font-size:18pt; font-weight:400; font-style:normal;\">\n"
"<p dir=\'rtl\' style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">1</p></body></html>"))
        self.label1_5.setText(_translate("MainWindow", "Abstract"))
        self.go.setText(_translate("MainWindow", "Go"))
        self.Abstract_2.setHtml(_translate("MainWindow", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'SimSun\'; font-size:20pt; font-weight:400; font-style:normal;\">\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><br /></p></body></html>"))


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