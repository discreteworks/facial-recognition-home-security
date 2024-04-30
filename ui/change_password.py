from tkinter import *
from db.admin import *
from ui.dialog import Dialog


class ChangePassword(Dialog):
    def body(self, master):

        Label(master, text="Old Password:").grid(row=0)
        Label(master, text="New Password:").grid(row=1)

        self.old_password = Entry(master, show="*")
        self.new_password = Entry(master, show="*")

        self.old_password.grid(row=0, column=1)
        self.new_password.grid(row=1, column=1)
        return self.old_password  # initial focus

    def ok(self, event=None):

        admin = Admin()

        if not self.validate():
            self.initial_focus.focus_set()  # put focus back
            return

        self.withdraw()
        self.update_idletasks()

        if admin.update_password(self.old_password.get(), self.new_password.get()):
            self.apply()
        else:
            # message of not change
            self.cancel()

    def cancel(self, event=None):

        # put focus back to the parent window
        self.parent.root.focus_set()
        self.destroy()

    #
    # command hooks

    def validate(self):

        return 1  # override

    def apply(self):
        self.parent.root.focus_set()
        self.destroy()
