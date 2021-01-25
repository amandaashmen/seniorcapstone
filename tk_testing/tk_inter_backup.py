from tkinter import *

LARGE_FONT= ("Verdana bold", 15)
SMALL_FONT= ("Verdana italic", 13)

#global TEMP_VAR
#TEMP_VAR = StringVar()
TEMP_VAR = "48"
global duration_var

class ARDapp(Tk):

    def __init__(self, *args, **kwargs):
        
        Tk.__init__(self, *args, **kwargs)
        container = Frame(self)
        container.pack(side="top", fill="both", expand = True)

        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)
        
        self.shared_data = {"temperature": StringVar(),
                            "duration": StringVar()}

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
        self.controller=controller #test
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
        self.controller=controller #test
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
        self.controller=controller #test
        label = Label(self, text="Enter Password", font=LARGE_FONT)
        label.pack(pady=10,padx=10)

        passEntry= Entry(self, width=30, font=("Arial",18,""))
        passEntry.pack()

        back = Button(self, text="Back", command=lambda: controller.show_frame(Modes))
        back.pack()

        submit = Button(self, text="Submit", command=lambda: controller.show_frame(Custom))
        submit.pack()

class Custom(Frame):

    def __init__(self, parent, controller):
        #self.test = StringVar()
        
        Frame.__init__(self, parent)
        self.controller=controller #test
        label = Label(self, text="Custom Setting", font=LARGE_FONT)
        label.pack(pady=10,padx=10)
        
        temp=StringVar()
        minute=StringVar()
        second=StringVar()
        temp.set("00")
        minute.set("00")
        second.set("00")

        temp_set = Label(self, text="Set Temp.", font=SMALL_FONT)
        temp_set.place(x=150,y=70)

        time_set = Label(self, text="Set Time.", font=SMALL_FONT)
        time_set.place(x=150,y=100)
        #tempEntry= Entry(self, width=3, font=("Arial",18,""), textvariable=self.test)
        #self.controller.shared_data["temperature"] = "89"
        
        #tempEntry= Entry(self, width=3, font=("Arial",18,""), textvariable=self.controller.shared_data["temperature"])
        tempEntry= Entry(self, width=3, font=("Arial",18,""))
        tempEnt = "5"
        self.controller.shared_data["temperature"].set(tempEnt)
        #tempEntry = Entry(self, width=3, font=("Arial",18,""), textvariable=self.controller.shared_data["temperature"])
        global this_gotta
        this_gotta = tempEntry.get()
        #tempEntry = Entry(self, width=3, font=("Arial",18,""))
        tempEntry.place(x=260,y=70)
        #self.test = tempEntry.get()
        
        #global TEMP_VAR
        # Once the Submit button is pressed, this function will execute
        def set_variables():
            global TEMP_VAR
            TEMP_VAR = tempEntry.get()
            #self.test = tempEntry.get()
            #label = Label(self, text=self.test)
            #label.pack()
            #self.temp = tempEntry.get()
            #self.controller.shared_data["temperature"] = tempEntry.get()
            #self.controller.shared_data["temperature"].set(tempEntry.get())
            self.controller.shared_data["temperature"] = "89"
            controller.show_frame(Confirm)
        
            #new.place(x=300,y=250)
            #return self.test
            #controller.show_frame(Confirm)
            #return 8
        #TEMP_VAR.set(tempEntry.get())
        #TEMP_VAR = tempEntry.get()

        minuteEntry= Entry(self, width=3, font=("Arial",18,""), textvariable=minute)
        minuteEntry.place(x=260,y=100)
  
        secondEntry= Entry(self, width=3, font=("Arial",18,""), textvariable=second)
        secondEntry.place(x=290,y=100)
        # SEND VARIABLES TO CONFIRM FRAME
        back = Button(self, text="Back", command=lambda: controller.show_frame(Locked))
        back.place(x=150,y=200)

        #self.test = set_variables()
        submit = Button(self, text="Submit", command=set_variables)
        #submit = Button(self, text="Submit", command=lambda: controller.show_frame(Confirm))
        
        submit.place(x=300,y=200)

class Confirm(Frame):

    def __init__(self, parent, controller):
        Frame.__init__(self, parent)
        self.controller=controller #test
        label = Label(self, text="Confirm", font=LARGE_FONT)
        label.pack(pady=10,padx=10)

        
        current_temp = Label(self, text="Current Temp.")
        current_temp.pack(pady=10,padx=10)

        def printVariable():
            print(TEMP_VAR)
            labelp = Label(self, text=TEMP_VAR)
            labelp.pack()
        button2 = Button(self, command = printVariable)
        button2.pack()

        #cus = Custom(parent, controller)
        #cus.testing
        #display_temp = Label(self, text=cus.test)
        #temp = self.controller.shared_data["temperature"].get()
        temp = self.controller.shared_data["temperature"]
        display_temp = Label(self, text=self.controller.shared_data["temperature"])
        display_temp.pack(pady=10,padx=10)
        label2 = Label(self, text=this_gotta, font=LARGE_FONT)
        label2.pack()
        #display_test = Label(self, text=cus.temp)
        #display_test.pack(pady=10,padx=10)
        #global TEMP_VAR
        #label_temp = TEMP_VAR
        def get_temp():
            t = self.controller.shared_data["temperature"]
            label4 = Label(self, text="PRINT", font=LARGE_FONT)
            label4.place(x=0, y=0)
            v = StringVar()
            v = "dog"
            label42 = Label(self, text=v, font=LARGE_FONT)
            label42.pack()
        back = Button(self, text="Back", command=lambda: get_temp)
        back.place(x=150,y=200)
        #display_tem = Label(self, text=label_temp)
        display_temp = Label(self, text=TEMP_VAR)
        display_temp.pack(pady=10,padx=10)
        #display_tem.pack(pady=10,padx=10)

        #d_temp = Label(self, text="Desired Temp.")
        #d_temp.pack(pady=10,padx=10)

        #duration = Label(self, text="Desired Temp.")
        #duration.pack(pady=10,padx=10)

        back = Button(self, text="Back to Modes", command=lambda: controller.show_frame(Modes))
        back.pack(pady=10,padx=10)

        def clickedBegin(button):
            button['text'] = 'End'
            button['command'] = lambda: controller.show_frame(EndPage)

        begin = Button(self, text="Begin", command=lambda: clickedBegin(begin))
        begin.pack()

class EndPage(Frame):

    def __init__(self, parent, controller):
        Frame.__init__(self, parent)
        self.controller=controller #test
        
        label = Label(self, text="Treatment has ended", font=LARGE_FONT)
        label.pack(pady=10,padx=10)

        mode = Label(self, text="__F for __ minutes.", font=SMALL_FONT)
        mode.pack(pady=10,padx=10)

        done = Button(self, text="Return to Home", command=lambda: controller.show_frame(StartPage))
        done.pack()

        
app = ARDapp()
app.title("ARD Interface")
app.mainloop()
