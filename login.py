import tkinter as tk
from tkinter import ttk, messagebox
import services.firebaseAuthentication as firebaseAuthentication
from services.size import *
import keyring
from signup import SignupScreen
from services.singleton import UserData
"""
{'kind': 'identitytoolkit#VerifyPasswordResponse', 
'localId': 'bPzXQDEhDHcpu1FRZCUklwgzylw2', 
'email': 'test3@gmail.com', 
'displayName': '', 
'idToken': 'eyJhbGciOiJSUzI1NiIsImtpZCI6ImQxNjg5NDE1ZWMyM2EzMzdlMmJiYWE1ZTNlNjhiNjZkYzk5MzY4ODQiLCJ0eXAiOiJKV1QifQ.eyJpc3MiOiJodHRwczovL3NlY3VyZXRva2VuLmdvb2dsZS5jb20vZGlzdHJheGNlbCIsImF1ZCI6ImRpc3RyYXhjZWwiLCJhdXRoX3RpbWUiOjE3MDQ1ODU3MTEsInVzZXJfaWQiOiJiUHpYUURFaERIY3B1MUZSWkNVa2x3Z3p5bHcyIiwic3ViIjoiYlB6WFFERWhESGNwdTFGUlpDVWtsd2d6eWx3MiIsImlhdCI6MTcwNDU4NTcxMSwiZXhwIjoxNzA0NTg5MzExLCJlbWFpbCI6InRlc3QzQGdtYWlsLmNvbSIsImVtYWlsX3ZlcmlmaWVkIjpmYWxzZSwiZmlyZWJhc2UiOnsiaWRlbnRpdGllcyI6eyJlbWFpbCI6WyJ0ZXN0M0BnbWFpbC5jb20iXX0sInNpZ25faW5fcHJvdmlkZXIiOiJwYXNzd29yZCJ9fQ.PkeusX6y9kWr3NyaCg7Yd0OvoshPwlVfnUHaU8TFIWchDod8VySTmvC098dR8aQuaJBiqmK1vqdQylOg34ymOqWkX4jd40MKvmzxQ8pjLEHw48_uTE0PB4UiYcyQEamlr1XNquStbdLXUIQhCx6Usd7yHHGyJSPwuW4uHq3PWHrjx4EZpo8obyrKPtpTVsVK947F94c2mRIxJZgJPTLA95VCz6vpX4j4HREAU88xs3NQDHYVLX9p-FMToSMgyGS2IyoJuG0hgjtU_ht01vjVknQ4c-8QFlHn9OEe-WeUww1M_cWPmuhAJtZ_oLfYUAolqEWFqCDRMBv-KSyyd-zjGg',
'registered': True, 
'refreshToken': 'AMf-vBz5YDUXimTSIRXeYb24IBp6NSBmSBsSJcO0GisJ8rw2ZsTFEZngvpHMjOqWPJGZtVvqsY3xZEyfSNyhYCvYFkbXypnGoi8xoswC96ju7I00HuUwvocqwJ9TeQk7bI177qs_AAGip3ju4vkyGZWASuLTnSSfH268FzENM-I1YI2NbIL0j2V3YQ6pNlnLHKg_1gyA7pt9',
'expiresIn': '3600'}

"""


class LoginScreen(tk.Toplevel):

    def __init__(self, parent, bg_color="#000000"):
        super().__init__(parent)
        self.parent = parent
        # if sys.platform == "darwin":
        #     print("We are running in Mac OS")
        #     btn_font = ("Arial", 20)
        #     entry_height = 65
        # else:
        #     print("We are running in Windows")
        #     btn_font = ("Arial", 24)
        #     entry_height = 75

        self.geometry("280x115")
        self.title('DistraXcel v.1.0 Login')
        self.resizable(False, False)

        # configure the grid
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=3)

        self.create_widgets()

    def create_widgets(self):
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

        # login button
        login_button = ttk.Button(self,
                                  text="Login",
                                  command=self.login_to_home)
        login_button.grid(column=1, row=2, sticky=tk.SE, padx=5, pady=5)

        # signup button
        signup_button = ttk.Button(self,
                                   text="Signup",
                                   command=self.open_signup)
        signup_button.grid(column=1, row=2, sticky=tk.SW, padx=5, pady=5)

    def login_to_home(self):
        username = self.username_entry.get()
        password = self.password_entry.get()

        user = firebaseAuthentication.login(username, password)
        firebaseAuthentication.start_firebase_listener(self.parent,
                                                       self.parent.screens)

        if user is not None:
            # Store the ID/refresh tokens
            keyring.set_password("DistraXcel", "user_id_token",
                                 user["idToken"])
            keyring.set_password("DistraXcel", "user_refresh_token",
                                 user["refreshToken"])

            # update local user data with user's data
            db = firebaseAuthentication.db
            user_data = db.child("users").child(user["localId"]).get().val()
            user_data_singleton = UserData.get_instance()
            user_data_singleton.set_user_data(user_data)

            # Go to home screen
            self.parent.home_button(initial=True)
            self.destroy()
        else:
            messagebox.showerror("error", "invalid email / password")

    def open_signup(self):
        SignupScreen(self.parent)
        self.destroy()


