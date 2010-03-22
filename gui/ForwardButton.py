'''
Created on Mar 9, 2010

@author: ching
'''
#from Telnet_Connection import Connection

import sys
from PyQt4 import QtGui, QtCore
#from Telnet_Connection import Connection

class Gui(QtGui.QWidget):
    def __init__(self, parent=None):
        QtGui.QWidget.__init__(self, parent)
    
        widget = QtGui.QWidget()
        widget.resize(250, 150)
        widget.setWindowTitle('lunarbot - forward')
        widget.show()
        
        forward = QtGui.QPushButton('Forward',self)
        quit = QtGui.QPushButton('Close', self)
        
        hbox = QtGui.QHBoxLayout()
        hbox.addWidget(forward)
        hbox.addWidget(quit)
        
        self.setLayout(hbox)
        
        self.connect(forward,QtCore.SIGNAL("clicked()"),self.goForward) 
               
#        self.connect(self.quit, QtCore.SIGNAL('clicked()'),
#                     QtGui.qApp, QtCore.SLOT('quit()'))
        
    def goForward(self):
        print 'going forward'
    
    def goBackward(self):
        print 'going backward'

#self.tc = Connection('localhost', 2001)
app = QtGui.QApplication(sys.argv)
gui = Gui()
gui.show()
sys.exit(app.exec_())

