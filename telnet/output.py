#!/usr/bin/python

class ___Stdout:
  def __init__(self):
    self.out = ''
  def write(self,text):
    self.out += '\n', text
class ___StdErr:
  def __init__(self):
    self.err = ''
  def write(self,text):
    self.out += '\n', text
    
Stdout = ___Stdout()
Stderr = ___StdErr()