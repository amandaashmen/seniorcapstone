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
OUTPUT = 2.0                            # Volts
MAX_DAC_OUTPUT = 3.55                   # Volts
MAX_PELT_OUTPUT = 2.5
DURATION = 300                          # seconds
VS = 5.79                               # Volts
R1 = 145                                # Ohms
# steinhart-hart coefficients
K0 = 0.00113414
K1 = 0.000233106
K2 = 9.32975E-8

## DAC SET-UP
i2c = busio.I2C(3, 2)                                                # Initialize I2C bus: 3 = scl pin, 2 = sda pin
dac = DAC.MCP4725(i2c, address=0x60)                                 # Initialize MCP4725 - DAC

## ADC SET-UP
spi = busio.SPI(clock=board.SCK, MISO=board.MISO, MOSI=board.MOSI)   # create the spi bus
cs = digitalio.DigitalInOut(board.D22)                               # create the chip select
mcp = MCP.MCP3008(spi, cs)                                           # create the mcp object MCP3008 - ADC
chan0 = AnalogIn(mcp, MCP.P0)                                        # create an analog input channel on pin 0

## PID SET-UP
TARGET = 50                             # degrees
SAMPLE_TIME = .5                        # seconds
pelt_pid = PID(0.0, 0.0, 0.0, TARGET)   # create PID object

start_time = time.time()        # begin reading
last_read = 0                   # this keeps track of the last value to keep from
tolerance = 250                 # being jittery we'll only change voltage when the 
                                # thermistor has moved a significant amount on a 16-bit ADC
                        
tempList = []                   # creates an empty list of temperature values read
timeList = []                   # creates an empty list of time values per temperature

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

def adc_voltage(adc_counts):
    """Converts 16bit adc0 (0-65535) thermistor reading to 0-VS voltage value."""
    adc_16bit = 65535
    volts = (adc_counts*VS)/(adc_16bit)

def graphData(dataList, timeList):
    """Creates csv file to write data to."""

    with open(FILENAME, mode='w', newline= '') as data:
            tempData = csv.writer(data, quoting=csv.QUOTE_MINIMAL)
            tempData.writerow(["Time,    Temperature"])

            xList = []
            yList = []
            for point in range(len(dataList)):
                temp = dataList[point]
                time = timeList[point]

                xList.append(time)
                yList.append(temp)
                tempData.writerow([time,temp])

    plt.ylabel('Temperature (F)')
    plt.xlabel('Time (s)')
    plt.title('Thermistor Values')
    plt.plot(xList, yList)
    plt.savefig(FILENAME+'.png')
    plt.show()

def ctrlfunc():
    counter = 0
    pelt_pid.setSampleTime(SAMPLE_TIME)
    pelt_pid.setSetPoint(TARGET)

    while True:
        starttime = time.time()
        counter = counter + 1

        therm_changed = False                           # we'll assume that the thermistor didn't move

        therm = chan0.value                             # read the analog pin

        therm_adjust = abs(therm - last_read)           # how much has it changed since the last read?

        if therm_adjust > tolerance:
            therm_changed = True

        if therm_changed:
            volts = adc_voltage(therm) 

            degrees_f = round(convert_V_to_T(volts), 2)
            elapsed_time = round(time.time() - start_time, 2)

            tempList.append(degrees_f)
            timeList.append(elapsed_time)

            # print statements to console
            print('Raw ADC Value: ', therm)
            print('Raw Converted Voltage: ', str(volts) + ' Volts')
            print('Time: ', str(elapsed_time) + ' seconds\n')

            last_read = therm                           # save the thermistor reading for the next loop

        if counter == 50:
            pelt_pid.update(degrees_f)                                       # update pid system with current thermistor temperature
            target_voltage = pelt_pid.output                               
            dac_out = max(min(target_voltage, MAX_PELT), 0)                  # scales output to maximum voltage peltier can handle
            dac.normalized_value = dac_out/MAX_DAC_OUTPUT                    # Set pin output to desired voltage value

        # end program after specified time in seconds
        if elapsed_time > DURATION:
            break
   
        time.sleep(0.5)                                 # hang out and do nothing for a half second
        graphData(tempList, timeList)


# Main function
if __name__ == "__main__":
    ctrlfunc()