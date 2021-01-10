from tkinter import *
root = Tk()
root.geometry("500x300")
root.title("Tests")

def page1():
    page2text.pack_forget()
    page1text.pack()

def page2():
    page1text.pack_forget()
    page2text.pack()


page1btn = Button(root, text="Page 1", command=page1)
page2btn = Button(root, text="Page 2", command=page2)

page1text = Label(root, text="This is page 1")
page2text = Label(root, text="This is page 2")

page1btn.pack()
page2btn.pack()
page1text.pack()