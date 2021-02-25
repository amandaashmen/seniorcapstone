# i am not sure if i need moving average
# initializing degrees f if using tolerance
# not sure if i need counter
import os
import sys
import csv
import time
import busio
import board
import digitalio
import numpy as np
from pid_git import PID
import adafruit_mcp4725 as DAC
from matplotlib import pyplot as plt
import adafruit_mcp3xxx.mcp3008 as MCP
from adafruit_mcp3xxx.analog_in import AnalogIn

## SAVING TO FILENAME
try:
    FILENAME = sys.argv[1]
except IndexError:
    FILENAME = input("Enter filename.\n")

## GLOBAL VARIABLES
OUTPUT = 0                              # Volts
MAX_DAC = 3.78                          # Volts
MAX_PELT = 2.5                          # Volts
DURATION = 30                           # seconds
VS = 5.79                               # Volts
R1 = 145                                # Ohms
# steinhart-hart coefficients
K0 = 0.00113414
K1 = 0.000233106
K2 = 9.32975E-8

## DAC SET-UP
i2c = busio.I2C(3, 2)                                                # Initialize I2C bus: 3 = scl pin, 2 = sda pin
dac = DAC.MCP4725(i2c, address=0x60)                                 # Initialize first MCP4725 - DAC
dac2 = DAC.MCP4725(i2c, address=0x61)                                 # Initialize second MCP4725 - DAC

## ADC SET-UP
spi = busio.SPI(clock=board.SCK, MISO=board.MISO, MOSI=board.MOSI)   # create the spi bus
cs = digitalio.DigitalInOut(board.D22)                               # create the chip select
mcp = MCP.MCP3008(spi, cs)                                           # create the mcp object MCP3008 - ADC
chan0 = AnalogIn(mcp, MCP.P0)                                        # create an analog input channel on pin 0
chan1 = AnalogIn(mcp, MCP.P1)                                        # create an analog input channel on pin 1

## PID SET-UP
Kp = 24.0                               # proportional gain
Ki =  0.0                               # integral gain
Kd =  0.0                               # derivative gain
TARGET = 50                             # degrees
SAMPLE_TIME = .5                        # seconds
pelt_pid = PID(Kp, Ki, Kd, TARGET)      # create PID object for therm. 1
pelt_pid2 = PID(Kp, Ki, Kd, TARGET)     # create PID object for therm. 2

start_time = time.time()                # begin reading
last_read = 0                           # this keeps track of the last value to keep from
tolerance = 250                         #  being jittery we'll only change voltage when the
                                        #  thermistor has moved a significant amount on a 16-bit ADC

## GRAPH SET-UP
# thermistor 1 and 2 lists
t1_tempList = []                        # creates an empty list of temperature values read
t2_tempList = []                   
t1_timeList = []                        # creates an empty list of time values per temperature
t2_timeList = []                  
# pid lists
pidList = []                            # creates an empty list of pid outputs converted to voltage
timeList = []                          # creates an empty list of time values per pid output value
pidList2 = []                            # creates an empty list of pid outputs converted to voltage
timeList2 = []                          # creates an empty list of time values per pid output value

def convert_V_to_T(Vout):
    """
    Takes a voltage value from amplifier to ADC, maps to internal resistance of
    thermistor, calculates temperature in Celcius and Fahrenheit from
    Steinhart-Hart Equation. Returns temperature value in Fahrenheit.
    """
    # voltage to resistance
    GAIN = 2.68-0.154*Vout
    R = (VS*R1)/((1/GAIN)*Vout + (VS/2)) - R1
    print('Resistance: ', str(R) + ' kOhms')

    # resistance to temperature: Steinhart-Hart Equation
    term1 = K0
    term2 = K1*(np.log(1000*R))
    term3 = K2*(np.log(1000*R))**3
    c = (term1 + term2 + term3)**(-1) - 273.15  # degrees celcius
    f = c*(9/5) + 32                            # degrees fahrenheit

    #print formatting
    print('{:.3f}'.format(c) + " C")
    print('{:.3f}'.format(f) + " F")

    return(f)

def convert_T_to_V(temp):
    """
    Takes a target temperature value in Fahrenheit and maps to a linear equation 
    representing the steady-state voltage required to drive peltier
    to reach that desired temperature.
    Returns target voltage (Volts)
    """
    return (71-temp)/27        

def adc_voltage(adc_counts):
    """Converts 16bit adc0 (0-65535) thermistor reading to 0-VS voltage value."""
    adc_16bit = 65535
    volts = (adc_counts*VS)/(adc_16bit)
    return volts

