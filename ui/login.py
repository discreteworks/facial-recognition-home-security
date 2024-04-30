from tkinter import *
from tkinter import messagebox
from db.admin import *
from ui.dialog import Dialog


class Login(Dialog):
    def body(self, master):

        Label(master, text="Login:").grid(row=0)
        Label(master, text="Password:").grid(row=1)

        self.login = Entry(master,)
        self.password = Entry(master, show="*")

        self.login.grid(row=0, column=1)
        self.password.grid(row=1, column=1)
        return self.login  # initial focus

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

        admin = Admin()

        if not self.validate():
            self.initial_focus.focus_set()  # put focus back
            return

        self.withdraw()
        self.update_idletasks()

        if admin.authenticate(self.login.get(), self.password.get()):
            self.apply()
            self.parent.root.focus_set()
            self.destroy()
            self.parent.close_basic_menu()
            self.parent.show_full_menu()
        else:
            messagebox.showerror("Error", "Invalid Password!")

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
