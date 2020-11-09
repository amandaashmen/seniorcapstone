import os
import time
import busio
import digitalio
import board
import numpy as np
import adafruit_mcp3xxx.mcp3008 as MCP
from adafruit_mcp3xxx.analog_in import AnalogIn
import pandas
import csv

# steinhart-hart coefficients
K0 = 0.00113414
K1 = 0.000233106
K2 = 9.32975E-8

# create the spi bus
spi = busio.SPI(clock=board.SCK, MISO=board.MISO, MOSI=board.MOSI)

# create the cs (chip select)
cs = digitalio.DigitalInOut(board.D22)

# create the mcp object
mcp = MCP.MCP3008(spi, cs)

# create an analog input channel on pin 0
chan0 = AnalogIn(mcp, MCP.P0)

# begin reading
start_time = time.time()

print('Raw ADC Value: ', chan0.value)
print('ADC Voltage: ' + str(chan0.voltage) + 'V')

last_read = 0       # this keeps track of the last value
tolerance = 250     # to keep from being jittery we'll only change
                    # volume when the pot has moved a significant amount
                    # on a 16-bit ADC


tempList = []       # creates an empty list of temperature values read
timeList = []       # creates an empty list of time values per temperature

def convert_V_to_T(V):
    # takes a voltage value from amplifier to ADC
    # maps to internal resistance of thermistor
    # calculates temperature in Celcius and Fahrenheit from Steinhart-Hart Equation
    # returns temperature value in Fahrenheit

    # voltage to resistance
    R = (5.2*100)/(.5*V + 2.6) - 100            

    # resistance to temperature
    term1 = K0
    term2 = K1*(np.log(1000*R))
    term3 = K2*(np.log(1000*R))**3
    c = (term1 + term2 + term3)**(-1) - 273.15  # degrees celcius
    f = c*(9/5) + 32                            # degrees fahrenheit

    #print formatting
    print('{:.3f}'.format(c) + "C")
    print('{:.3f}'.format(f) + "F")

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
    filename = 'temp.csv'
    with open(filename, mode='w', newline= '') as data:
            tempData = csv.writer(data, quoting=csv.QUOTE_MINIMAL)
            tempData.writerow(["Time    Temperature"])

    for point in range(len(dataList)):
        temp = dataList[point]
        time = timeList[point]

        xList.append(temp)
        yList.append(time)
        tempData.writerow([time, temp])

    evalAxis = np.linspace(0, time.time(), min(map(len, runList))-1)

    plt.xlabel('Temperature (F)')
    plt.ylabel('Time')
    plt.title('Thermistor Values')
    plot(evalAxis, minList, label='min'+name)
    legend()


while True:
    # we'll assume that the thermistor didn't move
    therm_changed = False

    # read the analog pin
    therm = chan0.value

    # how much has it changed since the last read?
    therm_adjust = abs(therm - last_read)

    if therm_adjust > tolerance:
        therm_changed = True

    if therm_changed:
        # convert 16bit adc0 (0-65535) thermistor read into 0-5.2V voltage value
        set_voltage = remap_range(therm, 0, 65535, 0, 5.2)
    
        volts = (chan0.value*5.22)/65535

        # set OS volume playback volume
        print('Voltage = {voltage}%' .format(voltage = set_voltage))
        print('Raw ADC Value: ', chan0.value)
        print('Raw Voltage: ', chan0.voltage)
        #print('Raw converted: ', volts)
        #f = convert_V_to_T(volts)
        f = chan0.voltage
        tempList.append(f)
        timeList.append(time.time()-start_time)
        print(tempList)
        print(timeList)

        # save the thermistor reading for the next loop
        last_read = therm

    # hang out and do nothing for a half second
    time.sleep(0.5)
    elapsed_time = time.time() - start_time
    if elapsed_time > 15:
        break

graphData(tempList, timeList)

    
