import time
from tkinter import *
from tkinter import messagebox

LARGE_FONT= ("Verdana bold", 15)
SMALL_FONT= ("Verdana italic", 13)
PASSWORD = "U"

class ARDapp(Tk):

    def __init__(self, *args, **kwargs):

        Tk.__init__(self, *args, **kwargs)
        container = Frame(self)
        container.pack(side="top", fill="both", expand = True)

        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        # shared variables across frames
        self.temperature = StringVar()
        self.duration = StringVar()

        self.frames = {}

        for F in (StartPage, Modes, Locked, Custom, Confirm, EndPage):

            frame = F(container, self)

            self.frames[F] = frame

            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame(StartPage)

    def show_frame(self, cont):
        frame = self.frames[cont]
        frame.tkraise()

class StartPage(Frame):

    def __init__(self, parent, controller):
        Frame.__init__(self, parent)
        label = Label(self, text="Welcome to the \nAthletic Recovery Device", font= "Verdana 20 bold")
        label2 = Label(self, text="Ready to Recover?", fg="navy", font='Helvetica 15 italic')
        label.pack(pady=23, padx=10)
        label2.pack(pady=10)

        button = Button(self, text="Start", bg='#8B0000', fg='#ffffff', command=lambda: controller.show_frame(Modes))
        button.configure(font='Helvetica 15 bold')
        button.configure(borderwidth=3)
        button.pack(pady=30)

class Modes(Frame):

    def __init__(self, parent, controller):
        Frame.__init__(self, parent)
        label = Label(self, text="Select Treatment Mode", font=LARGE_FONT)
        label.pack(pady=10,padx=10)

        presetA = Button(self, text="Preset A: 40F for 20 minutes", command=lambda: controller.show_frame(Confirm))
        presetA.configure(font='Helvetica 13')
        presetA.pack(pady=15)

        presetB = Button(self, text="Preset B: 45F for 15 minutes", command=lambda: controller.show_frame(Confirm))
        presetB.configure(font='Helvetica 13')
        presetB.pack(pady=15)

        presetC = Button(self, text="Preset C: 40F for 10 minutes", command=lambda: controller.show_frame(Confirm))
        presetC.configure(font='Helvetica 13')
        presetC.pack(pady=15)

        custom = Button(self, text="Custom Setting", width = 24, command=lambda: controller.show_frame(Locked))
        custom.configure(font='Helvetica 13')
        custom.pack(pady=15)

class Locked(Frame):

    def __init__(self, parent, controller):
        Frame.__init__(self, parent)

        def checkPass():
            if passEntry.get() == PASSWORD:
                controller.show_frame(Custom)
            else:
                messagebox.showinfo("Password Entry", "Incorrect: Try Again")

        title = Label(self, text="Enter Password", font=LARGE_FONT)
        title.pack(pady=10,padx=10)

        passEntry= Entry(self, width=15, font=("Arial",18,""))
        passEntry.pack(pady=10,padx=10)

        back = Button(self, text="Back", command=lambda: controller.show_frame(Modes))
        back.pack(pady=10,padx=10)

        submit = Button(self, text="Submit", command=checkPass)
        submit.pack(pady=10,padx=10)

class Custom(Frame):

    def __init__(self, parent, controller):
        Frame.__init__(self, parent)
        label = Label(self, text="Custom Setting", font=LARGE_FONT)
        label.pack(pady=10,padx=10)

        set_temp = StringVar()
        set_dur = StringVar()

        # Once the Submit button is pressed, this function will execute
        def set_variables():
            controller.temperature.set(set_temp.get())
            controller.duration.set(set_dur.get())
            controller.show_frame(Confirm)

        temp_set = Label(self, text="Set Temperature (F)", font=SMALL_FONT)
        temp_set.place(x=70,y=90)

        time_set = Label(self, text="Set Duration (min.)", font=SMALL_FONT)
        time_set.place(x=70,y=130)

        tempEntry= Entry(self, width=3, font=("Arial",18,""), textvariable=set_temp)
        tempEntry.place(x=260,y=90)

        timeEntry= Entry(self, width=3, font=("Arial",18,""), textvariable=set_dur)
        timeEntry.place(x=260,y=130)

        back = Button(self, text="Back", command=lambda: controller.show_frame(Locked))
        back.place(x=100,y=200)

        submit = Button(self, text="Submit", command=set_variables)
        submit.place(x=250,y=200)


