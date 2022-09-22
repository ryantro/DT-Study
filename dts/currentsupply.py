# -*- coding: utf-8 -*-
"""
Created on Thu Jul 14 18:29:37 2022

@author: ryan.robinson
"""

import pyvisa
import time

def main():
    
    usbaddr = 'ASRL6::INSTR'
    
    # rm = pyvisa.ResourceManager()
    # a = rm.list_resources()
    # print(a)
    
    try:
        CS = CurrentSupply(addr = usbaddr, pprint = True)
        CS.getCurrent()
        CS.off()
        # CS.setCurrent()
        CS.getState()
        CS.getCurrent()
    finally:
        CS.close()
    return

class CurrentSupply:
    def __init__(self, addr = 'ASRL6::INSTR', pprint = False):
        
         
        self.cs = USBDevice(addr)
        
        self.pprint = pprint
        
        self.cs.write('SYST:LOCK ON')
        
        if(pprint):
            id = self.cs.send('*IDN?')
            print(id)
        
        return
    
    def getCurrent(self):
        
        curr = self.cs.send('CURR?')
        print(curr)
        return curr
    
    def setCurrent(self):
        
        self.cs.write('CURR 2')
        
        return
    
    def getState(self):
        
        st = self.cs.send('OUTPUT?')
        print(st)
        return st
    
    def on(self):
        """
        TURN CURRENT SUPPLY ON
        """
        self.cs.write('OUTPUT ON')
        
        if(self.getState() != 'ON'):
            print("Error: state didn't change.")
            return 1
        
        return 0
    
    def off(self):
        """
        TURN CURRENT SUPPLY OFF
        """
        self.cs.write('OUTPUT OFF')
        
        if(self.getState() != 'OFF'):
            print("Error: state didn't switch to off.")
            return 1
        
        return 0
    
    def close(self):
        
        self.cs.close()
        
        return

# GENERIC USB DEVICE CLASS
# USED TO COMMUNICATE WITH THE THORLABS ITC40005    
class USBDevice:
    def __init__(self,rname):
        self.inst = pyvisa.ResourceManager().open_resource(rname)
        return None
    
    def settimeout(self,timeout):
        """
        Sets the timeout.

        Parameters
        ----------
        timeout : int
            time before an exception is thrown.

        Returns
        -------
        None.

        """
        self.inst.timeout = timeout+1000
        
        return
    
    def write(self,command):
        """
        Sends a command that requires no response. 

        Parameters
        ----------
        command : str
            command string.

        Returns
        -------
        None.

        """
        self.inst.write(command)
        
        return
    
    def send(self,command):
        """
        Sends a command that gives a response.

        Parameters
        ----------
        command : str
            command string.

        Returns
        -------
        str
            command response.

        """
        return self.inst.query(command).strip('\r\n')
    
    def close(self):
        """
        Closes the device.

        Returns
        -------
        None.

        """
        self.inst.close()
        
        return
    


if __name__=="__main__":
    main()