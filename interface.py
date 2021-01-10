from tkinter import *
import tkinter.font as font

LARGE_FONT= ("Verdana", 15)
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
        #button['font'] = font.Font(size=15)
        button.configure(font='Helvetica 15 bold')
        button.configure(borderwidth=3)
        button.pack(pady=30)


class Modes(Frame):

    def __init__(self, parent, controller):
        Frame.__init__(self, parent)
        label = Label(self, text="Select Mode", font=LARGE_FONT)
        label.pack(pady=10,padx=10)

        presetA = Button(self, text="Preset A", command=lambda: controller.show_frame(Confirm))
        presetA.pack()

        presetB = Button(self, text="Preset B", command=lambda: controller.show_frame(Confirm))
        presetB.pack()

        presetC = Button(self, text="Preset C", command=lambda: controller.show_frame(Confirm))
        presetC.pack()

        custom = Button(self, text="Custom", command=lambda: controller.show_frame(Locked))
        custom.pack()


class Locked(Frame):

    def __init__(self, parent, controller):
        Frame.__init__(self, parent)
        label = Label(self, text="Locked", font=LARGE_FONT)
        label.pack(pady=10,padx=10)

        back = Button(self, text="Back", command=lambda: controller.show_frame(Modes))
        back.pack()

        submit = Button(self, text="Submit", command=lambda: controller.show_frame(Custom))
        submit.pack()

class Custom(Frame):

    def __init__(self, parent, controller):
        Frame.__init__(self, parent)
        label = Label(self, text="Custom", font=LARGE_FONT)
        label.pack(pady=10,padx=10)

        back = Button(self, text="Back", command=lambda: controller.show_frame(Locked))
        back.pack()

        submit = Button(self, text="Submit", command=lambda: controller.show_frame(Confirm))
        submit.pack()

class Confirm(Frame):

    def __init__(self, parent, controller):
        Frame.__init__(self, parent)
        label = Label(self, text="Confirm", font=LARGE_FONT)
        label.pack(pady=10,padx=10)

        back = Button(self, text="Back to Modes", command=lambda: controller.show_frame(Modes))
        back.pack()

        def clickedBegin(button):
            button['text'] = 'End'
            button['command'] = lambda: controller.show_frame(EndPage)

        begin = Button(self, text="Begin", command=lambda: clickedBegin(begin))
        begin.pack()

class EndPage(Frame):

    def __init__(self, parent, controller):
        Frame.__init__(self, parent)
        label = Label(self, text="Treatment has ended.", font=LARGE_FONT)
        label.pack(pady=10,padx=10)

        done = Button(self, text="Return to Home", command=lambda: controller.show_frame(StartPage))
        done.pack()

        
app = ARDapp()
app.geometry("500x300")
app.mainloop()
