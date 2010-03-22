#!/usr/bin/python

import sys
from PyQt4 import QtCore, QtGui

class Ui_Movement(QtGui.QWidget):
    def __init__(self, parent=None):
        QtGui.QWidget.__init__(self, parent)
        
        self.setGeometry(0, 0, 241, 221)
        self.setWindowTitle("Lunar Movement Widget")
        
        self.setLayout()
        
    def setLayout(self):

        self.verticalLayoutWidget = QtGui.QWidget(self)
        self.verticalLayoutWidget.setGeometry(QtCore.QRect(0, 0, 241, 221))
        self.verticalLayout = QtGui.QVBoxLayout(self.verticalLayoutWidget)
        
        self.motorSpeedLayout = QtGui.QHBoxLayout()
        self.motorSpeedLabel = QtGui.QLabel('Motor\nSpeed', self.verticalLayoutWidget)
        self.motorSpeedLayout.addWidget(self.motorSpeedLabel)
        
        self.leftMotorSlider = QtGui.QSlider(self.verticalLayoutWidget)
        self.leftMotorSlider.setMinimum(-256)
        self.leftMotorSlider.setMaximum(256)
        self.leftMotorSlider.setSingleStep(16)
        self.leftMotorSlider.setPageStep(32)
        self.leftMotorSlider.setOrientation(QtCore.Qt.Vertical)
        self.leftMotorSlider.setTickPosition(QtGui.QSlider.TicksAbove)
        self.leftMotorSlider.setTickInterval(64)
        self.leftMotorSlider.setObjectName("leftMotorSlider")
        self.motorSpeedLayout.addWidget(self.leftMotorSlider)
        
        self.rightMotorSlider = QtGui.QSlider(self.verticalLayoutWidget)
        self.rightMotorSlider.setMinimum(-256)
        self.rightMotorSlider.setMaximum(256)
        self.rightMotorSlider.setSingleStep(16)
        self.rightMotorSlider.setPageStep(32)
        self.rightMotorSlider.setOrientation(QtCore.Qt.Vertical)
        self.rightMotorSlider.setTickPosition(QtGui.QSlider.TicksAbove)
        self.rightMotorSlider.setTickInterval(64)
        self.rightMotorSlider.setObjectName("rightMotorSlider")
        self.motorSpeedLayout.addWidget(self.rightMotorSlider)
        
        spacerItem = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.motorSpeedLayout.addItem(spacerItem)
        
        self.verticalLayout.addLayout(self.motorSpeedLayout)
        self.dpadLayout = QtGui.QGridLayout()
        self.dpadLayout.setObjectName("dpadLayout")
        self.stopButton = QtGui.QPushButton('Stop', self.verticalLayoutWidget)
        self.stopButton.setObjectName("stopButton")
        self.dpadLayout.addWidget(self.stopButton, 1, 1, 1, 1)
        self.forwardButton = QtGui.QPushButton('Forward', self.verticalLayoutWidget)
        self.forwardButton.setObjectName("forwardButton")
        self.dpadLayout.addWidget(self.forwardButton, 0, 1, 1, 1)
        self.backwardButton = QtGui.QPushButton('Backward', self.verticalLayoutWidget)
        self.backwardButton.setObjectName("backwardButton")
        self.dpadLayout.addWidget(self.backwardButton, 2, 1, 1, 1)
        self.leftButton = QtGui.QPushButton('Left', self.verticalLayoutWidget)
        self.leftButton.setObjectName("leftButton")
        self.dpadLayout.addWidget(self.leftButton, 1, 0, 1, 1)
        self.rightButton = QtGui.QPushButton('Right', self.verticalLayoutWidget)
        self.rightButton.setObjectName("rightButton")
        self.dpadLayout.addWidget(self.rightButton, 1, 2, 1, 1)
        self.verticalLayout.addLayout(self.dpadLayout)

app = QtGui.QApplication(sys.argv)
moveUi = Ui_Movement()
moveUi.show()
app.exec_()