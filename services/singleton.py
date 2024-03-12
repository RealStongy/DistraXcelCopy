import re
import threading
import time


class UserData:  # TODO: the timer currently has a major acceleration issue that needs adjustment
    _instance = None

    model_label_to_name = {"facebook": "facebook.com"}

    valid_program_names = {
        "steam", "league of legends", "roblox", "minecraft", "fortnite",
        "discord", "battle.net", "genshin impact", "stockfish", "wechat",
        "musescore 3", "google chrome", "firefox", "opera", "safari",
        "facetime"
    }

    valid_category_names = {
        "Social Media": {
            "WeChat.exe", "Discord.exe", "Discord", "FaceTime", "WeChat",
            "Zoom", "Zoom.exe"
        },
        "Video Games": {
            "LeagueClient.exe", "Steam.exe", "RobloxPlayerBeta.exe",
            "MinecraftLauncher.exe", "FortniteClient-Win64-Shipping.exe",
            "Battle.net.exe", "GenshinImpact.exe", "Stockfish 13.exe", "Steam",
            "RobloxPlayerBeta", "MinecraftLauncher",
            "FortniteClient-Win64-Shipping", "Battle.net", "GenshinImpact",
            "Stockfish 13"
        },
        "Shopping": {
            "Google Chrome.exe", "Firefox.exe", "Opera.exe", "Safari.exe",
            "Safari", "Google Chrome", "Firefox", "Opera"
        },
        "News": {
            "Google Chrome.exe", "Firefox.exe", "Opera.exe", "Safari.exe",
            "Safari", "Google Chrome", "Firefox", "Opera"
        },
        "Sports": {
            "Google Chrome.exe", "Firefox.exe", "Opera.exe", "Safari.exe",
            "Safari", "Google Chrome", "Firefox", "Opera"
        },
    }

    def __init__(self):
        self.is_working = True
        self.timer_active = False
        self.timer_should_run = False
        self.timer_seconds_remaining = 600
        self.timer_callback = None
        self.timer_thread = None
        # self.timer_lock = threading.Lock()

        if UserData._instance is not None:
            raise Exception("This class is a singleton!")
        else:
            UserData._instance = self
            self.user_data = {
                "blacklist": {},
                "whitelist": {},
                "categories": [False] * 5,
                "settings": {
                    "pomodoro_work_slider_val": 50,
                    "pomodoro_rest_slider_val": 50,
                    "dark_mode": False,
                    "consecutive_cycles": 1
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

    @classmethod
    def get_instance(cls):
        if cls._instance is None:
            cls._instance = UserData()
        return cls._instance

    def set_user_data(self, data):
        # print(data)

        formatted_data = {
            "blacklist":
            data.get("blacklist", {}),
            "whitelist":
            data.get("whitelist", {}),
            "categories":
            data.get("categories", [False] * 5),
            "settings":
            data.get(
                "settings", {
                    "pomodoro_work_slider_val": 50,
                    "pomodoro_rest_slider_val": 50,
                    "dark_mode": False,
                    "consecutive_cycles": 1
                }),
            "stats":
            data.get(
                "stats",
                {
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
                })
        }

        # print(formatted_data)
        self.user_data = formatted_data

    def get_user_data(self):
        return self.user_data

    def check_if_website(self, potential_url):
        pattern = re.compile(
            r'^(https?:\/\/)?'  # http:// or https://
            r'(([a-zA-Z0-9-]+\.)+[a-zA-Z]{2,6})'  # domain
            r'(\/[a-zA-Z0-9@:%._\+~#?&//=]*)?$')  # path, query, fragment
        return bool(pattern.match(potential_url))

    def start_timer(self, amount, callback, root):
        self.timer_seconds_remaining = amount
        self.timer_callback = callback
        self.timer_active = True
        self._run_timer(root)
        # if not self.timer_active:
        #     self.timer_active = True
        #     self.timer_should_run = True
        #     # if self.timer_thread:
        #     #     # self.timer_thread.cancel()
        #     #     self.timer_thread = None

        #     # Move to background thread
        #     self.timer_thread = threading.Thread(target=self._run_timer)
        #     self.timer_thread.start()

    def _run_timer(self, root):
        if self.timer_seconds_remaining > 0 and self.timer_active:
            self.timer_seconds_remaining -= 1
            # print(f"HERE IS MY CALLBACK AT TIME {self.timer_seconds_remaining}: {self.timer_callback}")
            if self.timer_callback:
                self.timer_callback(self.timer_seconds_remaining)
            root.after(1000, lambda: self._run_timer(root))
        else:
            self.timer_active = False

    def stop_timer(self):
        self.timer_active = False

    def reset_timer(self, reset_value=600):
        print("RESETTING THE TIMER")
        self.stop_timer()
        # self.timer_should_run = False
        # if self.timer_thread:
        #     self.timer_thread.join()
        self.timer_seconds_remaining = reset_value
        if self.timer_callback:
            self.timer_callback(self.timer_seconds_remaining)
        # self.timer_thread = None

    def is_timer_running(self):
        return self.timer_active
