from tkinter import *
from tkinter.ttk import *
from db.user import *
from db.room import *
from ui.dialog import Dialog


class UpdateUser(Dialog):
    def __init__(self, parent, title=None, user_id=None):

        self.user_id = user_id
        Dialog.__init__(self, parent, title)

    def body(self, master):

        room_obj = Room()

        user_obj = User()

        cur_user = user_obj.get_user(self.user_id)

        self.roomList = room_obj.get_user_room(cur_user[2])

        Label(master, text="Name:").grid(row=0)
        Label(master, text="Room:").grid(row=1)

        self.name = Entry(master, width=20)
        self.room = Combobox(
            master, values=[item[1] for item in self.roomList], width=19
        )

        self.name.insert(0, cur_user[1])

        i = 0

        for item in self.roomList:
            if item[0] == cur_user[2]:
                break
            else:
                i = i + 1

        self.room.current(i)

        self.name.grid(row=0, column=1)
        self.room.grid(row=1, column=1)
        return self.name  # initial focus

    #
    # standard button semantics

    def ok(self, event=None):

        user = User()

        if not self.validate():
            self.initial_focus.focus_set()  # put focus back
            messagebox.showerror("Error: Validation", "Please provide name and room!")
            return

        self.withdraw()
        self.update_idletasks()

        if user.update_user(
            self.user_id, self.name.get(), self.roomList[self.room.current()][0]
        ):
            self.parent.root.focus_set()
            self.parent.show_user_list()
            self.destroy()
        else:
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
        pass
