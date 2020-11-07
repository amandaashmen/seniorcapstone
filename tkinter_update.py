#LED file

#from tkinter import *
import tkinter as tk
#import tkinter.font
from gpiozero import LED

win=tk.TK()
win.title("Using tkinter")
myFont=tkinter.font.Font(family = 'Helvetica', size=12, weight = "bold")
led = LED(21)

def ledToggle():
    if led.is_lit:
        led.off()
        ledButton["text"]="Turn LED On"
    else:
        led.on()
        ledButton["text"]="Turn LED Off"

def exitProgram():
    win.quit()

ledButton=tk.Button(win, text='Turn LED On', font=myFont, command=ledToggle, bg='bisque2', height=1, width=24)
ledButton.grid(row=0, sticky=tk.NSE)
exitButton=tk.Button(win, text='Exit', font=myFont, command=exitProgram, bg='cyan', height=1, width=6)
exitButton.grid(row=1, sticky=tk.E)

tk.mainloop()