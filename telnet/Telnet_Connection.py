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
        '''
        self.port = portNumber
        self.host = hostName
        
        self.tn = telnetlib.Telnet(hostName)
        self.reconnect()
        
    def disconnect(self):
        '''
        Disconnects the telnet connection
        '''
        self.tn.close()
        
    def reconnect(self):
        '''
        Reconnects the telnet connection
        '''
        self.tn = telnetlib.Telnet(host, port)
        self.tn.read_unil("Escape character is '^]'.", 2)
        
    def send(self, operation, data = None):
        '''
        Writes operand and data to lunarbot
        - returns false if:
        --- operation is not defined
        --- operation needs data that is not given
        --- connection is closed (and tries to reconnect)
        '''
        
        #Check if valid
        if(not protocol_out.has_key(operation)):
            sys.stderr.write(">>>Protocol Error: operation not valid\n")
            return False
        
        #Check if needs opcode needs operand
        if(protocol_hasOperand[operation] and data == None):
            sys.stderr.write(">>>Protocol Error: operation needs data")
            return False

        try:
            #write Opcode
            self.tn.write(protocol_out[operation])
            
            #write data (if opt-code supports operands)
            if(protocol_hasOperand[operation]):
                self.tn.write(char(data))
                
        except socket.error:
            sys.stderr.q
            sys.stderr.write(">>>Connection Error: telnet connection lost, reconnecting\n")
            self.reconnect()
            return False
        
        #operation successfully sent
        return True
            
    def read(self):
        '''
        pass