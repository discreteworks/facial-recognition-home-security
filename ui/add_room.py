from tkinter import *
from tkinter.ttk import *

# ui imports
from ui.dialog import Dialog

# db imports
from db.user import *
from db.room import *
from db.pin import *


class AddRoom(Dialog):
    def body(self, master):

        pin_obj = Pin()

        self.pin_list = pin_obj.get_room_pins()

        Label(master, text="Name:").grid(row=0)
        Label(master, text="Pin:").grid(row=1)
        Label(master, text="Common:").grid(row=2)

        self.name = Entry(master, width=20)
        self.pin = Combobox(
            master, values=[item[0] for item in self.pin_list], width=19
        )
        self.common_val = IntVar()
        self.common = Checkbutton(master, text="Yes", variable=self.common_val)

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

        self.withdraw()
        self.update_idletasks()

        print(self.pin.current())
        print(self.pin_list)
        print(self.pin_list[self.pin.current()][0])

        if room.add_room(
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
