import os
import sys
import time
import busio
import digitalio
import board
import numpy as np
import csv
import adafruit_mcp3xxx.mcp3008 as MCP
from adafruit_mcp3xxx.analog_in import AnalogIn
from matplotlib import pyplot as plt

# pi output imports
import RPi.GPIO as GPIO
import board
import busio
import adafruit_mcp4725

try:
    FILENAME = sys.argv[1]
except IndexError:
    FILENAME = input("Enter filename.\n")

OUTPUT = 2.0        # Volts
DURATION = 300       # seconds

VS = 5.79           # Volts
R1 = 145            # Ohms
# steinhart-hart coefficients
K0 = 0.00113414
K1 = 0.000233106
K2 = 9.32975E-8


# DAC SET-UP
# to use physical board pin numbers
GPIO.setmode(GPIO.BCM)
# to set up a channel as an output
channel = 16 # GPIO 16
GPIO.setup(channel, GPIO.OUT)
# set the output state of a GPIO pin
GPIO.output(channel, GPIO.HIGH)
# Initialize I2C bus.
i2c = busio.I2C(3, 2)
# Initialize MCP4725 - DAC
dac = adafruit_mcp4725.MCP4725(i2c, address=0x60)
# Set pin output to desired voltage value
dac.normalized_value = OUTPUT/3.55

# ADC SET-UP
# create the spi bus
spi = busio.SPI(clock=board.SCK, MISO=board.MISO, MOSI=board.MOSI)
# create the cs (chip select)
cs = digitalio.DigitalInOut(board.D22)
# create the mcp object MCP3008 - ADC
mcp = MCP.MCP3008(spi, cs)
# create an analog input channel on pin 0
chan0 = AnalogIn(mcp, MCP.P0)

# begin reading
start_time = time.time()

last_read = 0       # this keeps track of the last value
tolerance = 250     # to keep from being jittery we'll only change
                    # volume when the pot has moved a significant amount
                    # on a 16-bit ADC


tempList = []       # creates an empty list of temperature values read
timeList = []       # creates an empty list of time values per temperature

def convert_V_to_T(Vout):
    # takes a voltage value from amplifier to ADC
    # maps to internal resistance of thermistor
    # calculates temperature in Celcius and Fahrenheit from Steinhart-Hart Equation
    # returns temperature value in Fahrenheit

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

def remap_range(value, left_min, left_max, right_min, right_max):
    # this remaps a value from original (left) range to new (right) range
    # Figure out how 'wide' each range is
    left_span = left_max - left_min
    right_span = right_max - right_min

    # Convert the left range into a 0-1 range (int)
    valueScaled = int(value - left_min) / int(left_span)

    # Convert the 0-1 range into a value in the right range.
    return int(right_min + (valueScaled * right_span))

def graphData(dataList, timeList):
    # creates csv file to write data to
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
    therm_changed = False

    # read the analog pin
    therm = chan0.value

    # how much has it changed since the last read?
    therm_adjust = abs(therm - last_read)

    if therm_adjust > tolerance:
        therm_changed = True

    # convert 16bit adc0 (0-65535) thermistor read into 0-5.2V voltage value
    #set_voltage = remap_range(therm, 0, 65535, 0, 5.61)

    volts2 = (chan0.value*VS)/(65535) # DO i need both of these -- this ones not good for range 1-5V

    degrees_f = round(convert_V_to_T(volts2), 2)
    elapsed_time = round(time.time() - start_time, 2)

    tempList.append(degrees_f)
    timeList.append(elapsed_time)

    # print statements to console
    print('Raw ADC Value: ', chan0.value)
    #print('Raw Converted Voltage: ', str(set_voltage) + ' Volts')
    print('Raw Converted Voltage2: ', str(volts2) + ' Volts')
    print('Time: ', str(elapsed_time) + ' seconds')
    print()

    # save the thermistor reading for the next loop
    last_read = therm

    # hang out and do nothing for a half second
    time.sleep(0.5)

    # end program after specified time in seconds
    if elapsed_time > DURATION:
        break

# done with library, free up resources & return back to default
GPIO.cleanup()
graphData(tempList, timeList)