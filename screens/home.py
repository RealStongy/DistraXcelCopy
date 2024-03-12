import tkinter as tk
import customtkinter as ctk
from tkinter import ttk, messagebox, PhotoImage
from UI.toggle_switch import ToggleSwitch
from services.size import *
from PIL import Image, ImageTk
from tkmacosx import Button
import UI.shapes as shapes
import sys
import services.settings as settings


class HomeScreen(ctk.CTkFrame):

    def __init__(self, parent, bg_color="#000000"):
        super().__init__(parent)
        self.parent = parent
        self.default_categories = [
            "Social Media", "Video Games", "Shopping", "News", "Sports"
        ]
        self.default_values = [False, False, False, False, False]

        if sys.platform == "darwin":
            print("We are running in Mac OS")
            btn_font = ("Arial", 20)
            self.entry_height = 65
            self.delete_icon = PhotoImage(file="assets/DeleteIcon.png")
            # self.delete_icon = PhotoImage(file="assets/DeleteIcon2.png")
        else:
            print("We are running in Windows")
            btn_font = ("Arial", 24)
            self.entry_height = 75
            self.delete_icon = PhotoImage(file="assets\DeleteIcon.png")

        self.delete_icon = self.delete_icon.subsample(6, 6)
        self.style = ttk.Style()
        self.style.configure("Icon.TButton", background="#bbbbbb")

        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(2, weight=1)
        self.grid_rowconfigure(3, weight=0)
        # toggleFrame = tk.Frame(self)
        # toggleFrame.grid(column=0, row=0, sticky=tk.NW)

        # add a label over the first column above the category buttons
        label = tk.Label(self, text="Categories", font=("Arial", 24))
        label.grid(column=0, row=0, sticky=tk.N)

        # add a label over the second column above the search bar
        label = tk.Label(self, text="Blacklist", font=("Arial", 24))
        label.grid(column=1, row=0, sticky=tk.N)

        self.create_category_buttons(column=0,
                                     entry_height=self.entry_height,
                                     elements=self.default_categories,
                                     elementValues=self.default_values)
        self.create_category_buttons(
            column=1,
            includeSearch=True,
            entry_height=self.entry_height,
            elements=["youtube.com", "twitter.com", "Steam"],
            elementValues=self.default_values,
            use_toggle=False)  # TODO: replace with user data

        # Navbar frame setup
        self.navbar_frame = tk.Frame(self, bg="#656565")
        self.navbar_frame.grid(column=0, row=3, sticky="ew", columnspan=3)
        self.navbar_frame.grid_columnconfigure(0, weight=1)
        self.navbar_frame.grid_columnconfigure(1, weight=1)
        self.navbar_frame.grid_columnconfigure(2, weight=1)
        self.navbar_frame.grid_columnconfigure(3, weight=1)
        # self.navbar_frame.grid_columnconfigure(4, weight=1)

        # Create buttons within the navbar
        # btn_font = ("Arial", 24)
        btn_bg_color = "#656565"
        btn_fg_color = "#ffffff"
        btn_active_bg_color = "#656565"
        btn_active_fg_color = "#ffffff"

        # Assuming the height of buttons is 10% of the screen height
        button_height = percent(height=0.10)

        # Calculate width for the settings button (making it a square)
        settings_btn_width = button_height

        # Calculate the total width available for the other buttons
        total_navbar_width = self.parent.winfo_screenwidth()  # or SCREEN_WIDTH
        remaining_width = total_navbar_width - settings_btn_width

        # Divide the remaining width by the number of other buttons
        other_btn_width = remaining_width / 3

        # Create buttons within the navbar
        commands = [
            parent.focus_button, parent.home_button, parent.stats_button
        ]
        for i in range(0, 3):
            button_text = ["Focus", "Home", "Stats"][i]
            btn = Button(self.navbar_frame,
                         text=button_text,
                         font=btn_font,
                         height=button_height,
                         bg=btn_bg_color,
                         fg=btn_fg_color,
                         borderless=1,
                         activebackground=btn_active_bg_color,
                         activeforeground=btn_active_fg_color,
                         command=commands[i])
            btn.grid(row=0, column=i, sticky="nsew")

        # Settings button
        settings_btn = Button(self.navbar_frame,
                              bg=btn_bg_color,
                              fg=btn_fg_color,
                              height=button_height,
                              activebackground=btn_active_bg_color,
                              activeforeground=btn_active_fg_color,
                              command=lambda: parent.watcher.take_screenshot(
                                  "test", analyze=True))
        #   command=lambda: settings.show_settings(self))
        settings_btn.grid(row=0, column=3, sticky="nsew")

    def update_category_preferences(self, idx):
        category_preferences = self.default_values
        if "categories" in self.parent.singleton.get_user_data():
            category_preferences = self.parent.singleton.get_user_data(
            )["categories"]
        print(
            f"Here are the category preferences before changing {idx}: {category_preferences}"
        )
        category_preferences[idx] = not category_preferences[idx]
        print(
            f"Here are the new category preferences after changing {idx}: {category_preferences}"
        )
        self.parent.db.child("users").child(
            self.parent.uid).child("categories").set(category_preferences)

    def on_enter(self, event):
        print("Enter key pressed!")
        print(self.search_bar.get())
        enter_value = self.search_bar.get().strip().lower()

        current_blacklist = {}
        print(
            f"Singleton's current blacklist {self.parent.singleton.get_user_data()}"
        )
        if "blacklist" in self.parent.singleton.get_user_data():
            current_blacklist = self.parent.singleton.get_user_data(
            )["blacklist"]
        print(f"Here is the blacklist before adding: {current_blacklist}")

        if enter_value in self.parent.singleton.valid_program_names:
            # assume user is blocking a program
            if "programs" in current_blacklist:
                current_blacklist["programs"].append(enter_value)
            else:
                current_blacklist["programs"] = [enter_value]
        elif self.parent.singleton.check_if_website(enter_value):
            # assume website
            if "websites" in current_blacklist:
                current_blacklist["websites"].append(enter_value)
            else:
                current_blacklist["websites"] = [enter_value]
        else:
            print("Invalid blacklist entry!")
            return False

        if "merged" in current_blacklist:
            current_blacklist["merged"].append(enter_value)
        else:
            current_blacklist["merged"] = [enter_value]

        self.parent.db.child("users").child(
            self.parent.uid).child("blacklist").set(current_blacklist)
        print(f"Here is what we are adding to the db now: {current_blacklist}")
        return True

    def delete_blacklist_entry(self, entry_name):
        current_blacklist = {}
        print(f"Attempting to delete {entry_name} from blacklist")
        if "blacklist" in self.parent.singleton.get_user_data():
            current_blacklist = self.parent.singleton.get_user_data(
            )["blacklist"]
        print(f"Here is the blacklist before deleting: {current_blacklist}")
        current_blacklist["merged"].remove(entry_name)

        if self.parent.singleton.check_if_website(entry_name):
            current_blacklist["websites"].remove(entry_name)
        else:
            current_blacklist["programs"].remove(entry_name)

        print(f"Here is the blacklist after deleting: {current_blacklist}")
        self.parent.db.child("users").child(
            self.parent.uid).child("blacklist").set(current_blacklist)

    def clear_category_buttons(self):
        print("Attempting refresh of homepage...")
        for widget in self.winfo_children():
            if isinstance(widget, tk.Frame) and widget != self.navbar_frame:
                widget.destroy()

    def create_category_buttons(self,
                                column=0,
                                includeSearch=False,
                                entry_height=75,
                                elements=[],
                                elementValues=[],
                                use_toggle=True):
        frame = tk.Frame(self, bg="#d9d9d9")
        frame.grid(row=1, column=column, sticky="nsew")
        frame.grid_columnconfigure(0, weight=1)

        if includeSearch:
            border = tk.Frame(frame, bg="#bbbbbb", padx=16, pady=16)
            border.grid(row=0, column=0, padx=10, pady=10,
                        sticky="ew")  # Use grid instead of pack
            self.search_bar = tk.Entry(border,
                                       width=30,
                                       font=("Arial", 25),
                                       bg="#d9d9d9")
            self.search_bar.grid(row=0, column=0, sticky="ew")  # Use grid
            self.search_bar.bind("<Return>", self.on_enter)
            self.search_bar.bind("<Enter>", self.on_enter)

        user_data = self.parent.singleton.get_user_data()
        print(f"Testing: {user_data['categories']}")
        for i in range(len(elements)):
            category_canvas = tk.Canvas(frame,
                                        bg="#d9d9d9",
                                        height=self.entry_height,
                                        width=percent(width=0.45))
            category_canvas.configure(highlightthickness=0)
            category_canvas.grid(row=i + 1 if includeSearch else i,
                                 column=0,
                                 padx=10,
                                 pady=5,
                                 sticky="ew")

            shapes.round_rectangle(category_canvas,
                                   0,
                                   0,
                                   category_canvas.winfo_reqwidth(),
                                   self.entry_height,
                                   radius=50,
                                   fill="#bbbbbb")

            txt = tk.Label(category_canvas,
                           text=elements[i],
                           font=("Arial", 25),
                           bg="#bbbbbb")
            txt.place(x=10, y=10)

            if use_toggle:
                toggle = ToggleSwitch(
                    category_canvas,
                    default_state=elementValues[i],
                    callback=lambda i=i: self.update_category_preferences(i))
                toggle.place(x=category_canvas.winfo_reqwidth() - 80, y=22.5)
            else:
                # /Users/tonton/Documents/GitHub/DistraXcel/DistraXcel_/assets/DeleteIcon.png
                # icon = PhotoImage(file="assets/DeleteIcon.png")
                # print(f"ICON: {icon}")
                delete_button = ttk.Button(  # TODO Convert to circle icon or icon alone
                    category_canvas,
                    #    text="Delete",
                    image=self.delete_icon,
                    style="Icon.TLabel",
                    command=lambda i=i: self.delete_blacklist_entry(elements[i]
                                                                    ))
                delete_button.place(x=category_canvas.winfo_reqwidth() - 80,
                                    y=12.5)

        frame.grid(row=1, column=column)

    def update_with_new_data(self, data):
        # print(self.parent.singleton.get_user_data())
        if data["path"] == "/":
            print(f"Homescreen got new data: {data['data']['categories']}")
            updated_categories = data["data"]["categories"]
        else:
            updated_categories = self.parent.singleton.get_user_data(
            )["categories"]

        merged_list = []
        if "blacklist" in self.parent.singleton.get_user_data(
        ) and "merged" in self.parent.singleton.get_user_data()["blacklist"]:
            merged_list = self.parent.singleton.get_user_data(
            )["blacklist"]["merged"]

        self.clear_category_buttons()

        self.create_category_buttons(column=0,
                                     entry_height=self.entry_height,
                                     elements=self.default_categories,
                                     elementValues=updated_categories)
        self.create_category_buttons(column=1,
                                     includeSearch=True,
                                     entry_height=self.entry_height,
                                     elements=merged_list,
                                     use_toggle=False)
