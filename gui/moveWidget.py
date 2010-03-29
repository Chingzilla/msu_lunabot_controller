#!/usr/bin/python
from Telnet_Connection import Connection

import sys
from PyQt4 import QtCore, QtGui

class Ui_Movement(QtGui.QWidget):
    def __init__(self, parent=None):
        
        QtGui.QWidget.__init__(self, parent)
        
        self.tc = Connection('localhost', 2001)
        
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
        self.leftMotorSlider.setTracking(True)
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
        self.rightMotorSlider.setTracking(True)
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
        
        # Emit Slider Value Change
        self.connect(self.leftMotorSlider, QtCore.SIGNAL('valueChanged(int)'), self.motorSpeedChange)
        self.connect(self.rightMotorSlider, QtCore.SIGNAL('valueChanged(int)'), self.motorSpeedChange)

    def motorSpeedChange(self):
        
        if self.rightMotorSlider.value() < 0:
            self.tc.send('right_backward', abs(self.rightMotorSlider.value()))
        else:
            self.tc.send('right_forward', self.rightMotorSlider.value())
#        if self.leftMotorSlider.value() < 0:  
#            self.tc.send('left_backward', abs(self.leftMotorSlider.vaule()))
#        else:
#            self.tc.send('left_forward', self.leftMotorSlider.value())                                   
        
        print self.leftMotorSlider.value(), "\t", self.rightMotorSlider.value()
        self.emit(QtCore.SIGNAL('motorSpeedChanged()'))

    def stopMotors(self):
        ''' Move the motor speed sliders to zero '''
        self.rightMotorSlider.setValue(0)
        self.leftMotorSlider.setValue(0)
        
    def incLeftTurn(self):
        ''' Increase the speed to turn left '''
        diff = self.rightMotorSlider.value() + self.leftMotorSlider.value() 
        if(not diff == 0):
            self.stopMotors()
            
        self.leftMotorSlider.triggerAction(2)
        self.rightMotorSlider.triggerAction(1)    
            
    def incRightTurn(self):
        ''' Increase the speed to turn right '''
        diff = self.rightMotorSlider.value() + self.leftMotorSlider.value() 
        if(not diff == 0):
            self.stopMotors()
            
        self.leftMotorSlider.triggerAction(1)
        self.rightMotorSlider.triggerAction(2)  
       
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
        
    def keyPressEvent(self, event):
        if type(event) == QtGui.QKeyEvent:
            # Move Forward (.)
            if event.key() == 46:
                self.incForward()
            # Move Backward (e)
            elif event.key() == 69:
                self.incBackward()
            # Move Left (o)
            elif event.key() == 79:
                self.incLeftTurn()
            # Move Right (u)
            elif event.key() == 85:
                self.incRightTurn()
            # Stop (a)
            elif event.key() == 65:
                self.stopMotors()
            else:
                event.ignore()
                return
            event.accept()
        else:
            event.ignore()
                     
app = QtGui.QApplication(sys.argv)
moveUi = Ui_Movement()
moveUi.show()
app.exec_()