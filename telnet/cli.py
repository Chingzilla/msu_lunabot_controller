'''
Created on Mar 29, 2010

@author: ching
'''

if __name__ == '__main__':
    pass

import sys
from Telnet_Connection import Connection_Manager, protocol_out

class main():
    '''
    Simple cli for telnet connection
    '''
    
    host = '192.168.0.49'
    host_port = 2001
  
    tc = Connection_Manager.getInstance(host,host_port)
    
    for i in protocol_out:
        sys.stdout.write(i + "\n")
    sys.stdout.write('***********\n')
        
    while(True):
        sys.stdout.write("What do you want to do?\n")
        
        command = sys.stdin.readline().rstrip().split(' ')
        
        if(len(command) == 2):
            tc.send(command[0], int(command[1]))
        elif(len(command) == 1):
            tc.send(command[0])
        else:
            sys.stderr.write(">>> Command Error: out of bounds\n")