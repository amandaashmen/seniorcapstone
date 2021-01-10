from tkinter import *
from tkinter import font as tkFont
import tkinter.font as font

root = Tk()
root.geometry("500x300")
root.title("Tests")

# TEXT
## create ##
#myLabel = Label(root, text="Hello!")
#myLabel2 = Label(root, text="My name is Amanda")
## place  ## 
#myLabel.grid(row = 0, column = 0)
#myLabel2.grid(row = 1, column = 1)

# BUTTON
## event ##
def myClick():
    myLabel = Label(root, text="Look! I did it")
    myLabel.pack()
## create ##
myButton = Button(root, text="Click Me!", state = DISABLED)
myButton2 = Button(root, text="Click Mee!", padx=15, pady=5, command=myClick, fg="red", bg="light blue")
## place ##
#myButton.pack()
#myButton2.pack()

# INPUT FIELD
e = Entry(root, width=50, borderwidth = 5)
e.insert(0, "Enter passcode.")
e.pack()
passcode = e.get()
def myClick():
    myPasscode = Label(root, text=e.get())
    myPasscode.pack()

# EXIT
button_quit = Button(root, text="Exit", command = root.quit)
button_quit.pack()

# tests
helv36 = tkFont.Font(family='Helvetica', size=86, weight=tkFont.BOLD)
myButton2 = Button(text='btn1', font=helv36)
button3 = Button(root, text='My Button', bg='#0052cc', fg='#ffffff')
button = Button(root, text='Submit', bg='#0052cc', fg='#ffffff', command = myClick, height = 20, width = 20)
myFont = font.Font(size=19)
button['font'] = myFont
button.pack()
#button.grid(row = 0, column = 0)
#button3.grid(row = 1, column = 3)

root.mainloop()