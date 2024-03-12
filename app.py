import tkinter as tk
import customtkinter as ctk
import services.firebaseAuthentication as firebaseAuthentication
from services.size import *
import services.watcher as watcher
from screens.home import HomeScreen
from screens.focus import FocusScreen
from screens.stats import StatsScreen
from login import LoginScreen
from signup import SignupScreen
from services.singleton import UserData
import queue

skip_login = False


class App(ctk.CTk):

    def __init__(self):
        # Initial Tasks
        super().__init__()
        self.protocol("WM_DELETE_WINDOW", self.on_closing)
        self.singleton = UserData.get_instance()
        self.uid = ""
        self.db = firebaseAuthentication.db
        self.queue = queue.Queue()
        self.poll_queue()

        # Window Properties
        self.configure(bg="#ececec")
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        SCREEN_WIDTH = int(screen_width * 0.5)
        SCREEN_HEIGHT = int(screen_height * 0.5)
        self.geometry(f"{SCREEN_WIDTH}x{SCREEN_HEIGHT}")
        self.title("DistraXcel")
        self.resizable(False, False)

        # Setup Content Screens
        self.screens = {}
        for screen_class in [HomeScreen, FocusScreen, StatsScreen]:
            screen = screen_class(self, "#ececec")
            screen.grid(row=0, column=0, sticky="nsew")
            self.screens[screen_class] = screen
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        # User Settings
        self.check_login_status()
        if not self.check_login_status():
            self.withdraw()
            self.show_screen(LoginScreen)
        self.current_screen = ""
        self.home_button(initial=True)
        self.settings_open = False
        self.watcher = watcher.Watcher(model_path="models/bestLite.pt")

        # print(sorted(self.watcher.get_running_programs()))
        # print(self.watcher.get_mac_application_list())
        self.debug_task()

    def debug_task(self):
        running_programs = self.watcher.get_running_programs()
        for program in running_programs:
            if self.singleton.get_user_data()["categories"][
                    0] and program in self.singleton.valid_category_names[
                        "Social Media"]:
                print(f"{program} is a social media program!")
                self.watcher.kill_program(program)
            if self.singleton.get_user_data()["categories"][
                    1] and program in self.singleton.valid_category_names[
                        "Video Games"]:
                print(f"{program} is a video game!")
                self.watcher.kill_program(program)
            if self.singleton.get_user_data()["categories"][
                    2] and program in self.singleton.valid_category_names[
                        "Shopping"]:
                print(f"{program} is a shopping program!")
                self.watcher.kill_program(program)
            if self.singleton.get_user_data()["categories"][
                    3] and program in self.singleton.valid_category_names[
                        "News"]:
                print(f"{program} is a news program!")
                self.watcher.kill_program(program)
            if self.singleton.get_user_data()["categories"][
                    4] and program in self.singleton.valid_category_names[
                        "Sports"]:
                print(f"{program} is a sports program!")
                self.watcher.kill_program(program)

        self.after(5000, self.debug_task)

    def check_screen(self):
        result = self.watcher.take_screenshot()
        for item in result:

            print(item)

    def trigger_event(self, event_flag):
        self.event_generate(event_flag)

    def poll_queue(self):
        try:
            message = self.queue.get_nowait()
            self.handle_queue_events(message)
        except queue.Empty:
            pass
        finally:
            self.after(100, self.poll_queue)

    def handle_queue_events(self, message):
        print(f"QUEUE EVENT: {message}")
        self.screens[HomeScreen].update_with_new_data(message)
        self.screens[FocusScreen].update_with_new_data(message)

    def check_login_status(self):
        id_token = firebaseAuthentication.get_valid_id_token()
        # user_token = keyring.get_password("DistraXcel", "user_id_token")
        if id_token:
            print("User should already be logged in!")
            user = firebaseAuthentication.get_user_from_token(id_token)
            db = firebaseAuthentication.db
            user_data = db.child("users").child(user["user_id"]).get().val()
            self.uid = user["user_id"]
            user_data_singleton = UserData.get_instance()
            user_data_singleton.set_user_data(user_data)
            firebaseAuthentication.start_firebase_listener(self, self.screens)
            return True
        else:
            print("No one is logged in!")
            return False

    def show_screen(self, screen):
        if screen == LoginScreen:
            print("Going to login screen")
            self.login_screen = LoginScreen(self)
        else:
            self.deiconify()
            screen = self.screens[screen]
            screen.tkraise()

    def focus_button(self):
        print("Focus Clicked!")
        if self.current_screen == "focus":
            print("Already on the focus screen")
            return
        self.current_screen = "focus"
        self.show_screen(FocusScreen)

    def home_button(self, initial=False):
        print("Home Clicked!")
        if self.current_screen == "home" and not initial:
            self.deiconify()
            print("Already on the home screen")
            return
        self.current_screen = "home"
        self.show_screen(HomeScreen)

    def stats_button(self):
        print("Stats Clicked!")
        if self.current_screen == "stats":
            return
        self.current_screen = "stats"
        self.show_screen(StatsScreen)

    def returnToLogin(self):
        # homeScreen.destroy()
        print("Returning to home screen.")
        # login()

        # Close current windows
        self.withdraw()
        # self.login_screen.destroy()
        # self.settings_window.destroy()
        # self.screens[HomeScreen].destroy()
        # self.screens[FocusScreen].destroy()
        # self.screens[StatsScreen].destroy()

        # Return to login
        self.signup_to_login()

    def login_to_signup(self):
        SignupScreen(self)

    def signup_to_login(self):
        LoginScreen(self)

    def on_closing(self):
        print("Closing...")
        self.withdraw()
        self.destroy()
