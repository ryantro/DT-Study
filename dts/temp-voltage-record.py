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


def main():
    
    currents = [0.002, 0.004, 0.01, 0.02, 0.04, 0.08]
    emitters = [1, 2, 3, 4, 5, 6]
    arduinoCom = 'COM11'
    daq6210 = 'Dev2'
    savefolder = ''#r'N:/temp/Ryan/dT-data'
    file = 'c1.csv'
    # file = savefolder + '/' + filename
    delay = 1.0 # seconds
    print(file)
    
    try:
        while(True):
            
            """ set current to 0 """
            
            
            """ set the current emitter """
            for emitter in emitters:
                print("Turning on emitter {}.".format(emitter))
            
                """ power on laser driver """
                
                for current in currents:
                    setCurrent(current)
                    time.sleep(delay)
                
                    """ measure temperature and forward voltage """
                    with nidaqmx.Task() as task:
                        task.ai_channels.add_ai_thrmcpl_chan("{}/ai1".format(daq6210),name_to_assign_to_channel="", min_val=0.0,
                                                         max_val=100.0, units=nidaqmx.constants.TemperatureUnits.DEG_C,
                                                         thermocouple_type=nidaqmx.constants.ThermocoupleType.J,
                                                         cjc_source=nidaqmx.constants.CJCSource.CONSTANT_USER_VALUE, cjc_val=27.0,
                                                         cjc_channel="")
                        
                        
                        task.ai_channels.add_ai_voltage_chan("{}/ai7".format(daq6210), name_to_assign_to_channel='', 
                                                             terminal_config=nidaqmx.constants.TerminalConfiguration.DEFAULT, 
                                                             min_val=- 5.0, max_val=5.0, units=nidaqmx.constants.VoltageUnits.VOLTS, 
                                                             custom_scale_name='')
                        
                        data=task.read(1,1.0)
                    
                    # Temperature
                    T = data[0][0]
                    # Voltage
                    V = data[1][0]
                    # Time
                    t = time.time()
                    
                    # Save data so csv
                    a = np.asarray([[emitter, current, t, T , V]])
                    
                    """ 
                    save data to csv
                    [emitter, current, temperature, forward voltage]
                
                    """
                    with open(file, 'a') as csvfile:
                        np.savetxt(csvfile, a, delimiter = ',')
                    
                    time.sleep(1)
                
    except KeyboardInterrupt:
        print('Interrupted')
    
    finally:
        """ turn laser off """
        

        print('Done!')
    
    
    return

def setCurrent(current):
    print("Setting current to {} A.".format(current))
    return

def getData():
    
    return 10, 5

if __name__=="__main__":
    main()