# def login():
#     global loginScreen, username_entry, password_entry
#     loginScreen = tk.Tk()
#     loginScreen.geometry("280x115")
#     loginScreen.title('Login')
#     loginScreen.resizable(False, False)

#     # print(f"TESTING: {firebaseAuthentication.auth.current_user}")

#     # configure the grid
#     loginScreen.columnconfigure(0, weight = 1)
#     loginScreen.columnconfigure(1, weight = 3)

#     # username
#     username_label = ttk.Label(loginScreen, text = "Email:")
#     username_label.grid(column = 0, row = 0, sticky = tk.W, padx = 5, pady = 5)

#     username_entry = ttk.Entry(loginScreen)
#     username_entry.grid(column = 1, row = 0, sticky = tk.E, padx = 5, pady = 5)

#     # password
#     password_label = ttk.Label(loginScreen, text = "Password:")
#     password_label.grid(column = 0, row = 1, sticky = tk.W, padx = 5, pady = 5)

#     password_entry = ttk.Entry(loginScreen, show = "*")
#     password_entry.grid(column = 1, row = 1, sticky = tk.E, padx = 5, pady = 5)

#     # login button
#     login_button = ttk.Button(loginScreen, text = "Login", command = login_to_Home)
#     login_button.grid(column = 1, row = 2, sticky = tk.SE, padx = 5, pady = 5)

#     # signup button
#     signup_button = ttk.Button(loginScreen, text = "Signup", command = open_Signup)
#     signup_button.grid(column = 1, row = 2, sticky = tk.SW, padx = 5, pady = 5)

#     # run
#     loginScreen.mainloop()

# def signupToHome():
#     global username_entry, password_entry

#     username = username_entry.get()
#     password = password_entry.get()

#     user = firebaseAuthentication.signup(username, password)

#     if (user != None):
#         signupScreen.destroy()
#         home()
#     else:
#         tk.messagebox.showerror("error", "invalid email / password")

# def loginToHome():
#     global username_entry, password_entry

#     username = username_entry.get()
#     password = password_entry.get()

#     user = firebaseAuthentication.login(username, password)

#     if user is not None:
#         loginScreen.destroy()
#         cache_user_credentials(username, user['idToken'])
#         home()
#     else:
#         tk.messagebox.showerror("error", "invalid email / password")

# def returnToLogin():
#     homeScreen.destroy()
#     print("Returning to home screen.")
#     login()

# def signup():
#     global signupScreen, username_entry, password_entry

#     signupScreen = tk.Tk()
#     signupScreen.geometry("280x115")
#     signupScreen.title('Signup')
#     signupScreen.resizable(False, False)

#     # configure the grid
#     signupScreen.columnconfigure(0, weight = 1)
#     signupScreen.columnconfigure(1, weight = 3)

#     # username
#     username_label = ttk.Label(signupScreen, text = "Email:")
#     username_label.grid(column = 0, row = 0, sticky = tk.W, padx = 5, pady = 5)

#     username_entry = ttk.Entry(signupScreen)
#     username_entry.grid(column = 1, row = 0, sticky = tk.E, padx = 5, pady = 5)

#     # password —— maybe remove censor / add confirm password option
#     password_label = ttk.Label(signupScreen, text = "Password:")
#     password_label.grid(column = 0, row = 1, sticky = tk.W, padx = 5, pady = 5)

#     password_entry = ttk.Entry(signupScreen, show = "*")
#     password_entry.grid(column = 1, row = 1, sticky = tk.E, padx = 5, pady = 5)

#     # login button
#     signup_button = ttk.Button(signupScreen, text = "Signup", command = signupToHome)  # command = signupToHome
#     signup_button.grid(column = 1, row = 2, sticky = tk.SE, padx = 5, pady = 5)

#     # run
#     signupScreen.mainloop()

# def openSignup():
#     loginScreen.destroy()
#     signup()
