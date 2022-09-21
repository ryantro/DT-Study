# -*- coding: utf-8 -*-
"""
Created on Fri Jul 22 14:56:27 2022

@author: ryan.robinson
"""

# FOR DAQ
import nidaqmx.system
from nidaqmx.constants import LineGrouping
import time


def main():
    
    t1 = time.time()
    with nidaqmx.Task() as task:
        task.ao_channels.add_ao_voltage_chan("Dev3/ao1")
        task.write(5.0, auto_start=True)
    t2 = time.time()
    
    td = t2 - t1
    print(td)
    
    return



class RelayControl():
    
    def __init__(self,device = "Dev3"):
        """
        Initialize device.
        Can use NI Max to find the 'device' name.

        Parameters
        ----------
        device : TYPE, optional
            DESCRIPTION. Device name.

        Returns
        -------
        None.

        """
        self.target = '{}/port0/line0:5'.format(device)
        
        # Initialize all relays to be on, shorts across all emitters
        self.relays = [True, True, True, True, True, True]
        
        # Setup Daq
        self.sendToDaq()
        
        return
    
    def turnOn(self,num):
        """
        Turns on the specified emitter by switching off the respective relay
        and turning on all other relays.

        Parameters
        ----------
        num : TYPE
            DESCRIPTION. Can be any value from 0 to 5, specifies the emitter.

        Returns
        -------
        None.

        """
        # Check if a valid emitter num is entered
        if(num > 5):
            print("Invalid emitter specified")
        
        # Turn on the specified emitter
        else:
            self.relays = [True, True, True, True, True, True]
            self.relays[num] = False
            self.sendToDaq()
            
        return
    
    def sendToDaq(self):
        """
        Sends the command to the DAQ

        Returns
        -------
        None.

        """
        with nidaqmx.Task() as task:
            task.do_channels.add_do_chan(self.target, line_grouping=LineGrouping.CHAN_PER_LINE)
            task.write(self.relays)
            
        return
    
if __name__=="__main__":
    main()