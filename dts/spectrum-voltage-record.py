# -*- coding: utf-8 -*-
"""
Created on Wed Sep 21 16:13:50 2022

@author: ryan.robinson
"""

# -*- coding: utf-8 -*-
"""
Created on Wed Sep 21 10:57:22 2022

@author: ryan.robinson
"""
import time
import numpy as np
import arduinorelay as ar
import currentsupply as cs
import nidaqmx.system
from nidaqmx.constants import LineGrouping
import spectrum_analyzer as sa
import matplotlib.pyplot as plt

def main():
    
    current = 2.8
    emitters = [1, 2, 3, 4, 5, 6]
    arduinoCom = 'COM11'
    daq6210 = 'Dev2'
    daq6001 = 'Dev3'
    savefolder = ''#r'N:/temp/Ryan/dT-data'
    file = 'd1.csv'
    # file = savefolder + '/' + filename
    delay = 1.0 # seconds
    print(file)
    
    SA = sa.SpectrumAnalyzer()
    
    try:
        
        # SA.connect()
        """ turn all current sources off """
        
        """ select emitter """
        for emitter in emitters:
            
            """ turn on course switch """
            with nidaqmx.Task() as task:
                
                task.ao_channels.add_ao_voltage_chan("{}/ao1".format(daq6001))
                task.write(5.0, auto_start=True)
                print("Turning switch on")
            
            """ turn on fine current """
              
            """ turn on course current """
            
            """ wait a few seconds... """
            
            """ record spectrum """
            # SA.measureSpectrum()
            # wmean, sdev = SA.findStatistics()
            
            """ start recording """
            
            # SET UP DAQ6210 AS TASK 1
            task1 = nidaqmx.Task()
            task1.ai_channels.add_ai_voltage_chan("{}/ai7".format(daq6210), name_to_assign_to_channel='', 
                                                      terminal_config=nidaqmx.constants.TerminalConfiguration.DEFAULT, 
                                                      min_val=- 5.0, max_val=5.0, units=nidaqmx.constants.VoltageUnits.VOLTS, 
                                                      custom_scale_name='')
                
            task1.timing.cfg_samp_clk_timing(10000, source="", active_edge=nidaqmx.constants.Edge.RISING, 
                                                sample_mode=nidaqmx.constants.AcquisitionType.FINITE, samps_per_chan=10000)
            # SET UP DAQ 6001 AS TASK 2
            task2 = nidaqmx.Task()
            task2.ao_channels.add_ao_voltage_chan("{}/ao1".format(daq6001))
            
            
            print("recording...")
            
            
            print("writing voltage")
            
            
            task1.start()
            time.sleep(0.1)
            task2.write(0.0, auto_start=True)
            data = task1.read(10000,1.0)
            
            task1.close()
            task2.close()
            
            # print(data)
            
                
                
                
            """ flip switch off """
   
            """ turn off course current """             
   
        plt.plot(data)
       
    except KeyboardInterrupt:
        print('Interrupted')
    
    finally:
        """ turn laser off """
        
        # SA.close()

        print('Done!')
    
    
    return

def setCurrent(current):
    print("Setting current to {} A.".format(current))
    return

def getData():
    
    return 10, 5

if __name__=="__main__":
    main()