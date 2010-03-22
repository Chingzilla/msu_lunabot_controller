#!/usr/bin/python

import sys
from PyQt4 import QtCore, QtGui

class Ui_Movement(QtGui.QWidget):
    def __init__(self, parent=None):
        QtGui.QWidget.__init__(self, parent)
        
        self.sliderStep = 16
        self.sliderPage = 32
        
        self.setGeometry(0, 0, 241, 221)
        self.setWindowTitle("Lunar Movement Widget")
        
        self.setLayout()
        
    def setLayout(self):

        verticalLayoutWidget = QtGui.QWidget(self)
        verticalLayoutWidget.setGeometry(QtCore.QRect(0, 0, 241, 221))
        verticalLayout = QtGui.QVBoxLayout(verticalLayoutWidget)
        
        motorSpeedLayout = QtGui.QHBoxLayout()
        motorSpeedLabel = QtGui.QLabel('Motor\nSpeed', verticalLayoutWidget)
        motorSpeedLayout.addWidget(motorSpeedLabel)
        
        self.leftMotorSlider = QtGui.QSlider(verticalLayoutWidget)
        self.leftMotorSlider.setMinimum(-256)
        self.leftMotorSlider.setMaximum(256)
        self.leftMotorSlider.setSingleStep(self.sliderStep)
        self.leftMotorSlider.setPageStep(self.sliderPage)
        self.leftMotorSlider.setOrientation(QtCore.Qt.Vertical)
        self.leftMotorSlider.setTickPosition(QtGui.QSlider.TicksAbove)
        self.leftMotorSlider.setTickInterval(64)
        self.leftMotorSlider.setObjectName("leftMotorSlider")
        motorSpeedLayout.addWidget(self.leftMotorSlider)
        
        self.rightMotorSlider = QtGui.QSlider(verticalLayoutWidget)
        self.rightMotorSlider.setMinimum(-256)
        self.rightMotorSlider.setMaximum(256)
        self.rightMotorSlider.setSingleStep(self.sliderStep)
        self.rightMotorSlider.setPageStep(self.sliderPage)
        self.rightMotorSlider.setOrientation(QtCore.Qt.Vertical)
        self.rightMotorSlider.setTickPosition(QtGui.QSlider.TicksAbove)
        self.rightMotorSlider.setTickInterval(64)
        self.rightMotorSlider.setObjectName("rightMotorSlider")
        motorSpeedLayout.addWidget(self.rightMotorSlider)
        
        spacerItem = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        motorSpeedLayout.addItem(spacerItem)
        
        verticalLayout.addLayout(motorSpeedLayout)
        dpadLayout = QtGui.QGridLayout()
        dpadLayout.setObjectName("dpadLayout")
        stopButton = QtGui.QPushButton('Stop', verticalLayoutWidget)
        stopButton.setObjectName("stopButton")
        dpadLayout.addWidget(stopButton, 1, 1, 1, 1)
        forwardButton = QtGui.QPushButton('Forward', verticalLayoutWidget)
        forwardButton.setObjectName("forwardButton")
        dpadLayout.addWidget(forwardButton, 0, 1, 1, 1)
        backwardButton = QtGui.QPushButton('Backward', verticalLayoutWidget)
        backwardButton.setObjectName("backwardButton")
        dpadLayout.addWidget(backwardButton, 2, 1, 1, 1)
        leftButton = QtGui.QPushButton('Left', verticalLayoutWidget)
        leftButton.setObjectName("leftButton")
        dpadLayout.addWidget(leftButton, 1, 0, 1, 1)
        rightButton = QtGui.QPushButton('Right', verticalLayoutWidget)
        rightButton.setObjectName("rightButton")
        dpadLayout.addWidget(rightButton, 1, 2, 1, 1)
        verticalLayout.addLayout(dpadLayout)
        
        # Connect Stop button
        self.connect(stopButton, QtCore.SIGNAL('clicked()'), self.stopMotors)
        
        # Connect Direction Keys
        self.connect(rightButton, QtCore.SIGNAL('clicked()'), self.incRightTurn)
        self.connect(leftButton, QtCore.SIGNAL('clicked()'), self.incLeftTurn)
        self.connect(forwardButton, QtCore.SIGNAL('clicked()'), self.incForward)
        self.connect(backwardButton, QtCore.SIGNAL('clicked()'), self.incBackward)

    def stopMotors(self):
        ''' Move the motor speed sliders to zero '''
        self.rightMotorSlider.setValue(0)
        self.leftMotorSlider.setValue(0)
        
    def incLeftTurn(self):
        ''' Increase the speed to turn left '''
        diff = self.rightMotorSlider.value() + self.leftMotorSlider.value() 
        if(self.rightMotorSlider.value() > 0 or
           not diff == 0):
            self.stopMotors()
        
        self.leftMotorSlider.triggerAction(1)
        self.rightMotorSlider.triggerAction(2)    
            
    def incRightTurn(self):
        ''' Increase the speed to turn right '''
        diff = self.rightMotorSlider.value() + self.leftMotorSlider.value() 
        if(self.leftMotorSlider.value() > 0 or
           not diff == 0):
            self.stopMotors()
            
        self.leftMotorSlider.triggerAction(2)
        self.rightMotorSlider.triggerAction(1)  
       
    def incForward(self):
        ''' Increase the speed forward '''
        if(self.leftMotorSlider.value() != self.rightMotorSlider.value()):
            self.stopMotors()
            
        self.leftMotorSlider.triggerAction(1)
        self.rightMotorSlider.triggerAction(1)
        
    def incBackward(self):
        ''' Increase the speed backward '''
        if(self.leftMotorSlider.value() != self.rightMotorSlider.value()):
            self.stopMotors()
            
        self.leftMotorSlider.triggerAction(2)
        self.rightMotorSlider.triggerAction(2)  
            
    def incLeftMotorSpeed(self):
        print self.leftMotorSlider.value()
        self.leftMotorSlider.sl
         
app = QtGui.QApplication(sys.argv)
moveUi = Ui_Movement()
moveUi.show()
app.exec_()