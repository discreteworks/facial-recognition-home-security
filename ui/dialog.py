from tkinter import *
from db.admin import *


class Dialog(Toplevel):
    def __init__(self, parent, title=None):

        Toplevel.__init__(self, parent.root)

        self.transient(parent.root)

        if title:
            self.title(title)

        self.parent = parent

        self.result = None

        body = Frame(self)

        self.initial_focus = self.body(body)

        self.initial_focus.focus()

        body.pack(padx=5, pady=5)

        self.buttonbox()

        if not self.initial_focus:
            self.initial_focus = self
            self.focus()

        self.protocol("WM_DELETE_WINDOW", self.cancel)

        window_height = self.parent.root.winfo_width()
        window_width = self.parent.root.winfo_height()

        screen_width = self.parent.root.winfo_screenwidth()
        screen_height = self.parent.root.winfo_screenheight()

        x_cordinate = int((screen_width / 2))
        y_cordinate = int((screen_height / 2))

        # self.geometry("{}x{}+{}+{}".format(window_width, window_height, x_cordinate, y_cordinate))

        self.geometry("+%d+%d" % (x_cordinate - 100, y_cordinate - 100))

        self.transient(self.parent.root)

        self.grab_set()

        self.wait_window(self)

    def body(self, master):
        pass

    def buttonbox(self):
        # add standard button box. override if you don't want the
        # standard buttons

        box = Frame(self)

        w = Button(box, text="OK", width=10, command=self.ok, default=ACTIVE)
        w.pack(side=LEFT, padx=5, pady=5)
        w = Button(box, text="Cancel", width=10, command=self.cancel)
        w.pack(side=LEFT, padx=5, pady=5)

        self.bind("<Return>", self.ok)
        self.bind("<Escape>", self.cancel)

        box.pack()

    #
    # standard button semantics

    def ok(self, event=None):

        pass

    def cancel(self, event=None):

        # put focus back to the parent window
        self.parent.root.focus_set()
        self.destroy()

    #
    # command hooks

    def validate(self):

        return 1  # override

    def apply(self):
        pass
