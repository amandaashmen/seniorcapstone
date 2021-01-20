from tkinter import *

class MyWindow(Frame):
    def __init__(self, parent):
        Frame.__init__(self, parent)
        ## set a stringvar and make it global (use specifc variable name,
        ## globals can mess with other variables from your imports)
        global label_var
        label_var = StringVar()

                                                    ## set textvariable to stringvar
        self.label = Label(self, textvariable=label_var)
        label_var.set('Hello, world')
        self.label.pack()
        
        


root = Tk()

run = MyWindow(root)

## use the global stringvar to .set() the text from another class via button or whatever
label_var.set('Hello, everyone')

root.geometry('480x320')   
MyWindow(root).pack()
root.mainloop()