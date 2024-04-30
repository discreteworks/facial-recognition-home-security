#!/usr/bin/python3
from tkinter import *
from tkinter.ttk import *

from ui.dashboard import Dashboard


def main():

    root = Tk()
    root.minsize(300, 200)
    root.iconphoto(True, PhotoImage(file="facial-recognition.png"))

    app = Dashboard(root)

    root.title("Facial Recognition Dashboard")

    root.mainloop()

    try:
        root.destroy()
    except:
        pass

if __name__ == "__main__":
    main()
