import RPi.GPIO as GPIO
import board
import busio
import adafruit_mcp4725

MIN_VOLTAGE = 0
MAX_VOLTAGE = 2.5   

# Initialize I2C bus.
i2c = busio.I2C(3, 2)

# Initialize MCP4725.
dac = adafruit_mcp4725.MCP4725(i2c, address=0x60)
dac2 = adafruit_mcp4725.MCP4725(i2c, address=0x61)

# Set the output voltage value of each DAC
dac.normalized_value = MIN_VOLTAGE/3.55
dac2.normalized_value = MIN_VOLTAGE/3.55

# There are a three ways to set the DAC output:

#dac.value = 65535                              # Use the value property with a 16-bit number just like the AnalogOut class.  Note the MCP4725 is only a 12-bit
                                                # DAC so quantization errors will occur.  The range of values is 0 (minimum/ground) to 65535 (maximum/Vout).

#dac.raw_value = 4095                           # Use the raw_value property to directly read and write the 12-bit DAC value.  The range of values is
                                                # 0 (minimum/ground) to 4095 (maximum/Vout).

#dac.normalized_value = 1.0                     # Use the normalized_value property to set the output with a floating point value in the range
                                                # 0 to 1.0 where 0 is minimum/ground and 1.0 is maximum/Vout.

# Testing loop will go up and down through the range of DAC values forever.
testing = False
while testing: 
    # Go up the 12-bit raw range.
    print("Going up 0-3.3V...")
    for i in range(4095):
        dac.raw_value = i
    # Go back down the 12-bit raw range.
    print("Going down 3.3-0V...")
    for i in range(4095, -1, -1):
        dac.raw_value = i

## TO USE GPIO PINS       
# to use physical board pin numbers
#GPIO.setmode(GPIO.BCM)

# to set up a channel as an output
#channel = 16 # GPIO 16
#GPIO.setup(channel, GPIO.OUT)

# set the output state of a GPIO pin
#GPIO.output(channel, GPIO.HIGH)

# done with library, free up resources & return back to default
#GPIO.cleanup()
