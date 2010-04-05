'''
Created on Apr 4, 2010

@author: ching
'''
import PyQt4
from main_ui import Ui_MainWindow

class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self):
        self.setupUi(self)
        
        ###Connect movement###
        self.connect()
        
    def motorSpeedChange(self):
        
        if self.rightMotorSlider.value() < 0:
            self.tc.send('right_backward', abs(self.rightMotorSlider.value()))
        else:
            self.tc.send('right_forward', self.rightMotorSlider.value())

        if self.leftMotorSlider.value() < 0:  
            self.tc.send('left_backward', abs(self.leftMotorSlider.value()))
        else:
            self.tc.send('left_forward', self.leftMotorSlider.value())                                   
        
        print self.leftMotorSlider.value(), "\t", self.rightMotorSlider.value()
        self.emit(QtCore.SIGNAL('motorSpeedChanged()'))

    def stopMotors(self):
        ''' Move the motor speed sliders to zero '''
        self.leftMotorSlider.setValue(0)
        self.rightMotorSlider.setValue(0)
        
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