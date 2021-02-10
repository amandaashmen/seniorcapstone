import time
from tkinter import *
from tkinter import messagebox


# creating Tk window
root = Tk()

# setting geometry of tk window
root.geometry("250x250")

# Using title() to display a message in
# the dialogue box of the message in the
# title bar.
root.title("Time Counter")

# Declaration of variables
hour=StringVar()
minute=StringVar()
second=StringVar()

# setting the values
minute.set("40")
second.set("00")

# Use of Entry class to take input from the user
minuteLabel= Label(root, width=3, font=("Arial",18,""), textvariable=minute)
minuteLabel.place(x=70,y=20)

secondLabel= Label(root, width=3, font=("Arial",18,""), textvariable=second)
secondLabel.place(x=130,y=20)


def submit():
    # the input provided by the user is
    # stored in here :temp
    temp = int(minute.get())*60 + int(second.get())
    while temp >-1:

        # divmod(firstvalue = temp//60, secondvalue = temp%60)
        mins,secs = divmod(temp,60)

        # using format () method to store the value up to
        # two decimal places
        minute.set("{0:2d}".format(mins))
        second.set("{0:2d}".format(secs))

        # updating the GUI window after decrementing the
        # temp value every time
        root.update()
        time.sleep(1)

        # when temp value = 0; then a messagebox pop's up
        # with a message:"Time's up"
        if (temp == 0):
            messagebox.showinfo("Time Countdown", "Time's up ")

        # after every one sec the value of temp will be decremented
        # by one
        temp -= 1


btn = Button(root, text='Go', bd='5', command= submit)
btn.place(x = 80,y = 120)

root.mainloop()