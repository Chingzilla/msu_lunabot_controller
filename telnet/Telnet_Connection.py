'''
Created on Feb 27, 2010

@author: ching
'''

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
import telnetlib

class Connection(object):    
    '''
    This class is used to control the connection to
    the embedded board
    '''

    def __init__(self, hostName, portNumber):
        '''
        Constructor
        '''
        self.port = portNumber
        self.host = hostName
        
        self.tn = telnetlib.Telnet(hostName)
        self.reconnect()
        
    def disconnect(self):
        self.tn.close()
        
    def reconnect(self):
        self.tn = telnetlib.Telnet(host, port)
        self.tn.read_unil("Escape character is '^]'.", 2)
        
    def send(self, operation, data = None):
        '''
        Writes operand and data to lunarbot
        - returns false if:
        --- operation is not defined
        --- connection is closed
        '''
        
        #Check if valid
        if(not protocol_out.has_key(operation)):
            print "Error: operation not valid"
            return False
        
        try:
            #write Opcode
            self.tn.write(protocol_out[operation])
            
            #write data (if opt-code supports operands)
            if(protocol_hasOperand[operation]):
                self.tn.write(char(data))
        except socket.error:
            print "Error: telnet connection lost"
            self.reconnect()
            return False
        
        #operation successfully sent
        return True
            
    def read(self):
        pass
        