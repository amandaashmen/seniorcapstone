import time
from tkinter import *
from tkinter import messagebox

LARGE_FONT= ("Verdana bold", 15)
SMALL_FONT= ("Verdana italic", 13)
TEMP_VAR = ""
DUR_VAR = ""
PASSWORD = "U"

class ARDapp(Tk):

    def __init__(self, *args, **kwargs):

        Tk.__init__(self, *args, **kwargs)
        container = Frame(self)
        container.pack(side="top", fill="both", expand = True)

        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        ##self.entrythingy = Entry()
        #self.entrythingy.pack()

        # Create the application variable.
        self.contents = StringVar()

        #self.shared_data = {"temperature": StringVar(),
                            #"duration": StringVar()}

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

        #self.entrythingy = Entry()
        # Set it to some value.
        ##controller.contents.set("this is a variable")
        # Tell the entry widget to watch this variable.
        ##controller.entrythingy["textvariable"] = controller.contents
        #controller.entrythingy.pack() #packs to every frame
        ##myEntry = Entry(self, textvariable = controller.entrythingy.get())
        ##myEntry.pack()

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

        ##entrynew = Entry(self)
        ##entrynew.pack()
        ##controller.contents.set(entrynew.get())
        # Tell the entry widget to watch this variable.
        ##controller.entrythingy["textvariable"] = controller.contents

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

        ##self.controller = controller
        temp = StringVar()

        # Once the Submit button is pressed, this function will execute
        def set_variables():
            #global TEMP_VAR
            #TEMP_VAR = tempEntry.get()
            #print("custom")
            #print(TEMP_VAR)
            #print("above")
            #global DUR_VAR
            #DUR_VAR = timeEntry.get()
            #controller.show_frame(Confirm)
            #con = Confirm(parent, controller)
            #con.printHi()
            #controller.frames[Confirm].printHi
            controller.contents.set(temp.get())
            #controller.shared_data["temperature"] = temp.get()
            controller.show_frame(Confirm)

        temp_set = Label(self, text="Set Temperature (F)", font=SMALL_FONT)
        temp_set.place(x=70,y=90)

        time_set = Label(self, text="Set Duration (min.)", font=SMALL_FONT)
        time_set.place(x=70,y=130)

        tempEntry= Entry(self, width=3, font=("Arial",18,""), textvariable=temp)
        tempEntry.place(x=260,y=90)

        timeEntry= Entry(self, width=3, font=("Arial",18,""))
        timeEntry.place(x=260,y=130)

        back = Button(self, text="Back", command=lambda: controller.show_frame(Locked))
        back.place(x=100,y=200)

        submit = Button(self, text="Submit", command=set_variables)
        submit.place(x=250,y=200)


class Confirm(Frame):
    #def printHi(self):
        #print('hi')
    def __init__(self, parent, controller):
        Frame.__init__(self, parent)
        #self.controller = controller # necessda?

        # Declaration of variables
        #minute=DUR_VAR
        minute=DUR_VAR
        second=StringVar()

        # setting the default value as 0
        #minute.set("9"+DUR_VAR+"9")                    #DUR_VAR makes it blank
        second.set("00")

        #def printMode():
        #while(1):
        current_temp = Label(self, text="Current Temperature: 70", font=SMALL_FONT)
        current_temp.place(x=100,y=110)

        desired_temp = Label(self, text="Desired temperature: ", font=SMALL_FONT)
        desired_temp.place(x= 100, y = 140)

        #tempLabel = Label(self, font=SMALL_FONT, textvariable= controller.shared_data["temperature"])
        tempLabel = Label(self, font=SMALL_FONT, textvariable= controller.contents)
        tempLabel.place(x= 170, y = 140)

        #contents = StringVar()
        # Set it to some value.
        #contents.set(TEMP_VAR)
        #maqybe make contents global and set in the other frame
        # Tell the entry widget to watch this variable.
        #tempLabel["textvariable"] = contents


        timeLabel = Label(self, text="Timer: "+DUR_VAR+":", font=SMALL_FONT)
        secondLabel =  Label(self, textvariable=second, font=SMALL_FONT)
        secondLabel.place(x= 195, y = 170)
        timeLabel.place(x= 100, y = 170)

        def update():
                #global TEMP_VAR

            print(TEMP_VAR)
            tempLabel.config(text=TEMP_VAR)

        #self.parent.after(100, update)
        self.after(100, update)
        #self.controller.after(100, update)

        def printHi(self):
            print("confirm")

        #self.printHi = printHi()

            #self.update()
            #time.sleep(1)

            # Use of Entry class to take input from the user
        #minuteEntry= Entry(self, width=3, font=("Arial",18,""), textvariable=minute)
        #minuteEntry.place(x=170,y=170)

            #secondEntry= Entry(self, width=3, font=("Arial",18,""), textvariable=second)
        #secondEntry.place(x=217,y=170)

        def submit(button):
            #def reformat():
             #   title.destroy()
              #  showTemp.destroy()
               # button['text'] = 'click'
               # temp = 0

            button['text'] = 'End'
            button['command'] = lambda: controller.show_frame(EndPage)
            #button['command'] = lambda: reformat

            #try:
                # the input provided by the user is
                # stored in here :temp
            temp = int(DUR_VAR)*60
            #except:
            #    print("Please input the right value")
            while temp >-1:
                #controller.show_frame(EndPage)

                # divmod(firstvalue = temp//60, secondvalue = temp%60)
                mins,secs = divmod(temp, 60)

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
                if (temp == 0):
                    messagebox.showinfo("Time Countdown", "Time's up ")

                # after every one sec the value of temp will be decremented
                # by one
                temp -= 1



        title = Label(self, text="Confirm", font=LARGE_FONT)
        title.pack(pady=10,padx=10)

        #showTemp = Button(self, text="Click to check mode", command = printMode, fg="navy", font="Helvetica 14")
        #showTemp.pack(pady=10)

        back = Button(self, text="Back to Modes", command=lambda: controller.show_frame(Modes))
        back.place(x=70, y=250)

        begin = Button(self, text="Begin", command=lambda: submit(begin))
        begin.place(x=250, y=250)

    def printHi(self):
        tempLabel = Label(self, text=TEMP_VAR, font=SMALL_FONT)
        tempLabel.pack()
        print("confirm")
        print(TEMP_VAR)
        tempLabel.config(text=TEMP_VAR)
        print('config')
        tempLabel.place(x= 170, y = 140)
        begin = Button(self, text="Begdfgin", command=lambda: submit(begin))
        begin.place(x=300, y=250)

class EndPage(Frame):

    def __init__(self, parent, controller):
        Frame.__init__(self, parent)

        label = Label(self, text="Treatment has ended", font=LARGE_FONT)
        label.pack(pady=10,padx=10)

        mode = Label(self, text="__F for __ minutes.", font=SMALL_FONT)
        mode.pack(pady=10,padx=10)

        done = Button(self, text="Return to Home", command=lambda: controller.show_frame(StartPage))
        done.pack()

app = ARDapp()
app.title("ARD Interface")
app.mainloop()