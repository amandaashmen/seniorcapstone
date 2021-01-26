import RPi.GPIO as GPIO

# to use physical board pin numbers
GPIO.setmode(GPIO.BOARD)

# to set up a channel as an output
channel = 36 # GPIO 16
GPIO.setup(channel, GPIO.OUT)

# set the output state of a GPIO pin
GPIO.output(channel, GPIO.HIGH)

# done with library, free up resources & return back to default 
#GPIO.cleanup()