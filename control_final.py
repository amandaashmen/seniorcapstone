############################################################################################
#
# Main control algorithm to read thermistor values, calculate output signal
# needed to approach target value, and drive a voltage signal to peltiers. 
#
############################################################################################
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
VS = 5.9                                # Volts
R1 = 151.2                              # kOhms
# steinhart-hart coefficients
K0 = 0.00113414
K1 = 0.000233106
K2 = 9.32975E-8

## DAC SET-UP
i2c = busio.I2C(3, 2)                                                # Initialize I2C bus: 3 = scl pin, 2 = sda pin
dac = DAC.MCP4725(i2c, address=0x60)                                 # Initialize MCP4725 - DAC objects
dac2 = DAC.MCP4725(i2c, address=0x61)                               
dac.normalized_value = 0                                             # Initialize DAC outputs to 0 Volts
dac2.normalized_value = 0

## ADC SET-UP
spi = busio.SPI(clock=board.SCK, MISO=board.MISO, MOSI=board.MOSI)   # create the spi bus
cs = digitalio.DigitalInOut(board.D22)                               # create the chip select
mcp = MCP.MCP3008(spi, cs)                                           # create the mcp object MCP3008 - ADC
chan0 = AnalogIn(mcp, MCP.P0)                                        # create an analog input channel on pin 0
chan1 = AnalogIn(mcp, MCP.P1)                                        # create an analog input channel on pin 1
ADC_MAX = 65535

## PID SET-UP
Kp = 28.35                              # proportional gain
Ki =  1.48                              # integral gain
Kd =  0.0                               # derivative gain
SAMPLE_TIME = .5                        # seconds
TARGET = 70                             # Fahrenheit
pelt_pid = PID(Kp, Ki, Kd, TARGET)      # create PID object for therm. 1
pelt_pid2 = PID(Kp, Ki, Kd, TARGET)     # create PID object for therm. 2

## GRAPH SET-UP
DIFF = 0                                # seconds
start_time = time.time()                # begin reading
t1_tempList = []                        # creates an empty list of temperature values read
t2_tempList = []                   
timeList = []                           # creates an empty list of time values per temperature


def adc_voltage(adc_counts):
    """Converts 16bit adc0 (0-65535) thermistor reading to 0-VS voltage value."""
    adc_16bit = 65535
    volts = (adc_counts*VS)/(adc_16bit)
    return volts

def convert_V_to_T(adc_value, therm):
    """
    Takes a voltage value from amplifier to ADC, maps to internal resistance of
    thermistor, calculates temperature in Celcius and Fahrenheit from
    Steinhart-Hart Equation. Prints Resistance (kOhms) and Temperature (F).
    Returns temperature value in Fahrenheit.
    """
    if therm == 1:
        GAIN = 2.754-1.041*(adc_value/ADC_MAX)
    else:
        GAIN = 2.766-1.006*(adc_value/ADC_MAX)
    Vout = adc_voltage(adc_value)
    R = (VS*R1)/((1/GAIN)*Vout + (VS/2)) - R1

    # resistance to temperature: Steinhart-Hart Equation
    term1 = K0
    term2 = K1*(np.log(1000*R))
    term3 = K2*(np.log(1000*R))**3
    c = (term1 + term2 + term3)**(-1) - 273.15  # degrees celcius
    f = c*(9/5) + 32                            # degrees fahrenheit

    return(f)   

def adc_to_degrees(value, therm):
    """
    Given a value from an ADC, converts value to voltage then 
    converts that voltage to temperature in Fahrenheit.
    Returns rounded value in degrees F.
    """
    return round(convert_V_to_T(value, therm), 2)

def convert_T_to_V(temp):
    """
    Takes a target temperature value in Fahrenheit and maps to a linear equation 
    representing the steady-state voltage required to drive peltier
    to reach that desired temperature.
    Returns target voltage (Volts)
    """
    return (71-temp)/10.4     

def graphData(dataList1, dataList2, timeList):
    """plots graph of data for two sets of inputs."""   
    plt.ylabel('Temperature (F)')
    plt.xlabel('Time (s)')
    plt.title('Thermistor Values')
    plt.plot(timeList, dataList1, label='Therm. 1')
    plt.plot(timeList, dataList2, label='Therm. 2')        
    plt.legend()
    plt.savefig(FILENAME+'.png')
    plt.show()
    
def getAverage():
    """ 
    Returns the average temperature of the two thermistors
    """
    degrees_f1 = adc_to_degrees(chan0.value, 1)
    degrees_f2 = adc_to_degrees(chan1.value, 2)
    return (degrees_f1+degrees_f2)/2

def setTarget(temp):
    """ 
    Sets the target temperature for the system to approach.
    """
    global TARGET
    TARGET = int(temp) +1.5    # Fudge Factor remove if necessary
    
def updatePID(current_temp, pelt, dac_no, therm):
    """
    Given degrees of a thermistor in Fahrenheit, sets the PID system to 
    compute a new output target temperature, which is converted to a 
    voltage to drive the peltier unit. 
    """
    pelt.update(current_temp)                                           # update pid system with current thermistor temperature
    target_out_temp = pelt.output
    dac_out = max(min(convert_T_to_V(target_out_temp), MAX_PELT), 0)    # scales output to maximum voltage peltier can handle
    dac_no.normalized_value = dac_out/MAX_DAC                           # set pin output to desired voltage value

def ctrlfunc(starttime, counter):
    pelt_pid.setSampleTime(SAMPLE_TIME)
    pelt_pid.setSetPoint(int(TARGET))
    pelt_pid2.setSampleTime(SAMPLE_TIME)
    pelt_pid2.setSetPoint(int(TARGET))

    therm = chan0.value                             # read the analog pin of the first thermistor
    therm2 = chan1.value                             # read the analog pin of the first thermistor
    
    global DIFF
    if DIFF == 0:
       global ORIGINAL_DIFF 
       DIFF = time.time() - start_time
    
    DIFF = 0
    elapsed_time = round(time.time() - start_time - DIFF, 2)   
    minutes, seconds = divmod(elapsed_time-start_time, 60)
    print("Time elapsed")
    print(elapsed_time)
    timeList.append(elapsed_time)
    
    # Thermistor 1
    degrees_f = adc_to_degrees(therm, 1)
    print("Therm. 1")
    print(degrees_f)                            #remove
    t1_tempList.append(degrees_f)

    # Thermistor 2
    degrees_f2 = adc_to_degrees(therm2, 2)
    print("Therm. 2")
    print(degrees_f2)                           # remove
    t2_tempList.append(degrees_f2)    
            
    # Thermistor 1
    updatePID(degrees_f, pelt_pid, dac, 1)
           
    # Thermistor 2
    updatePID(degrees_f2, pelt_pid2, dac2, 2)
        
def endProgram():
    """When called, sets DAC output to 0 to turn off peltiers and produces graph of temperatures."""
    dac.normalized_value = 0.0
    dac2.normalized_value = 0.0
    graphData(t1_tempList, t2_tempList, timeList)
