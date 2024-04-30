from tkinter import *
from tkinter.ttk import *
from db.user import *
from db.room import *
from ui.dialog import Dialog


class AddUser(Dialog):
    def body(self, master):

        roomObj = Room()

        self.roomList = roomObj.get_user_room()

        Label(master, text="Name:").grid(row=0)
        Label(master, text="Room:").grid(row=1)

        self.name = Entry(master, width=20)
        self.room = Combobox(
            master, values=[item[1] for item in self.roomList], width=19
        )

        self.name.grid(row=0, column=1)
        self.room.grid(row=1, column=1)
        return self.name  # initial focus

    def ok(self, event=None):

        user = User()

        if not self.validate():
            self.initial_focus.focus_set()  # put focus back
            messagebox.showerror("Error: Validation", "Please provide name and room!")
            return

        self.withdraw()
        self.update_idletasks()

        if user.add_user(self.name.get(), self.roomList[self.room.current()][0]):
            self.parent.root.focus_set()
            self.parent.show_user_list()
            self.destroy()
        else:
            self.cancel()

    #
    # command hooks

    def validate(self):
        if self.name.get() == "" or self.room.current() == -1:
            return False
        else:
            return True

    def apply(self):
        pass
