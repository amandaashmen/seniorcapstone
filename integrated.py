############################################################################################
#
# INTEGRATED.py
# Reads an external thermistor sensor from an ADC to Raspberry Pi, converts that
# value to a temperature, plots the output to a figure & csv file, and outputs
# a voltage to a DAC chip .
#
############################################################################################
import os
import sys
import time
import busio
import digitalio
import board
import numpy as np
import csv
from matplotlib import pyplot as plt
from adafruit_mcp3xxx.analog_in import AnalogIn
import adafruit_mcp3xxx.mcp3008 as MCP
import adafruit_mcp4725 as DAC

## SAVING TO FILENAME
try:
    FILENAME = sys.argv[1]
except IndexError:
    FILENAME = input("Enter filename.\n")

## GLOBAL VARIABLES
OUTPUT = 2.0                    # Volts
MAX_OUTPUT = 3.55               # Volts
DURATION = 300                  # seconds
VS = 5.79                       # Volts
R1 = 145                        # Ohms
# steinhart-hart coefficients
K0 = 0.00113414
K1 = 0.000233106
K2 = 9.32975E-8

## DAC SET-UP
#GPIO.setmode(GPIO.BCM)                                              # to use physical board pin numbers
#channel = 16                                                        # GPIO 16
#GPIO.setup(channel, GPIO.OUT)                                       # to set up a channel as an output
#GPIO.output(channel, GPIO.HIGH)                                     # set the output state of a GPIO pin
i2c = busio.I2C(3, 2)                                                # Initialize I2C bus: 3 = scl pin, 2 = sda pin
dac = DAC.MCP4725(i2c, address=0x60)                                 # Initialize MCP4725 - DAC
dac.normalized_value = OUTPUT/MAX_OUTPUT                             # Set pin output to desired voltage value

## ADC SET-UP
spi = busio.SPI(clock=board.SCK, MISO=board.MISO, MOSI=board.MOSI)   # create the spi bus
cs = digitalio.DigitalInOut(board.D22)                               # create the chip select
mcp = MCP.MCP3008(spi, cs)                                           # create the mcp object MCP3008 - ADC
chan0 = AnalogIn(mcp, MCP.P0)                                        # create an analog input channel on pin 0


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

    # resistance to temperature
    term1 = K0
    term2 = K1*(np.log(1000*R))
    term3 = K2*(np.log(1000*R))**3
    c = (term1 + term2 + term3)**(-1) - 273.15  # degrees celcius
    f = c*(9/5) + 32                            # degrees fahrenheit

    #print formatting
    print('{:.3f}'.format(c) + " C")
    print('{:.3f}'.format(f) + " F")

    return(f)


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

while True:
    # we'll assume that the thermistor didn't move
    #therm_changed = False

    # read the analog pin
    therm = chan0.value

    # how much has it changed since the last read?
    #therm_adjust = abs(therm - last_read)

    #if therm_adjust > tolerance:
    #    therm_changed = True

    #if therm_changed:
        # convert 16bit adc0 (0-65535) thermistor read into 0-VS voltage value
    adc_16bit = 65535
    volts = (therm*VS)/(adc_16bit)

    degrees_f = round(convert_V_to_T(volts), 2)
    elapsed_time = round(time.time() - start_time, 2)

    tempList.append(degrees_f)
    timeList.append(elapsed_time)

        # print statements to console
    print('Raw ADC Value: ', chan0.value)
    print('Raw Converted Voltage: ', str(volts) + ' Volts')
    print('Time: ', str(elapsed_time) + ' seconds\n')

        # save the thermistor reading for the next loop
        #last_read = therm


    # hang out and do nothing for a half second
    time.sleep(0.5)

    # end program after specified time in seconds
    if elapsed_time > DURATION:
        break

graphData(tempList, timeList)