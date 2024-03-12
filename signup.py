import tkinter as tk
from tkinter import ttk, messagebox
import services.firebaseAuthentication as firebaseAuthentication
from services.size import *


class SignupScreen(tk.Toplevel):

    def __init__(self, parent, bg_color="#000000"):
        super().__init__(parent)
        self.parent = parent

        self.geometry("280x115")
        self.title('Signup')
        self.resizable(False, False)

        # configure the grid
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=3)

        self.create_widgets()

    def create_widgets(self):
        pass
        # username
        username_label = ttk.Label(self, text="Email:")
        username_label.grid(column=0, row=0, sticky=tk.W, padx=5, pady=5)

        self.username_entry = ttk.Entry(self)
        self.username_entry.grid(column=1, row=0, sticky=tk.E, padx=5, pady=5)

        # password
        self.password_label = ttk.Label(self, text="Password:")
        self.password_label.grid(column=0, row=1, sticky=tk.W, padx=5, pady=5)

        self.password_entry = ttk.Entry(self, show="*")
        self.password_entry.grid(column=1, row=1, sticky=tk.E, padx=5, pady=5)

        # back button
        back_button = ttk.Button(self, text="Back", command=self.back_to_login)
        back_button.grid(column=1, row=2, sticky=tk.SE, padx=5, pady=5)

        # signup button
        signup_button = ttk.Button(self,
                                   text="Signup",
                                   command=self.signup_to_home)
        signup_button.grid(column=1, row=2, sticky=tk.SW, padx=5, pady=5)

    def back_to_login(self):
        self.destroy()
        # LoginScreen(self.parent)
        self.parent.signup_to_login()

    def signup_to_home(self):
        username = self.username_entry.get()
        password = self.password_entry.get()

        user = firebaseAuthentication.signup(username, password)
        firebaseAuthentication.start_firebase_listener(self.parent,
                                                       self.parent.screens)

        if (user is not None):
            db = firebaseAuthentication.db

            default_user_data = {
                "blackList": [],
                "whiteList": [],
                "categories": [False] * 5,
                "settings": {
                    "pomodoro_work_slider_val": 25,
                    "pomodoro_rest_slider_val": 5,
                    "dark_mode": False
                },
                "stats": {
                    "block_count":
                    dict(),  # number of times a given program was blocked
                    "category_block_count": dict(
                    ),  # number of times something from a category was blocked
                    "focus_time":
                    0,  # total amount of time (in minutes) spent on focus mode during pomodoro session 
                    "rest_time":
                    0,  # total amount of time (in minutes) spent on break mode during pomodoro sessions
                    "current_focus_streak":
                    0,  # current daily consecutive uses of pomodoro
                    "longest_focus_streak":
                    0,  # longest daily consecutive uses of pomodoro
                }
            }

            db.child("users").child(user["localId"]).set(default_user_data)

            self.destroy()
            self.parent.home_button()
        else:
            tk.messagebox.showerror("error", "invalid email / password")
