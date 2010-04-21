'''
This class manages the connection and communication with the
Lunarbot using a client Telnet

@author: ching
'''
import telnetlib
import sys
import time
import threading

protocol_out = { 'move_forward'   : 'e',
                 'move_backward'  : 'f',
                 'left_forward'   : 'a',
                 'left_backward'  : 'b',
                 'right_forward'  : 'c',
                 'right_backward' : 'd',
                 'bucket_raise'   : 'g',
                 'bucket_lower'   : 'h',
                 'belt_start'     : 'm',
                 'belt_stop'      : 't',
                 'full_stop'      : 'l',
                 'stop_wheels'    : 'k',
                 'serial_sync'    : '!'
                 }

protocol_in = dict([(v, k) for (k, v) in protocol_out.iteritems()])

protocol_hasOperand = [  'move_forward',
                         'move_backward',
                         'left_forward',
                         'left_backward',
                         'right_forward',
                         'right_backward',
                         'bucket_raise',
                         'bucket_lower', 
                         'belt_start'
                         ]


class Connection_Interface(object):
    '''
    Standard interface to for communicating with with the
    Lunar robot.
    - Implements Multiton
    '''
    
    def __init__(self):
        self.instances = {}
        
    def getInstance(self,host,port):
        key = host + str(port)
        try:
            return self.instances[key]
        except keyError:
            self.instances[key] = _Connection(host,port)

class _Connection(object):    
    '''
    This class is used to control the connection to
    the embedded board
    '''

    def __init__(self, hostName, portNumber):
        '''
        Connection creates a telnet connection with 'hostName:portNumber'
        hostName = Computer's host name that is running Ser2Net
        portNumber = Port number that Ser2Net is using for the Telnet connection 
        '''
        self._port = portNumber
        self._host = hostName
        
        self.alive = False
        self.keep_alive_thread = threading.Thread(target=self.keepAlive)
        self.keep_alive_thread.setDaemon(1)
        
        self.connect()
        
    def disconnect(self):
        '''
        Disconnects the telnet connection
        '''
        print 'disconnect'
        self.alive = False
        self.tn.close()
        
    def connect(self):
        '''
        Connects the telnet connection
        '''
        print 'connecting to telnet: ', self._host
        self.alive = True
        self.tn = telnetlib.Telnet(self._host, self._port)
        print 'connected'
        
        self.keep_alive_thread.start()
    
    def keepAlive(self):
        '''
        Sends the no-op command every second to ensure 
        the connection is still there and prevent the
        FPGA board from timeing out
        '''
        try:
            while(self.alive):
                self.send("serial_sync")
                time.sleep(1)
        except:
            raise          
        
    def send(self, operation, data = None):
        '''
        Writes operand and data to lunarbot
        operation = opcode in readable from
        data = operand, values from 0 - 256
        - returns false if:
        --- operation is not defined
        --- operation needs data that is not given
        --- connection is closed (and tries to reconnect)
        '''
        
        #Check if valid
        if(not protocol_out.has_key(operation)):
            sys.stderr.write(">>> Protocol Error: operation not valid\n")
            return False
        
        #Check if needs opcode needs operand
        if(operation in protocol_hasOperand and data == None):
            sys.stderr.write(">>> Protocol Error: operation needs data\n")
            return False

        try:
            #write Opcode
            self.tn.write(protocol_out[operation])
            
            #shifts then writes data (if opt-code supports operands)
            if(operation in protocol_hasOperand):
                self.tn.write(chr(data))
                
        except ValueError:
            sys.stderr.write(">>> Connection Error: telnet connection lost, reconnecting\n")
            self.connect()
            return False           
            sys.stderr.write(">>> Operand Error: value is out of range\n")
            
            #reset connection
            self.tn.write(protocol_out['serial_sync'])
            
            return False
        
        #operation successfully sent
        time.sleep(.01)
        return True
            
    def getData(self):
        '''
        Read returns the next data set from the Lunarbot, returns None if nothing is on
        the bus, or if a communications are incomplete
        '''
        pass