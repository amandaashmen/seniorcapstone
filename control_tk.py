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
#from scipy.interpolate import make_interp_spline, BSpline

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
Kp = 28.35                               # proportional gain
Ki =  1.48                                # integral gain
Kd =  0.0                                 # derivative gain
SAMPLE_TIME = .5                          # seconds
TARGET = 70
pelt_pid = PID(Kp, Ki, Kd, TARGET)      # create PID object for therm. 1
pelt_pid2 = PID(Kp, Ki, Kd, TARGET)     # create PID object for therm. 2
#ORIGINAL_DIFF = 0

start_time = time.time()                # begin reading
last_read = 0                           # this keeps track of the last value to keep from
tolerance = 250                         #  being jittery we'll only change voltage when the
                                        #  thermistor has moved a significant amount on a 16-bit ADC

## GRAPH SET-UP
# thermistor 1 and 2 lists
t1_tempList = []                        # creates an empty list of temperature values read
t2_tempList = []                   
timeList = []                        # creates an empty list of time values per temperature
t2_timeList = []                  


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
    #volts = adc_voltage(value)
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

    # Thermistor 1
    #xList = []
    #yList = []
    #for point in range(len(dataList1)):
    #    temp = dataList1[point]
    #    time = timeList1[point]
    
    #    xList.append(time)
    #    yList.append(temp)
               
    # Thermistor 2
    #xList2 = []
    #yList2 = []
    #for point in range(len(dataList2)):
    #temp = dataList2[point]
    #time = timeList2[point]
    
    #xList2.append(time)
    #yList2.append(temp)

    

#create data
#x = np.array([1, 2, 3, 4, 5, 6, 7, 8])
#y = np.array([4, 9, 12, 30, 45, 88, 140, 230])

    #define x as 200 equally spaced values between the min and max of original x 
    ##xnew = np.linspace(0, timeList[len(timeList)-1], len(timeList)*5) 

    #define spline
    ##spl = make_interp_spline(timeList, dataList1, k=3)
    ##y_smooth = spl(xnew)

    #create smooth line chart 
    ##plt.plot(xnew, y_smooth, label='Therm. 1')
    #plt.show()
         
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
    print(pelt.output)
    dac_out = max(min(convert_T_to_V(target_out_temp), MAX_PELT), 0)    # scales output to maximum voltage peltier can handle
    dac_no.normalized_value = dac_out/MAX_DAC                           # set pin output to desired voltage value

def ctrlfunc(starttime, counter):
    #counter = 0
    pelt_pid.setSampleTime(SAMPLE_TIME)
    pelt_pid.setSetPoint(int(TARGET))
    pelt_pid2.setSampleTime(SAMPLE_TIME)
    pelt_pid2.setSetPoint(int(TARGET))

    #starttime = time.time()

    therm = chan0.value                             # read the analog pin of the first thermistor
    therm2 = chan1.value                             # read the analog pin of the first thermistor
    
    if ORIGINAL_DIFF == 0:
       global ORIGINAL_DIFF 
       ORIGINAL_DIFF = time.time() - start_time
        
    elapsed_time = round(time.time() - start_time - ORIGINAL_DIFF, 2)   
    #minutes, seconds = divmod(elapsed_time-start_time, 60)
    #timeList.append("{:0>2}:{:05.2f}".format(int(minutes),seconds))
    print(elapsed_time)
    timeList.append(elapsed_time)
    
    # Thermistor 1
    degrees_f = adc_to_degrees(therm, 1)
    print(degrees_f)                            #remove
    t1_tempList.append(degrees_f)

    # Thermistor 2
    degrees_f2 = adc_to_degrees(therm2, 2)
    print(degrees_f2)                           # remove
    t2_tempList.append(degrees_f2)    

    #if counter % 5 == 0:                             # Sample time (.5) / Max process time (.1)
            
    # Thermistor 1
    updatePID(degrees_f, pelt_pid, dac, 1)
           
    # Thermistor 2
    updatePID(degrees_f2, pelt_pid2, dac2, 2)
        
    #counter = 0
        
    #endtime = time.time()
    #processTime = endtime - starttime
    #sleeptime = .1 - processTime
    #if sleeptime < 0:
    #    sleeptime = 0
    #time.sleep(sleeptime)
        
    #counter = counter + 1

def endProgram():
    """When called, sets DAC output to 0 to turn off peltiers and produces graph of temperatures."""
    dac.normalized_value = 0.0
    dac2.normalized_value = 0.0
    graphData(t1_tempList, t2_tempList, timeList)



