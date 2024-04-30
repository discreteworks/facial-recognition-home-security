from tkinter import *
from tkinter.ttk import *

# ui imports
from ui.dialog import Dialog

# db imports
from db.user import *
from db.room import *
from db.pin import *


class UpdateRoom(Dialog):
    def __init__(self, parent, title=None, room_id=None):

        self.room_id = room_id
        Dialog.__init__(self, parent, title)

    def body(self, master):

        pin_obj = Pin()

        room_obj = Room()

        cur_room = room_obj.get_room(self.room_id)

        self.pin_list = pin_obj.get_room_pins(cur_room[3])

        Label(master, text="Name:").grid(row=0)
        Label(master, text="Pin:").grid(row=1)
        Label(master, text="Common:").grid(row=2)

        self.name = Entry(master, width=20)
        self.pin = Combobox(
            master, values=[item[0] for item in self.pin_list], width=19
        )
        self.common_val = IntVar()

        self.common_val.set(cur_room[2])

        self.common = Checkbutton(master, text="Yes", variable=self.common_val)

        self.name.insert(0, cur_room[1])

        i = 0
        for item in self.pin_list:
            if item[0] == cur_room[3]:
                break
            else:
                i = i + 1

        self.pin.current(i)

        self.name.grid(row=0, column=1)
        self.pin.grid(row=1, column=1)
        self.common.grid(row=2, column=1)
        return self.name  # initial focus

    def ok(self, event=None):

        room = Room()

        if not self.validate():
            self.initial_focus.focus_set()  # put focus back
            messagebox.showerror("Error: Validation", "Please provide name and room!")
            return

        if bool(self.common_val.get()):
            user_obj = User()
            usr = user_obj.get_user_by_room(self.room_id)
            if usr:
                messagebox.showerror(
                    "Error: Unable To Set Room Common",
                    "User is already assigned to this room!",
                )
                return

        self.withdraw()
        self.update_idletasks()

        if room.update_room(
            self.room_id,
            self.name.get(),
            self.pin_list[self.pin.current()][0],
            bool(self.common_val.get()),
        ):
            self.parent.root.focus_set()
            self.parent.show_room_list()
            self.destroy()
        else:
            self.cancel()

    #
    # command hooks

    def validate(self):
        if self.name.get() == "" or self.pin.current() == -1:
            return False
        else:
            return True

    def apply(self):
        pass
