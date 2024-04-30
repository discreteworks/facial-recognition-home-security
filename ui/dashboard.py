import threading
import datetime
import cv2
import os
import time

from tkinter import *
from tkinter.ttk import *
import tkinter.messagebox
from tkinter import filedialog as fd

from PIL import Image
from PIL import ImageTk
import numpy as np

from ui.login import Login
from ui.change_password import ChangePassword

from ui.add_user import AddUser
from ui.update_user import UpdateUser
from ui.update_room import UpdateRoom
from ui.register_user import RegisterUser

from ui.add_room import AddRoom

if os.uname()[4][:3] == "arm":
    from hardware.gpio import PinManager

from db.user import User
from db.room import Room

# Constants
PHOTOS_COUNT = 29

class Dashboard:
    def __init__(self, master):

        self.root = master

        self.detectFrame = None

        self.cam = None

        self.tree = None

        self.lstFrame = None

        self.trainFrame = None

        self.room_id = None

        self.user_id = None

        if os.uname()[4][:3] == "arm":
            self.pin_manager = PinManager()

        self.dirname = os.path.dirname(__file__)

        self.classifier_filename = os.path.join(
            self.dirname, "../cascades/haarcascade_frontalface_default.xml"
        )

        dataset_directory = os.path.join(self.dirname, "../dataset")

        if not os.path.exists(dataset_directory):
            os.mkdir(dataset_directory)

        self.menu()

        self.init_room_context_menu()

        self.init_user_context_menu()

        self.toolbar_menu()

        self.show_basic_menu()

        self.trainEvent = threading.Event()

        self.stopEvent = threading.Event()

        self.completeEvent = threading.Event()

        self.thread = threading.Thread(target=self.show_detect_camera, args=())

        self.thread.start()

        # self.root.overrideredirect(True)
        self.root.geometry(
            "{0}x{1}+0+0".format(
                int(self.root.winfo_screenwidth()), int(self.root.winfo_screenheight())
            )
        )
        self.root.focus_set()  # <-- move focus to this widget
        self.root.bind("<Escape>", self.close_app)
        self.root.wm_protocol("WM_DELETE_WINDOW", self.close_app)

    def login_window(self):
        """
        Show login window to
        authenticate admin.
        """
        Login(self, "Login")

    def add_user_window(self):
        """
        Show add user window to
        add user.
        """
        AddUser(self, "Add User")

    def register_window(self):
        """
        Show register user window to
        facial train user.
        """
        RegisterUser(self, "Register User")

    def register_camera(self):
        """
        Show register user window to
        facial train user.
        """
        self.thread = threading.Thread(target=self.show_train_camera, args=())

        self.thread.start()

    def register_image(self):
        """
        Show register user window to
        facial train user.
        """
        self.show_train_image()

    def change_password_window(self):
        """
        Show change password window.
        """
        d = ChangePassword(self, "Change Password")

    def add_room_window(self):
        """
        Show add user window to add room.
        """
        AddRoom(self, "Add Room")

    def show_user_list(self):
        """
        Show user list.
        """
        self.reset_panel()

        usr_obj = User()

        users = usr_obj.get_users()

        self.lstFrame = Frame(self.root)

        columns = ("ID", "Name", "Room", "Registered")

        treeview = Treeview(
            self.lstFrame, height=18, show="headings", columns=columns
        )  #

        vsb = Scrollbar(orient="vertical", command=treeview.yview)

        treeview.configure(yscrollcommand=vsb.set)

        treeview.column("ID", anchor="center")
        treeview.column("Name", anchor="center")
        treeview.column("Room", anchor="center")
        treeview.column("Registered", anchor="center")

        treeview.heading("ID", text="ID")
        treeview.heading("Name", text="Name")
        treeview.heading("Room", text="Room")
        treeview.heading("Registered", text="Registered")

        treeview.pack(side=LEFT, fill=BOTH)
        for item in users:
            treeview.insert("", item[0], values=item)

        self.lstFrame.pack(side="top", padx=10, pady=10, anchor="w")

        treeview.bind("<Button-3>", self.user_popup)

        self.tree = treeview

    def show_room_list(self):
        """
        Show room list.
        """
        self.reset_panel()

        room_obj = Room()

        rooms = room_obj.get_rooms()

        self.lstFrame = Frame(self.root)

        columns = ("ID", "Name", "GPIO_Pin", "Common")

        treeview = Treeview(self.lstFrame, height=18, show="headings", columns=columns)

        vsb = Scrollbar(orient="vertical", command=treeview.yview)

        treeview.configure(yscrollcommand=vsb.set)

        treeview.column("ID", anchor="center")
        treeview.column("Name", anchor="center")
        treeview.column("GPIO_Pin", anchor="center")
        treeview.column("Common", anchor="center")

        treeview.heading("ID", text="ID")
        treeview.heading("Name", text="Name")
        treeview.heading("GPIO_Pin", text="GPIO Pin")
        treeview.heading("Common", text="Common")

        treeview.pack(side=LEFT, fill=BOTH)

        for item in rooms:
            treeview.insert("", item[0], values=item)

        treeview.bind("<Button-3>", self.room_popup)

        self.tree = treeview

        self.lstFrame.pack(side="top", padx=10, pady=10, anchor="w")

    def user_popup(self, event):
        """
        Action in event of button 3 on tree view
        """

        iid = self.tree.identify_row(event.y)
        if iid:
            curItem = self.tree.focus()
            item = self.tree.item(curItem)

            self.user_id = item["values"][0]

            # mouse pointer over item
            self.tree.selection_set(iid)
            self.user_popup_menu.post(event.x_root, event.y_root)
        else:
            # mouse pointer not over item
            # occurs when items do not fill frame
            # no action required
            pass

    def room_popup(self, event):
        """
        Action in event of button 3 on tree view
        """
        iid = self.tree.identify_row(event.y)
        if iid:
            curItem = self.tree.focus()
            item = self.tree.item(curItem)

            self.room_id = item["values"][0]
            # mouse pointer over item
            self.tree.selection_set(iid)
            self.room_popup_menu.post(event.x_root, event.y_root)
        else:
            # mouse pointer not over item
            # occurs when items do not fill frame
            # no action required
            pass

    def init_room_context_menu(self):
        """
        Setup update/delete context menu for room.
        """

        self.room_popup_menu = Menu(self.root, tearoff=0)
        self.room_popup_menu.add_command(label="Update Room", command=self.update_room)
        self.room_popup_menu.add_command(label="Delete Room", command=self.delete_room)

    def init_user_context_menu(self):
        """
        Setup update/delete context menu for user.
        """

        self.user_popup_menu = Menu(self.root, tearoff=0)
        self.user_popup_menu.add_command(label="Update User", command=self.update_user)
        self.user_popup_menu.add_command(label="Delete User", command=self.delete_user)

    def update_user(self):
        """
        Open Update user dialog window.
        """

        UpdateUser(self, "Update User", self.user_id)

    def delete_user(self):
        """
        Delete user
        """

        delete = tkinter.messagebox.askyesno(
            title="Delete User", message="Do you want to delete User ?"
        )
        
        if delete:
            usrObj = User()
            if self.delete_files(self.user_id):
                users = usrObj.delete_user(self.user_id)
            else:
                tkinter.messagebox.showerror(
                    title="Delete User Failure", message="Cannot delete files!"
                )
            self.show_user_list()

    def delete_files(self, user_id):

        try:
            for count in range(1, 31):
                path = os.path.join(
                    self.dirname,
                    "../dataset/User." + str(user_id) + "." + str(count) + ".jpg",
                )
                if os.path.exists(path):
                    os.remove(path) 
            # re-train after deletion
            face_detector = cv2.CascadeClassifier(self.classifier_filename)
            self.trainer(face_detector)    
            return True
        except Exception as e:
            return False

    def update_room(self):
        """
        Open Update room dialog window.
        """

        UpdateRoom(self, "Update Room", self.room_id)

    def delete_room(self):
        """
        Delete room
        """

        delete = tkinter.messagebox.askyesno(
            title="Delete Room", message="Do you want to delete Room ?"
        )
        if delete:
            user_obj = User()
            rslt = user_obj.get_user_by_room(self.room_id)
            if bool(rslt) == False:
                room_obj = Room()
                room_obj.delete_room(self.room_id)
                self.show_room_list()
            else:
                tkinter.messagebox.showerror(
                    title="Delete Room Failed", message="User exist for this room!"
                )

    def sign_out(self):
        """
        Sign out admin from dashboard.
        """
        self.reset_panel()
        if os.uname()[4][:3] == "arm":
            self.pin_manager.pin_reset()
        self.thread = threading.Thread(target=self.show_detect_camera, args=())
        self.thread.start()
        self.close_full_menu()
        self.show_basic_menu()

    def reset_panel(self):
        """
        Reset panel 
        """
        # stop camera.
        self.stopEvent.set()

        if self.trainFrame:
            self.trainFrame.destroy()
        if self.lstFrame:
            self.lstFrame.destroy()

    def about(self):
        """
        Open application about message.
        """

        tkinter.messagebox.showinfo(
            title="About Facial Recognition", message="Facial Recognition Version:1.0"
        )

    def close_app(self):
        """
        set the stop event, cleanup the camera 
        """
        print("[INFO] Dashboard closing...")
        self.stopEvent.set()
        self.user_popup_menu.destroy()
        if os.uname()[4][:3] == "arm":
            self.pin_manager.cleanup()
        self.root.quit()

    def menu(self):
        """
        Dashboard menubar
        """
        menu = Menu(self.root, tearoff=0)
        menubar = Menu(self.root)
        filemenu = Menu(menubar, tearoff=0)
        filemenu.add_command(label="Exit", command=self.close_app)
        menubar.add_cascade(label="Application", menu=filemenu)

        helpmenu = Menu(menubar, tearoff=0)
        helpmenu.add_command(label="About...", command=self.about)
        menubar.add_cascade(label="Help", menu=helpmenu)
        self.root.config(menu=menubar)

    def toolbar_menu(self):

        frame = Frame(self.root)

        frame.pack(side=TOP, fill=X)

        self.add_user = Button(frame, text="Add User", command=self.add_user_window)

        self.register = Button(
            frame, text="Register User", command=self.register_window
        )

        self.list_user = Button(frame, text="List User", command=self.show_user_list)

        self.add_room = Button(frame, text="Add Room", command=self.add_room_window)

        self.list_room = Button(frame, text="List Room", command=self.show_room_list)

        self.change_password = Button(
            frame, text="Change Password", command=self.change_password_window
        )

        self.signout = Button(frame, text="Sign Out", command=self.sign_out)

        self.login = Button(frame, text="Admin", command=self.login_window)

    def show_full_menu(self):
        """
        Show full menu after admin authentication.
        """
        self.add_user.pack(side=LEFT, padx=2, pady=2)

        self.register.pack(side=LEFT, padx=2, pady=2)

        self.list_user.pack(side=LEFT, padx=2, pady=2)

        self.add_room.pack(side=LEFT, padx=2, pady=2)

        self.list_room.pack(side=LEFT, padx=2, pady=2)

        self.change_password.pack(side=LEFT, padx=2, pady=2)

        self.signout.pack(side=LEFT, padx=2, pady=2)

    def close_full_menu(self):
        """
        Close full menu to return to facial
        detection.
        """

        self.add_user.pack_forget()

        self.register.pack_forget()

        self.list_user.pack_forget()

        self.add_room.pack_forget()

        self.list_room.pack_forget()

        self.change_password.pack_forget()

        self.signout.pack_forget()

    def show_basic_menu(self):
        """
        Show basic menu
        """
        self.login.pack(side=LEFT)

    def close_basic_menu(self):
        """
        Close the basic menu
        """
        self.login.pack_forget()
        self.close_detect_camera()

    def show_train_camera(self):
        """
        Show user camera view
        for live training.
        """
        self.reset_panel()

        self.trainEvent.clear()
        self.stopEvent.clear()

        self.trainFrame = Frame(self.root)
        self.trainFrame.pack(side="top")

        panel = Label(self.trainFrame)

        panel.grid(
            row=0, column=0, columnspan=2, sticky=W + E + N + S, padx=10, pady=10
        )
        self.train = Button(
            self.trainFrame, text="Train", command=lambda: self.trainEvent.set()
        )
        self.cancel_train = Button(
            self.trainFrame, text="Cancel", command=lambda: self.stopEvent.set()
        )
        self.train.grid(row=1, padx=2, pady=2)
        self.cancel_train.grid(row=1, column=1, padx=2, pady=2)

        try:
            cam = cv2.VideoCapture(0)
            cam.set(3, 640)  # set video width
            cam.set(4, 480)  # set video height

            count = 0

            face_detector = cv2.CascadeClassifier(self.classifier_filename)

            while not self.stopEvent.is_set():

                ret, img = cam.read()
                if self.stopEvent.is_set():
                    break
                # img = cv2.flip(img, -1) # flip video image vertically
                gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
                faces = face_detector.detectMultiScale(gray, 1.3, 5)
                for (x, y, w, h) in faces:
                    cv2.rectangle(img, (x, y), (x + w, y + h), (255, 0, 0), 2)
                    if self.trainEvent.is_set():
                        count += 1
                        # Save the captured image into the datasets folder
                        # this will be conditional
                        dataset_filename = os.path.join(
                            self.dirname,
                            "../dataset/User."
                            + str(self.user_id)
                            + "."
                            + str(count)
                            + ".jpg",
                        )
                        cv2.imwrite(
                            dataset_filename, gray[y : y + h, x : x + w],
                        )
                if count > PHOTOS_COUNT:
                    break
                image = Image.fromarray(img)
                image = ImageTk.PhotoImage(image)

                panel.configure(image=image)
                panel.image = image

            if self.trainEvent.is_set():
                if self.trainer(face_detector):
                    tkinter.messagebox.showinfo(
                        title="User Training", message="User registered"
                    )
                    User().register_user(self.user_id)
        except:
            tkinter.messagebox.showinfo(
                title="User Training", message="User not registered"
            )
        cam.release()
        self.trainFrame.destroy()
        self.trainFrame = None

    def trainer(self, face_detector):
        """
        Training function
        """
        try:
            recognizer = cv2.face.LBPHFaceRecognizer_create()
            faces, ids = self.get_images_labels(
                os.path.join(self.dirname, "../dataset"), face_detector
            )
            recognizer.train(faces, np.array(ids))
            recognizer.write(os.path.join(self.dirname, "../trainer.yml"))
            return True
        except Exception as e:
            return False

    def get_images_labels(self, path, detector):
        """
        Get images and user id's from dataset directory
        """
        imagePaths = [os.path.join(path, f) for f in os.listdir(path)]
        faceSamples = []
        ids = []
        for imagePath in imagePaths:
            PIL_img = Image.open(imagePath).convert("L")  # convert it to grayscale
            img_numpy = np.array(PIL_img, "uint8")
            id = int(os.path.split(imagePath)[-1].split(".")[1])
            faces = detector.detectMultiScale(img_numpy)
            for (x, y, w, h) in faces:
                faceSamples.append(img_numpy[y : y + h, x : x + w])
                ids.append(id)
        return faceSamples, ids

    def _set_text(self, entry, text):
        """
        Set text in Form Entry Widget
        """
        entry.delete(0, END)
        entry.insert(0, text)

    def _train_by_pic(self, pics):
        """
        Train using user provided pictures.
        """
        face_detector = cv2.CascadeClassifier(self.classifier_filename)
        count = 0

        try:
            for imagePath in pics:

                PIL_img = Image.open(imagePath).convert(
                    "RGB"
                )  # convert it to grayscale
                img_numpy = np.array(PIL_img, "uint8")

                gray = cv2.cvtColor(img_numpy, cv2.COLOR_BGR2GRAY)
                faces = face_detector.detectMultiScale(gray, 1.3, 5)

                for (x, y, w, h) in faces:
                    cv2.rectangle(img_numpy, (x, y), (x + w, y + h), (255, 0, 0), 2)
                    count += 1
                    # Save the captured image into the datasets folder
                    # this will be conditional
                    dataset_filename = os.path.join(
                        self.dirname,
                        "../dataset/User."
                        + str(self.user_id)
                        + "."
                        + str(count)
                        + ".jpg",
                    )
                    cv2.imwrite(
                        dataset_filename, gray[y : y + h, x : x + w],
                    )
            if count == len(pics):
                if self.trainer(face_detector):
                    tkinter.messagebox.showinfo(
                        title="User Training", message="User registered"
                    )
                    User().register_user(self.user_id)
                    return

            tkinter.messagebox.showinfo(
                title="User Training",
                message="No face detected in images. \n Please try again.",
            )

        except Exception as e:
            print("[Error] Training Failure.")

    def show_train_image(self):
        """
        Build form to accept images
        form user for training
        """
        self.reset_panel()
        self.trainFrame = Frame(self.root)
        self.trainFrame.pack(side="top")

        self.pic_1 = Entry(self.trainFrame, width=20)
        self.pic_2 = Entry(self.trainFrame, width=20)
        self.pic_3 = Entry(self.trainFrame, width=20)
        self.pic_4 = Entry(self.trainFrame, width=20)
        self.pic_5 = Entry(self.trainFrame, width=20)
        self.pic_6 = Entry(self.trainFrame, width=20)
        self.pic_7 = Entry(self.trainFrame, width=20)
        self.pic_8 = Entry(self.trainFrame, width=20)
        self.pic_9 = Entry(self.trainFrame, width=20)
        self.pic_10 = Entry(self.trainFrame, width=20)

        self.pic_1.grid(row=0, padx=2, pady=2)
        self.pic_2.grid(row=1, padx=2, pady=2)
        self.pic_3.grid(row=2, padx=2, pady=2)
        self.pic_4.grid(row=3, padx=2, pady=2)
        self.pic_5.grid(row=4, padx=2, pady=2)
        self.pic_6.grid(row=5, padx=2, pady=2)
        self.pic_7.grid(row=6, padx=2, pady=2)
        self.pic_8.grid(row=7, padx=2, pady=2)
        self.pic_9.grid(row=8, padx=2, pady=2)
        self.pic_10.grid(row=9, padx=2, pady=2)

        browse_1 = Button(
            self.trainFrame,
            text="Browse",
            command=lambda: self._set_text(self.pic_1, fd.askopenfilename()),
        )
        browse_2 = Button(
            self.trainFrame,
            text="Browse",
            command=lambda: self._set_text(self.pic_2, fd.askopenfilename()),
        )
        browse_3 = Button(
            self.trainFrame,
            text="Browse",
            command=lambda: self._set_text(self.pic_3, fd.askopenfilename()),
        )
        browse_4 = Button(
            self.trainFrame,
            text="Browse",
            command=lambda: self._set_text(self.pic_4, fd.askopenfilename()),
        )
        browse_5 = Button(
            self.trainFrame,
            text="Browse",
            command=lambda: self._set_text(self.pic_5, fd.askopenfilename()),
        )
        browse_6 = Button(
            self.trainFrame,
            text="Browse",
            command=lambda: self._set_text(self.pic_6, fd.askopenfilename()),
        )
        browse_7 = Button(
            self.trainFrame,
            text="Browse",
            command=lambda: self._set_text(self.pic_7, fd.askopenfilename()),
        )

        browse_8 = Button(
            self.trainFrame,
            text="Browse",
            command=lambda: self._set_text(self.pic_8, fd.askopenfilename()),
        )

        browse_9 = Button(
            self.trainFrame,
            text="Browse",
            command=lambda: self._set_text(self.pic_9, fd.askopenfilename()),
        )

        browse_10 = Button(
            self.trainFrame,
            text="Browse",
            command=lambda: self._set_text(self.pic_10, fd.askopenfilename()),
        )

        browse_1.grid(row=0, column=1, padx=2, pady=2)
        browse_2.grid(row=1, column=1, padx=2, pady=2)
        browse_3.grid(row=2, column=1, padx=2, pady=2)
        browse_4.grid(row=3, column=1, padx=2, pady=2)
        browse_5.grid(row=4, column=1, padx=2, pady=2)
        browse_6.grid(row=5, column=1, padx=2, pady=2)
        browse_7.grid(row=6, column=1, padx=2, pady=2)
        browse_8.grid(row=7, column=1, padx=2, pady=2)
        browse_9.grid(row=8, column=1, padx=2, pady=2)
        browse_10.grid(row=9, column=1, padx=2, pady=2)

        train = Button(self.trainFrame, text="Train", command=self.train_cmd)
        cancel_train = Button(self.trainFrame, text="Cancel", command=self.cancel_cmd)
        train.grid(row=10, padx=2, pady=2)
        cancel_train.grid(row=10, column=1, padx=2, pady=2)

    def train_cmd(self):
        """
        Perform training after validating images.
        """
        images = []
        if not self.pic_1.get():
            tkinter.messagebox.showerror(
                title="User Training", message="Picture 1 missing"
            )
            return
        if not self.pic_2.get():
            tkinter.messagebox.showerror(
                title="User Training", message="Picture 2 missing"
            )
            return
        if not self.pic_3.get():
            tkinter.messagebox.showerror(
                title="User Training", message="Picture 3 missing"
            )
            return
        if not self.pic_4.get():
            tkinter.messagebox.showerror(
                title="User Training", message="Picture 4 missing"
            )
            return
        if not self.pic_5.get():
            tkinter.messagebox.showerror(
                title="User Training", message="Picture 5 missing"
            )
            return

        if not self.pic_6.get():
            tkinter.messagebox.showerror(
                title="User Training", message="Picture 6 missing"
            )
            return
        if not self.pic_7.get():
            tkinter.messagebox.showerror(
                title="User Training", message="Picture 7 missing"
            )
            return
        if not self.pic_8.get():
            tkinter.messagebox.showerror(
                title="User Training", message="Picture 8 missing"
            )
            return
        if not self.pic_9.get():
            tkinter.messagebox.showerror(
                title="User Training", message="Picture 9 missing"
            )
            return
        if not self.pic_10.get():
            tkinter.messagebox.showerror(
                title="User Training", message="Picture 10 missing"
            )
            return

        # all is good now append the images in array
        images.append(self.pic_1.get())
        images.append(self.pic_2.get())
        images.append(self.pic_3.get())
        images.append(self.pic_4.get())
        images.append(self.pic_5.get())
        images.append(self.pic_6.get())
        images.append(self.pic_7.get())
        images.append(self.pic_8.get())
        images.append(self.pic_9.get())
        images.append(self.pic_10.get())

        self._train_by_pic(images)

    def cancel_cmd(self):
        """
        Close training form.
        """
        self.trainFrame.destroy()
        self.trainFrame = None

    def show_detect_camera(self):
        """
        Show detect camera for facial recognition
        """
        print("show_facial_detection_camera")

        self.stopEvent.clear()

        self.detectFrame = Frame(self.root)
        self.detectFrame.pack(side="top")

        video = Label(self.detectFrame)
        message = Label(self.detectFrame, font=("Helvetica", 16))
        video.grid(row=0, padx=2, pady=2)
        message.grid(row=1, padx=2, pady=2)

        trainer_file = os.path.join(self.dirname, "../trainer.yml")

        if not os.path.exists(trainer_file):
            msg_text = "Training file missing!\n No User registered."
            message.configure(text=msg_text)
            message.text = msg_text
            return

        recognizer = cv2.face.LBPHFaceRecognizer_create()
        recognizer.read(trainer_file)

        faceCascade = cv2.CascadeClassifier(self.classifier_filename)
        font = cv2.FONT_HERSHEY_SIMPLEX
        # init id counter
        id = 0
        user_obj = User()
        names = {}
        users = user_obj.get_users()
        for item in users:
            names[item[0]] = item[1]
        # Initialize and start realtime video capture
        cam = cv2.VideoCapture(0)
        cam.set(3, 640)  # video width
        cam.set(4, 480)  # video height
        # window size for face.
        minW = 0.1 * cam.get(3)
        minH = 0.1 * cam.get(4)

        try:
            while not self.stopEvent.is_set():

                ret, img = cam.read()

                if self.stopEvent.is_set():
                    print("Exit facial detection camera")
                    break
                #  for raspberry pi may require a flip img = cv2.flip(img, -1)
                gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

                faces = faceCascade.detectMultiScale(
                    gray,
                    scaleFactor=1.2,
                    minNeighbors=5,
                    minSize=(int(minW), int(minH)),
                )
                for (x, y, w, h) in faces:
                    cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 2)
                    id, confidence = recognizer.predict(gray[y : y + h, x : x + w])
                    # Check if confidence is less them 100
                    if confidence < 100:
                        print(f"user_id:{id}")
                        # run query to get user room.
                        if os.uname()[4][:3] == "arm":
                            user_obj = User()
                            pin = user_obj.get_user_room_pin(id)
                            if bool(pin):
                                self.pin_manager.pin_high(pin[0])
                                print(f"user pin:{pin[0]}")
                            # hardware call
                            # turn on lights of common rooms and user assigned room.
                            room_obj = Room()
                            pins = room_obj.get_common_room_pins()
                            for pin in pins:
                                print(f"common:{pin[0]}")
                                self.pin_manager.pin_high(pin[0])

                        id = names[id]
                        confidence = "  {0}%".format(round(100 - confidence))
                    else:
                        id = "unknown"
                        confidence = "  {0}%".format(round(100 - confidence))

                    cv2.putText(
                        img, str(id), (x + 5, y - 5), font, 1, (255, 255, 255), 2
                    )
                    cv2.putText(
                        img,
                        str(confidence),
                        (x + 5, y + h - 5),
                        font,
                        1,
                        (255, 255, 0),
                        1,
                    )

                # if the panel is not None, we need to initialize it
                image = Image.fromarray(img)
                image = ImageTk.PhotoImage(image)
                video.configure(image=image)
                video.image = image
                if id and id != "unknown":
                    msg_txt = f"Welcome {id}"
                else:
                    msg_txt = ""
                message.configure(text=msg_txt)
                message.text = msg_txt
                id = ""
                self.completeEvent.set()
        except Exception as e:
            print(f"[INFO] Facial detection camera closed {e}. ")
        cam.release()

    def close_detect_camera(self):
        """ close camera
        """
        self.stopEvent.set()
        self.detectFrame.destroy()
        self.detectFrame = None
