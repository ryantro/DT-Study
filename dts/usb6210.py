# -*- coding: utf-8 -*-
"""
Created on Wed Jul 27 16:20:34 2022

@author: ryan.robinson
"""

import nidaqmx.system
from nidaqmx.constants import LineGrouping


import time

with nidaqmx.Task() as task:
    task.ai_channels.add_ai_thrmcpl_chan("Dev2/ai1",name_to_assign_to_channel="", min_val=0.0,
                                     max_val=100.0, units=nidaqmx.constants.TemperatureUnits.DEG_C,
                                     thermocouple_type=nidaqmx.constants.ThermocoupleType.J,
                                     cjc_source=nidaqmx.constants.CJCSource.CONSTANT_USER_VALUE, cjc_val=27.0,
                                     cjc_channel="")
    
    
    task.ai_channels.add_ai_voltage_chan("Dev2/ai7", name_to_assign_to_channel='', 
                                         terminal_config=nidaqmx.constants.TerminalConfiguration.DEFAULT, 
                                         min_val=- 5.0, max_val=5.0, units=nidaqmx.constants.VoltageUnits.VOLTS, 
                                         custom_scale_name='')
    
    task.timing.cfg_samp_clk_timing(1000, source="", active_edge=nidaqmx.constants.Edge.RISING, 
                                    sample_mode=nidaqmx.constants.AcquisitionType.FINITE, samps_per_chan=1000)
    
    ts = time.time()
    
    
    data=task.read(1000,1.0)
    tf = time.time() - ts
    
    
    
    print(data)
    
    print(tf)
    
    # for i in range(0,20):
    #     data=task.read(5,1.0)
    #     print(data)
    #     print(time.time() - ts)
    #     # print(data[0])
    #     # time.sleep(1)

