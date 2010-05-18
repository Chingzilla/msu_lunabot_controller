'''
Created on Apr 4, 2010

@author: ching
'''
from PyQt4 import QtGui, QtCore
from main_ui import Ui_MainWindow
from telnet.Telnet_Connection import Connection_Manager
from Telnet_Connection import FakeConnection
import pygame
import sys
import threading

class MainWindow(QtGui.QMainWindow, Ui_MainWindow):
    def __init__(self, parent=None):
        QtGui.QMainWindow.__init__(self,parent)  
        self.setupUi(self)
        
        ### Setup Telnet
        #self.tc = Connection_Manager.getInstance('192.168.0.49',2001)
        self.tc = FakeConnection('0.0.0.0',100)
        
        ### Setup Joystick
        self.joystickThread = threading.Thread(target = self.joyUpdate)
        self.joystickThread.setDaemon(1)
        
        pygame.init()
        self.joystick_en = False
        
        if pygame.joystick.get_count() > 0:
            self.joy0 = pygame.joystick.Joystick(0)
            self.joy0.init()
            self.joystick_en = True
            self.check_joystick_enable.setChecked(True)
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
        
        # Connect Belt UI
        self.connect(self.slider_belt_speed, QtCore.SIGNAL('valueChanged(int)'), self.belt_setspeed)
        
        self.connect(self.button_belt_start, QtCore.SIGNAL('clicked()'), self.belt_start)
        self.connect(self.button_belt_stop, QtCore.SIGNAL('clicked()'), self.belt_stop)
        self.connect(self.button_belt_lower, QtCore.SIGNAL('pressed()'), self.belt_lower)
        self.connect(self.button_belt_raise, QtCore.SIGNAL('pressed()'), self.belt_raise)
        self.connect(self.button_belt_lower, QtCore.SIGNAL('released()'), self.belt_stop_raise)
        self.connect(self.button_belt_raise, QtCore.SIGNAL('released()'), self.belt_stop_raise)
        
        # Connect Bucket UI
        self.connect(self.button_bucket_up, QtCore.SIGNAL('pressed()'), self.bucket_raise)
        self.connect(self.button_bucket_down, QtCore.SIGNAL('pressed()'), self.bucket_lower)
        self.connect(self.button_bucket_up, QtCore.SIGNAL('released()'), self.bucket_stop)
        self.connect(self.button_bucket_down, QtCore.SIGNAL('released()'), self.bucket_stop)
        
        # Connect the Panic Button
        self.connect(self.button_panic, QtCore.SIGNAL('clicked()'), self.panic)
        
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
        temp_left = 300
        temp_right = 300
        temp_trigger_digger = 300
        while self.joystick_en:
            for event in pygame.event.get():
                if event.type == pygame.JOYAXISMOTION:
                    value = -self.joyScale(event.value)
                    if event.axis == 1:
                        temp_left = value
                    elif event.axis == 4:
                        temp_right = value
                    elif event.axis == 5:
                        value = self.triggerScale(event.value)
                        temp_trigger_digger = value
                    
                elif event.type == pygame.JOYBUTTONDOWN:
                    if event.button == 7:
                        self.panic()
                    elif event.button == 0:
                        self.bucket_lower()
                    elif event.button == 3:
                        self.bucket_raise()
                    elif event.button == 14:
                        pass
                        toggle_state = not self.group_belt.isChecked()
                        self.group_belt.setEnabled(toggle_state)
                        self.group_belt.setChecked(toggle_state)
                    elif event.button == 6:
                        pass
                        toggle_state = self.group_bucket.isChecked()
                        self.group_bucket.setEnabled(not toggle_state)
                    elif event.button == 11:
                        self.belt_lower()
                    elif event.button == 10:
                        self.belt_raise()
                elif event.type == pygame.JOYBUTTONUP:
                    if event.button == 0:
                        self.bucket_stop()
                    elif event.button == 3:
                        self.bucket_stop()
                    elif event.button == 11:
                        self.belt_stop_raise()
                    elif event.button == 10:
                        self.belt_stop_raise()
                    
            if temp_left != 300:
                self.slider_speed_left.setValue(value)
                temp_left = 300
            if temp_right != 300:
                self.slider_speed_right.setValue(value)
                temp_right = 300
            if temp_trigger_digger != 300:
                self.slider_belt_speed.setValue(value)
                self.button_belt_start.click()
                temp_trigger_digger = 300
                
            pygame.time.Clock().tick(60)
            pygame.event.pump()
                                            
    def joyScale(self,value):
        if abs(value) < .20:
            value = 0                    
        else:
            value = int(value * 255)
        return value
    
    def triggerScale(self,value):
        value += 1
        value = int(value*127)
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
    
    def belt_stop(self):
        '''  call to stop the belt '''
        self.tc.send('belt_stop')
        
    def belt_setspeed(self):
        ''' call when the belt speed has changed '''  
        self.lcd_belt_speed.display(self.slider_belt_speed.value())
        
    def belt_lower(self):
        ''' call to lower the digger '''
        self.tc.send('belt_lower', self.spinbox_belt_raise_speed.value())
        
    def belt_raise(self):
        ''' call to raise the digger '''
        self.tc.send('belt_raise', self.spinbox_belt_raise_speed.value())
    
    def belt_stop_raise(self):
        ''' call to stop raising/lowering the belt '''
        self.tc.send('belt_raise', 0)
        
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
        self.slider_speed_left.setValue(0)
        self.slider_speed_right.setValue(0)
        
app = QtGui.QApplication(sys.argv)

mw = MainWindow()
mw.show()
app.exec_()
