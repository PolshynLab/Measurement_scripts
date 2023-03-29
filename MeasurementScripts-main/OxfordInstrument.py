# Oxford fridge 
# Read Probe Temperature
# Read Pressure

import labrad
import numpy as np
import time
import msvcrt
import os
import re
from datetime import datetime, timedelta   # Usd for local time

# Data Vault initilization
cxn = labrad.connect()
DV = cxn.data_vault    

# Oxford temperature control initialization
cxn1 = labrad.connect()
OxFridge = cxn1.mercury_itc_server
OxFridge.select_device()

cxn2 = labrad.connect()
OxMag = cxn2.mercury_ips_server
OxMag.select_device()

# Name and path of data file, the prefix is D:\Data
file_path = 'Ox_Instrument_Troubleshoot'
file_name = 'Ox_Instrument_Troubleshoot'
#file_name_pressure = 'Ox_ITC_P'

# Some constants
T = 180 # The time constant determines how long we read temperature of the probe, unit second
number_of_Time_points = 3000
number_of_independents = 2
number_of_dependents = 5

print("Program starts ...")

# Funtion to save Temperature data
Loop = np.arange(number_of_Time_points)
data = np.zeros(number_of_independents+number_of_dependents)  # Initilize the data

Real_time_begin = datetime.now()
matlab_datenum_base = datetime(1,1,1,0,0,0)
def datenum(Real_time):
    return (Real_time - matlab_datenum_base + timedelta(days=2)).total_seconds()/86400 + 365  # I just notice that this program needs to compenstated by the constant 365

def main():
    # Create a new file to store data
    try:
        DV.mkdir(file_path)
        DV.cd(file_path)
    except Exception:
        DV.cd(file_path)

    DV.new(file_name,('T[s]','Matlab_T'),("probeT[K]","P[m]","Mag_T(K)","PT1(K)","PT2(K)"))

    print("T[s]   Matlab_datenum   probeT[K]    P[m]    Mag_T(K)    PT1(K)    PT2(K)")

    for i in Loop:
        t = i*T

        Real_time = datetime.now()
        Matlab_time = datenum(Real_time)
        #Real_time_string = Real_time.strftime("%Y:%m:%d:%H:%M:%S")  # Stringfy the date struct
        #Real_time_array = re.findall('\d+',Real_time_string)  # Find the number in the string

        data[0] = t
        data[1] = Matlab_time          # Year

        data[2] = OxFridge.probe_temperature_read()    # Use the functions in Labrad
        P = re.findall("\d+\.\d+",OxFridge.read_pressure())   # Extract the number to string and write it to array
        data[3] = P[0]
        data[4] = OxMag.read_magnet_temperature()
        data[5] = OxMag.read_pt1_temperature()
        data[6] = OxMag.read_pt2_temperature()

        print(data[0:-1])
        DV.add(data)    # Write data to file by data vault

        time.sleep(T)

        # catching  interruption ESC
        if msvcrt.kbhit():
            if ord(msvcrt.getch()) == 27:
                print ('Interrupting the cycle...')
                break


    print("Real time reading finished")
    print("Reading probe temperature, pressure, magnet temperature, temperature of PT1, PT2 finished")
    #print(Time_temperature)

main()




