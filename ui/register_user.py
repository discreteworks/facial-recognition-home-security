from tkinter import *
from tkinter.ttk import *
from db.user import *
from db.room import *
from ui.dialog import Dialog


class RegisterUser(Dialog):
    def body(self, master):

        user_obj = User()

        training_method = ["Camera", "Images"]

        self.user_list = user_obj.get_users()

        Label(master, text="User:").grid(row=0)
        Label(master, text="Method:").grid(row=1)

        self.name = Combobox(
            master, values=[item[1] for item in self.user_list], width=19
        )
        self.method = Combobox(master, values=training_method, width=19)

        self.name.grid(row=0, column=1)
        self.method.grid(row=1, column=1)
        return self.name  # initial focus

    def ok(self, event=None):

        user = User()

        if not self.validate():
            self.initial_focus.focus_set()  # put focus back
            messagebox.showerror("Error: Validation", "Please user and method!")
            return

        self.withdraw()
        self.update_idletasks()
        self.parent.root.focus_set()

        # set user_id in the parent window.
        self.parent.user_id = self.user_list[self.name.current()][0]

        if self.method.current() == 0:
            self.parent.register_camera()
        elif self.method.current() == 1:
            self.parent.register_image()

        self.destroy()

    # command hooks

    def validate(self):
        if self.name.current() == -1 or self.method.current() == -1:
            return False
        else:
            return True

    def apply(self):
        pass