class Confirm(Frame):
    def __init__(self, parent, controller):
        Frame.__init__(self, parent)

        minute = StringVar()
        second = StringVar()
        minute.set(controller.duration.get())
        second.set("00")

        current_temp = Label(self, text="Current Temperature: 70", font=SMALL_FONT)
        current_temp.place(x=100,y=110)

        desired_temp = Label(self, text="Desired temperature: ", font=SMALL_FONT)
        desired_temp.place(x= 100, y = 140)

        tempLabel = Label(self, font=SMALL_FONT, textvariable= controller.temperature)
        tempLabel.place(x= 300, y = 140)

        timeLabel = Label(self, text="Timer:", font=SMALL_FONT)
        timeLabel.place(x= 100, y = 170)

        #minuteLabel =  Label(self, textvariable=controller.duration, font=SMALL_FONT)
        #minuteLabel.place(x= 163, y = 170)

        minuteLabel= Label(self, width=3, font=SMALL_FONT, textvariable=controller.duration)
        minuteLabel.place(x=163,y=170)

        colon = Label(self, font=SMALL_FONT, text= ":")
        colon.place(x=190, y=169)

        #secondLabel =  Label(self, textvariable=second, font=SMALL_FONT)
        #secondLabel.place(x= 195, y = 170)
        secondLabel= Label(self, width=3, font=SMALL_FONT, textvariable=second)
        secondLabel.place(x=196,y=170)

        #self.parent.after(100, update)
        #self.after(100, update)
        #self.controller.after(100, update)

            #self.update()
            #time.sleep(1)

            # Use of Entry class to take input from the user
        #minuteEntry= Entry(self, width=3, font=("Arial",18,""), textvariable=minute)
        #minuteEntry.place(x=170,y=170)
        print('h3ello?')
            #secondEntry= Entry(self, width=3, font=("Arial",18,""), textvariable=second)
        #secondEntry.place(x=217,y=170)


        def submit():
            print('helloe?')
    # the input provided by the user is
    # stored in here :temp
            #FIRST_RUN = True
            #if FIRST_RUN:
            #    minute.set(controller.duration.get())
            #    FIRST_RUN = False
            temp = int(controller.duration.get())*60 + int(second.get())
            while temp >-1:

        # divmod(firstvalue = temp//60, secondvalue = temp%60)
                mins,secs = divmod(temp,60)

        # using format () method to store the value up to
        # two decimal places
                minute.set("{0:2d}".format(mins))
                second.set("{0:2d}".format(secs))
                minuteLabel['textvariable']= minute


                begin['text'] = 'End'
                begin['command'] = lambda: controller.show_frame(EndPage)
                #print(minute.get())
                #minuteLabel= Label(self, width=3, font=SMALL_FONT, textvariable=minute)
                #minuteLabel.place(x=163,y=170)

        # updating the GUI window after decrementing the
        # temp value every time
                self.update()
                time.sleep(1)

        # when temp value = 0; then a messagebox pop's up
        # with a message:"Time's up"
                if (temp == 0):
                    messagebox.showinfo("Time Countdown", "Time's up ")
                #print(mins)
        # after every one sec the value of temp will be decremented
        # by one
                temp -= 1

                #minuteLabel.place(x=163,y=170)
                #print(minute.get())


        #def submit(button):

            #try:
                # the input provided by the user is
                # stored in here :temp
            #temp = int(controller.duration.get())*60
            #except:
            #    print("Please input the right value")
            #while temp >-1:
                #controller.show_frame(EndPage)

                # divmod(firstvalue = temp//60, secondvalue = temp%60)
                #mins,secs = divmod(temp, 60)

                # using format () method to store the value up to
                # two decimal places
                #secondLabel.config(text="{0:2d}".format(secs))
                #minute.set("{0:2d}".format(mins))
                #second.set("{0:2d}".format(secs))

                # updating the GUI window after decrementing the
                # temp value every time
                #self.update()
                #time.sleep(1)

                # when temp value = 0; then a messagebox pop's up
                # with a message:"Time's up"
                #if (temp == 0):
                 #   messagebox.showinfo("Time Countdown", "Time's up ")

                # after every one sec the value of temp will be decremented
                # by one
                #temp -= 1


        title = Label(self, text="Confirm", font=LARGE_FONT)
        title.pack(pady=10,padx=10)

        back = Button(self, text="Back to Modes", command=lambda: controller.show_frame(Modes))
        back.place(x=70, y=250)

        begin = Button(self, text="Begin", command=lambda: submit())
        begin.place(x=250, y=250)

class EndPage(Frame):

    def __init__(self, parent, controller):
        Frame.__init__(self, parent)

        label = Label(self, text="Treatment has ended", font=LARGE_FONT)
        label.pack(pady=10,padx=10)

        mode = Label(self, text="   F for     minutes.", font=SMALL_FONT)
        mode.place(x=131,y=60)

        tempLabel =  Label(self, textvariable=controller.temperature, font=SMALL_FONT)
        tempLabel.place(x= 124, y = 60)

        durationLabel =  Label(self, textvariable=controller.duration, font=SMALL_FONT)
        durationLabel.place(x= 193, y = 60)

        done = Button(self, text="Return to Home", command=lambda: controller.show_frame(StartPage))
        done.place(x=128, y=100)

app = ARDapp()
app.title("ARD Interface")
app.mainloop()