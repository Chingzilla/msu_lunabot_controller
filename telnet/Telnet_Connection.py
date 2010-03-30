'''
This class manages the connection and communication with the
Lunarbot using a client Telnet

@author: ching
'''
import telnetlib
import sys

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
                 'fullstop'       : 'l',
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
                         'belt_start',
                         'belt_stop'
                         ]


class Connection(object):    
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
        self.port = portNumber
        self.host = hostName
        
        self.connect()
        
    def disconnect(self):
        '''
        Disconnects the telnet connection
        '''
        print 'disconnect'
        self.tn.close()
        
    def connect(self):
        '''
        Reconnects the telnet connection
        '''
        print 'connecting to telnet: ', self.host
        self.tn = telnetlib.Telnet(self.host, self.port)
        print 'connected'
        
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
            self.reconnect()
            return False           
            sys.stderr.write(">>> Operand Error: value is out of range\n")
            
            #reset connection
            self.tn.write(protocol_out['serial_sync'])
            
            return False
        
        #operation successfully sent
        return True
            
    def getData(self):
        '''
        Read returns the next data set from the Lunarbot, returns None if nothing is on
        the bus, or if a communications are incomplete
        '''
        pass