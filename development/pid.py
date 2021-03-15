############################################################################################
#
# PID algorithm to take input thermistor readings, and target requirements, and
# as a result feedback a new voltage output.
#
############################################################################################
class PID:

	def __init__(self, p_gain, i_gain, d_gain, now):
		self.last_error = 0.0
		self.last_time = now

		self.p_gain = p_gain
		self.i_gain = i_gain
		self.d_gain = d_gain

		self.i_error = 0.0


	def Compute(self, input, target, now):
		dt = (now - self.last_time)

		#---------------------------------------------------------------------------
		# Error is what the PID alogithm acts upon to derive the output
		#---------------------------------------------------------------------------
		error = target - input

		#---------------------------------------------------------------------------
		# The proportional term takes the distance between current input and target
		# and uses this proportially (based on Kp) to control the ESC pulse width
		#---------------------------------------------------------------------------
		p_error = error

		#---------------------------------------------------------------------------
		# The integral term sums the errors across many compute calls to allow for
		# external factors like wind speed and friction
		#---------------------------------------------------------------------------
		self.i_error += (error + self.last_error) * dt
		i_error = self.i_error

		#---------------------------------------------------------------------------
		# The differential term accounts for the fact that as error approaches 0,
		# the output needs to be reduced proportionally to ensure factors such as
		# momentum do not cause overshoot.
		#---------------------------------------------------------------------------
		d_error = (error - self.last_error) / dt

		#---------------------------------------------------------------------------
		# The overall output is the sum of the (P)roportional, (I)ntegral and (D)iffertial terms
		#---------------------------------------------------------------------------
		p_output = self.p_gain * p_error
		i_output = self.i_gain * i_error
		d_output = self.d_gain * d_error

		#---------------------------------------------------------------------------
		# Store off last input for the next differential calculation and time for next integral calculation
		#---------------------------------------------------------------------------
		self.last_error = error
		self.last_time = now

		#---------------------------------------------------------------------------
		# Return the output, which has been tuned to be the increment / decrement in ESC PWM
		#---------------------------------------------------------------------------
		return p_output, i_output, d_output


############################################################################################
#
#  Class for managing each blade + motor configuration via its ESC
#
############################################################################################
class PELTIER:

	def __init__(self, pin):
		#---------------------------------------------------------------------------
		# The GPIO numbered pin providing output voltage to Peltier
		#---------------------------------------------------------------------------
		self.bcm_pin = pin

		#---------------------------------------------------------------------------
		# range of output voltage values to Peltier from RPi
		#---------------------------------------------------------------------------
		self.min_voltage = 0
		self.max_voltage = 3.3

		#---------------------------------------------------------------------------
		# Initialize voltage output to Peltier
		#---------------------------------------------------------------------------
		output_voltage = self.min_voltage

		#---------------------------------------------------------------------------
		# Initialize the RPIO DMA PWM for the THERMOSTAT.								## FIX
		#---------------------------------------------------------------------------
		PWM.add_channel_pulse(RPIO_DMA_CHANNEL, self.bcm_pin, 0, pulse_width)			## FIX

	def update(self, temp_out):
		output_voltage = int(self.min_voltage + temp_out)
		
		# windup guard
		if output_voltage < self.min_voltage:
			output_voltage = self.min_voltage
		if output_voltage > self.max_voltage:
			output_voltage = self.max_voltage

		PWM.add_channel_pulse(RPIO_DMA_CHANNEL, self.bcm_pin, 0, pulse_width)			## FIX

temp_pid = PID(P_GAIN, I_GAIN, D_GAIN, time_now)
peltier = PELTIER(RPIO_THERMOSTAT_PWM) 													## FIX

[p_out, i_out, d_out] = temp_pid.Compute(thermistor, TARGET, time_now)					## FIX
pid_out = p_out + i_out + d_out
PELTIER.update(pid_out)