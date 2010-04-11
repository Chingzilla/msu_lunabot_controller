'''
Created on Apr 4, 2010

@author: ching
'''
from PyQt4 import QtGui, QtCore
from main_ui import Ui_MainWindow
from Telnet_Connection import Connection
import pygame
import sys
import threading
import time

class MainWindow(QtGui.QMainWindow, Ui_MainWindow):
    def __init__(self, parent=None):
        QtGui.QMainWindow.__init__(self,parent)  
        self.setupUi(self)
        
        ### Setup Telnet
        #self.tc = Connection('localhost',2002)
        
        ### Setup Joystick
        self.joystickThread = threading.Thread(target = self.joyUpdate)
        self.joystickThread.setDaemon(1)
        
        pygame.init()
        self.joystick_en = False
        
        if pygame.joystick.get_count() > 0:
            self.joy0 = pygame.joystick.Joystick(0)
            self.joy0.init()
            self.joystick_en = True
            self.joystickThread.start()
        
        ### Connect Movement
        # Connect Stop button
        self.connect(self.button_move_stop, QtCore.SIGNAL('clicked()'), self.stopMotors)
        
        # Connect Direction Keys
        self.connect(self.button_move_right, QtCore.SIGNAL('clicked()'), self.incRightTurn)
        self.connect(self.button_move_left, QtCore.SIGNAL('clicked()'), self.incLeftTurn)
        self.connect(self.button_move_forward, QtCore.SIGNAL('clicked()'), self.incForward)
        self.connect(self.button_move_backward, QtCore.SIGNAL('clicked()'), self.incBackward)
        
        # Emit Slider Value Change
        self.connect(self.slider_speed_left, QtCore.SIGNAL('valueChanged(int)'), self.motorSpeedChange)
        self.connect(self.slider_speed_right, QtCore.SIGNAL('valueChanged(int)'), self.motorSpeedChange)
        
    
    def motorSpeedChange(self):
      
	self.lcd_speed_right.display(self.slider_speed_right.value())
	self.lcd_speed_left.display(self.slider_speed_left.value())
        
        if self.slider_speed_right.value() < 0:
            self.tc.send('right_backward', abs(self.slider_speed_right.value()))
        else:
            self.tc.send('right_forward', self.slider_speed_right.value())

        if self.slider_speed_left.value() < 0:  
            self.tc.send('left_backward', abs(self.slider_speed_left.value()))
        else:
            self.tc.send('left_forward', self.slider_speed_left.value())                                   
        
        print self.slider_speed_left.value(), "\t", self.slider_speed_right.value()
        self.emit(QtCore.SIGNAL('motorSpeedChanged()'))

    def stopMotors(self):
        ''' Move the motor speed sliders to zero '''
        self.slider_speed_left.setValue(0)
        self.slider_speed_right.setValue(0)
        
    def incLeftTurn(self):
        ''' Increase the speed to turn left '''
        diff = self.slider_speed_right.value() + self.slider_speed_left.value() 
        if(not diff == 0):
            self.stopMotors()
            
        self.slider_speed_left.triggerAction(2)
        self.slider_speed_right.triggerAction(1)    
            
    def incRightTurn(self):
        ''' Increase the speed to turn right '''
        diff = self.slider_speed_right.value() + self.slider_speed_left.value() 
        if(not diff == 0):
            self.stopMotors()
            
        self.slider_speed_left.triggerAction(1)
        self.slider_speed_right.triggerAction(2)  
       
    def incForward(self):
        ''' Increase the speed forward '''
        if(self.slider_speed_left.value() != self.slider_speed_right.value()):
            self.stopMotors()
            
        self.slider_speed_left.triggerAction(1)
        self.slider_speed_right.triggerAction(1)
        
    def incBackward(self):
        ''' Increase the speed backward '''
        if(self.slider_speed_left.value() != self.slider_speed_right.value()):
            self.stopMotors()
            
        self.slider_speed_left.triggerAction(2)
        self.slider_speed_right.triggerAction(2)  
            
    def incLeftMotorSpeed(self):
        print self.slider_speed_left.value()
        self.slider_speed_left.sl
        
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
    def joyUpdate(self):
        try:
            while(self.joystick_en):
                left = self.joyScale(1,self.slider_speed_left.value())
                right = self.joyScale(4,self.slider_speed_right.value())
                if left != 266:
                    self.slider_speed_left.setValue(left)
                if right != 266:
                    self.slider_speed_right.setValue(right)
                pygame.event.clear()
                pygame.event.pump()
                time.sleep(.1)
        except:
            raise
    def joyScale(self,axis,old):
        value = self.joy0.get_axis(axis)
        if abs(value) < .20:
            value = 0
            if old == 0:
                return 266                    
        elif value > 0:
            value -= .10
        else:
            value += .10
        value = (value * -255) // 1
        
        if (value > old - 5) and (value < old + 5):
            return 266
        else:
            return value
        
app = QtGui.QApplication(sys.argv)

mw = MainWindow()
mw.show()
app.exec_()