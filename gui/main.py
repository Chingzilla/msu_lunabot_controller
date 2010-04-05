# -*- coding: utf-8 -*-
'''
Created on Apr 4, 2010

@author: ching
'''
from PyQt4 import QtGui
from main_ui import Ui_MainWindow
import sys

class MainWindow(QtGui.QMainWindow, Ui_MainWindow):
    def __init__(self, parent=None):
        QtGui.QMainWindow.__init__(self,parent)  
        self.setupUi(self)
        
app = QtGui.QApplication(sys.argv)

mw = MainWindow()
mw.show()
app.exec_()