def graphData_two(dataList1, timeList1, dataList2, timeList2):
    """Creates csv file to write data to and plots graph of data for two sets of inputs."""

    # Thermistor 1
    with open(FILENAME+"_t1", mode='w', newline= '') as data:
            tempData = csv.writer(data, quoting=csv.QUOTE_MINIMAL)
            tempData.writerow(["Time,    Temperature"])

            xList = []
            yList = []
            for point in range(len(dataList1)):
                temp = dataList1[point]
                time = timeList1[point]
    
                xList.append(time)
                yList.append(temp)
                tempData.writerow([time,temp])
                
    # Thermistor 2
    with open(FILENAME+"_t2", mode='w', newline= '') as data:
            tempData2 = csv.writer(data, quoting=csv.QUOTE_MINIMAL)
            tempData2.writerow(["Time,    Temperature"])

            xList2 = []
            yList2 = []
            for point in range(len(dataList2)):
                temp = dataList2[point]
                time = timeList2[point]
    
                xList2.append(time)
                yList2.append(temp)
                tempData2.writerow([time,temp])

    plt.ylabel('Temperature (F)')
    plt.xlabel('Time (s)')
    plt.title('Thermistor Values')
    plt.plot(xList, yList, xList2, yList2)
    plt.savefig(FILENAME+'.png')
    plt.show()

def graphData_one(dataList, timeList, file):
    """Creates csv file to write data to and plots graph of data for single input."""

    with open(file+"_pid", mode='w', newline= '') as data:
            pidData = csv.writer(data, quoting=csv.QUOTE_MINIMAL)
            pidData.writerow(["Time,    PID"])

            xList = []
            yList = []
            for point in range(len(dataList2)):
                pid = dataList2[point]
                time = timeList2[point]

                xList.append(time)
                yList.append(pid)
                pidData.writerow([time,pid])

    plt.ylabel('PID')
    plt.xlabel('Time (s)')
    plt.title('PID Values')
    plt.plot(xList, yList)
    plt.savefig(file+'_pid.png')
    plt.show()

def ctrlfunc():
    counter = 0
    pelt_pid.setSampleTime(SAMPLE_TIME)
    pelt_pid.setSetPoint(TARGET)

    while True:
        starttime = time.time()

        #therm_changed = False                          # we'll assume that the thermistor didn't move
        therm_changed = True

        therm = chan0.value                             # read the analog pin of the first thermistor
        therm2 = chan1.value                             # read the analog pin of the first thermistor

        #therm_adjust = abs(therm - last_read)           # how much has it changed since the last read?

        #if therm_adjust > tolerance:
        #    therm_changed = True

        #if therm_changed:
            
        # Thermistor 1
        volts = adc_voltage(therm)
        degrees_f = round(convert_V_to_T(volts), 2)
        elapsed_time = round(time.time() - start_time, 2)

        t1_tempList.append(degrees_f)
        t1_timeList.append(elapsed_time)

        # Thermistor 2
        volts2 = adc_voltage(therm2)
        degrees_f2 = round(convert_V_to_T(volts2), 2)
        elapsed_time2 = round(time.time() - start_time, 2)

        t2_tempList.append(degrees_f2)
        t2_timeList.append(elapsed_time2)
                 
        # Print statements to console
        print('T1 Raw ADC Value: ', therm)
        print('T1 Raw Converted Voltage: ', str(volts) + ' Volts')
        print('T1 Time: ', str(elapsed_time) + ' seconds\n')
        
        print('T2 Raw ADC Value: ', therm2)
        print('T2 Raw Converted Voltage: ', str(volts2) + ' Volts')
        print('T2 Time: ', str(elapsed_time2) + ' seconds\n')
            
        #last_read = therm                           # save the thermistor reading for the next loop

        if counter == 5:                             # Sample time (.5) / Max process time (.1)
            
            # Thermistor 1
            pelt_pid.update(degrees_f)                                       # update pid system with current thermistor temperature
            target_out_temp = pelt_pid.output
            dac_out = max(min(convert_T_to_V(target_out_temp), MAX_PELT), 0) # scales output to maximum voltage peltier can handle
            dac.normalized_value = dac_out/MAX_DAC                           # set pin output to desired voltage value
            
            pidList.append(target_out_temp)
            timeList.append(elapsed_time)
            
            # Thermistor 2
            pelt_pid2.update(degrees_f2)                                       # update pid system with current thermistor temperature
            target_out_temp2 = pelt_pid2.output
            dac_out2 = max(min(convert_T_to_V(target_out_temp2), MAX_PELT), 0) # scales output to maximum voltage peltier can handle
            dac2.normalized_value = dac_out2/MAX_DAC                           # set pin output to desired voltage value
            
            pidList2.append(target_out_temp)
            timeList2.append(elapsed_time2)

            counter = 0

        # end program after specified time in seconds
        if elapsed_time > DURATION:
            graphData_two(t1_tempList, t1_timeList, t2_tempList, t2_timeList)
            graphData_one(pidList, timeList, FILENAME+'_1')
            graphData_one(pidList2, timeList2, FILENAME+'_2')
            break

        endtime = time.time()
        processTime = endtime - starttime
        sleeptime = .1 - processTime
        if sleeptime < 0:
            sleeptime = 0
        time.sleep(sleeptime)
        
        counter = counter + 1


# Main function
if __name__ == "__main__":
    ctrlfunc()
