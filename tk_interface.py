from tkinter import *

LARGE_FONT= ("Verdana bold", 15)
SMALL_FONT= ("Verdana italic", 13)

class ARDapp(Tk):

    def __init__(self, *args, **kwargs):
        
        Tk.__init__(self, *args, **kwargs)
        container = Frame(self)
        container.pack(side="top", fill="both", expand = True)

        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)
        
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
        label = Label(self, text="Welcome to the Athletic Recovery Device", font=LARGE_FONT)
        label2 = Label(self, text="Ready to Recover?", font=SMALL_FONT)
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
    
        Frame.__init__(self, parent)
        label = Label(self, text="Custom Setting", font=LARGE_FONT)
        label.pack(pady=10,padx=10)
        
        minute=StringVar()
        second=StringVar()
        minute.set("00")
        second.set("00")

        temp_set = Label(self, text="Set Temp.", font=SMALL_FONT)
        temp_set.place(x=150,y=70)

        time_set = Label(self, text="Set Time.", font=SMALL_FONT)
        time_set.place(x=150,y=100)

        tempEntry= Entry(self, width=3, font=("Arial",18,""), textvariable=minute)
        tempEntry.place(x=260,y=70)

        minuteEntry= Entry(self, width=3, font=("Arial",18,""), textvariable=minute)
        minuteEntry.place(x=260,y=100)
  
        secondEntry= Entry(self, width=3, font=("Arial",18,""), textvariable=second)
        secondEntry.place(x=290,y=100)
        # SEND VARIABLES TO CONFIRM FRAME
        back = Button(self, text="Back", command=lambda: controller.show_frame(Locked))
        back.place(x=150,y=200)

        submit = Button(self, text="Submit", command=lambda: controller.show_frame(Confirm))
        submit.place(x=300,y=200)

class Confirm(Frame):

    def __init__(self, parent, controller):
        Frame.__init__(self, parent)
        label = Label(self, text="Confirm", font=LARGE_FONT)
        label.pack(pady=10,padx=10)

        
        c_temp = Label(self, text="Current Temp.")
        c_temp.pack(pady=10,padx=10)

        d_temp = Label(self, text="Desired Temp.")
        d_temp.pack(pady=10,padx=10)

        duration = Label(self, text="Desired Temp.")
        duration.pack(pady=10,padx=10)

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
        label = Label(self, text="Treatment has ended", font=LARGE_FONT)
        label.pack(pady=10,padx=10)

        mode = Label(self, text="__F for __ minutes.", font=SMALL_FONT)
        mode.pack(pady=10,padx=10)

        done = Button(self, text="Return to Home", command=lambda: controller.show_frame(StartPage))
        done.pack()

        
app = ARDapp()
app.geometry("500x300")
app.mainloop()
