'''
Created on Apr 4, 2010

@author: ching
'''
from PyQt4 import QtGui, QtCore
from gui.main_ui import Ui_MainWindow
from telnet.Telnet_Connection import Connection_Manager
import pygame
import sys
import threading

class MainWindow(QtGui.QMainWindow, Ui_MainWindow):
    def __init__(self, parent=None):
        QtGui.QMainWindow.__init__(self,parent)  
        self.setupUi(self)
        
        self.belt_en = False
        
        ### Setup Telnet
        self.tc = Connection_Manager.getInstance('192.168.0.40',2001)
        
        ### Setup Joystick
        self.joystickThread = threading.Thread(target = self.joyUpdate)
        self.joystickThread.setDaemon(1)
        self.joystickThread.start()
        
        pygame.init()
        self.joystick_en = False
        
        if pygame.joystick.get_count() > 0:
            self.joy0 = pygame.joystick.Joystick(0)
            self.joy0.init()
            self.joystick_en = True
            self.check_joystick_enable.setChecked(True)
        
        ### Connect Movement
        # Connect Stop button
        self.connect(self.button_move_stop, QtCore.SIGNAL('clicked()'), self.stopMotors)
        
        # Connect Direction Keys
        self.connect(self.button_move_right, QtCore.SIGNAL('clicked()'), self.incRightTurn)
        self.connect(self.button_move_left, QtCore.SIGNAL('clicked()'), self.incLeftTurn)
        self.connect(self.button_move_forward, QtCore.SIGNAL('clicked()'), self.incForward)
        self.connect(self.button_move_backward, QtCore.SIGNAL('clicked()'), self.incBackward)
        
        # Emit Slider Value Change
        #self.connect(self.slider_speed_left, QtCore.SIGNAL('valueChanged(int)'), self.motorSpeedChange)
        self.connect(self.slider_speed_right, QtCore.SIGNAL('valueChanged(int)'), self.motorSpeedChange)
        
        # Connect Belt UI
        self.connect(self.slider_belt_speed, QtCore.SIGNAL('valueChanged(int)'), self.belt_setspeed)
        
        self.connect(self.button_belt_start, QtCore.SIGNAL('clicked()'), self.belt_start)
        self.connect(self.button_belt_stop, QtCore.SIGNAL('clicked()'), self.belt_stop)
        self.connect(self.button_belt_lower, QtCore.SIGNAL('clicked()'), self.belt_lower)
        self.connect(self.button_belt_raise, QtCore.SIGNAL('clicked()'), self.belt_raise)
        
        # Connect Bucket UI
        self.connect(self.button_bucket_up, QtCore.SIGNAL('clicked()'), self.bucket_raise)
        self.connect(self.button_bucket_down, QtCore.SIGNAL('clicked()'), self.bucket_lower)
        self.connect(self.button_bucket_stop, QtCore.SIGNAL('clicked()'), self.bucket_stop)
        
        # Connect the Panic Button
        self.connect(self.button_panic, QtCore.SIGNAL('clicked()'), self.panic)
        
        
        # Connect State Radio Buttons
        self.connect(self.radio_state_move, QtCore.SIGNAL('toggled()'), self.stateMove)
        
        ### Connect Joystick
        #self.connect(self.check_joystick_enable, QtCore.SIGNAL('stateChanged(int)'), self.toggleJoystickState)
    
    def motorSpeedChange(self):
      
        self.lcd_speed_right.display(self.slider_speed_right.value())
        self.lcd_speed_left.display(self.slider_speed_left.value())
        
        if self.slider_speed_left.value() < 0:  
            self.tc.send('left_backward', abs(self.slider_speed_left.value()))
        else:
            self.tc.send('left_forward', self.slider_speed_left.value()) 
                     
        if self.slider_speed_right.value() < 0:
            self.tc.send('right_backward', abs(self.slider_speed_right.value()))
        else:
            self.tc.send('right_forward', self.slider_speed_right.value())
        
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
        
    def keyPressEvent(self, event):
        ''' keyboard short cuts are handled here '''
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
        ''' scan's the gamepad for movements '''
        temp_left = 0
        temp_right = 0
        while self.joystick_en:
            for event in pygame.event.get():
                if event.type == pygame.JOYAXISMOTION:
                    value = self.joyScale(event.value)
                    if event.axis == 1 and temp_left != value:
                        temp_left = value
                        self.slider_speed_left.setValue(value)
                    elif event.axis == 3 and temp_right != value:
                        temp_right = value
                        self.slider_speed_right.setValue(value)
            pygame.time.get_ticks(30)
            pygame.event.pump()
                                            
    def joyScale(self,value):
        if abs(value) < .20:
            value = 0                    
        else:
            value = int(value * 255)
        return value
    
    def toggleJoystickState(self):
        ''' call to enable or disable the joystick '''
        if not self.joystick_en and pygame.joystick.get_count():
            self.joystick_en = False
        else:
            self.joystick_en = True
            self.joystickThread.start()
            
        self.check_joystick_enable.setChecked(self.joystick_en)
        
    def belt_start(self):
        ''' call to start the belt at the set speed '''
        self.tc.send('belt_start', self.slider_belt_speed.value())
        self.belt_en = True
    
    def belt_stop(self):
        '''  call to stop the belt '''
        self.tc.send('belt_stop')
        self.belt_en = False
        
    def belt_setspeed(self):
        ''' call when the belt speed has changed '''
        if self.belt_en:
            self.belt_start()
            
        self.lcd_belt_speed.display(self.slider_belt_speed.value())
        
    def belt_lower(self):
        ''' call to lower the digger '''
        self.tc.send('belt_lower', self.spinbox_belt_raise_speed.value())
        
    def belt_raise(self):
        ''' call to raise the digger '''
        self.tc.send('belt_raise', self.spinbox_belt_raise_speed.value())
        
    def bucket_lower(self):
        ''' call to lower the bucket '''
        self.tc.send('bucket_lower', self.spinbox_bucket_speed.value())
        
    def bucket_raise(self):
        ''' call to raise the bucket '''
        self.tc.send('bucket_raise', self.spinbox_bucket_speed.value())
    
    def bucket_stop(self):
        ''' call if the bucket needs to be stopped '''
        self.tc.send('bucket_lower', 0)
    
    def panic(self):
        '''  call to stop all functions '''
        self.tc.send('full_stop')
        self.belt_en = False
        self.slider_speed_left.setValue(0)
        self.slider_speed_right.setValue(0)
        
    def stateMove(self):
        '''
        changes the operating state to Move
        - disables the bucket controlls
        - disables and rasise the belt
        '''
        if self.radio_state_move.isChecked():
            # stop all fuctions
            self.panic()
            self.belt_raise()
            self.group_bucket.setChecked(False)
            self.group_belt.setChecked(False)
        
app = QtGui.QApplication(sys.argv)

mw = MainWindow()
mw.show()
app.exec_()