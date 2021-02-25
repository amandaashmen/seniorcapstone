import tk_interface
import control


app = ARDapp()
app.title("ARD Interface")
app.mainloop()



app.controller.temperature 
control.setTarget(60)

## import control in the interface
## set the target temp using the setTemp() function in controller
## fed that in ith the controller.temp attribute at the confirm frame
## next point of communication is getting the current temp from the thermistor - should I represent as individual therm or avg
## should i make a getter function for the avg therm temp
