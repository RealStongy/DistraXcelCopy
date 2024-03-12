import tkinter as tk
import customtkinter as ctk
from tkinter import ttk
from tkmacosx import Button
import UI.shapes as shapes
from services.size import *
from services.singleton import UserData
import sys
import services.settings as settings
"""
work mode: only whitelist
rest mode: full access aside from blacklist
"""


class FocusScreen(ctk.CTkFrame):

    def __init__(self, parent, bg_color="#000000"):
        super().__init__(parent)
        self.parent = parent

        # Styles and Configurations
        self.configure_grid()
        self.setup_styles()

        # Create widgets
        self.create_timer_and_controls()
        self.create_search_and_whitelist()
        self.create_navbar()

        self.bind_events()

    def configure_grid(self):
        self.grid_columnconfigure(0, weight=1, uniform="group1")
        self.grid_columnconfigure(1, weight=1, uniform="group1")
        self.grid_rowconfigure(0, weight=1)

    def setup_styles(self):
        self.btn_font = ("Arial", 20 if sys.platform == "darwin" else 24)
        self.entry_height = 65 if sys.platform == "darwin" else 75
        self.text_font_large = ("Arial", 100, "bold")
        self.text_font_small = ("Arial", 24)
        self.timer_color = "#ef5959"

    def create_search_and_whitelist(self, elements=[]):
        # Frame for the search bar and whitelist on the right side
        self.whitelist_frame = ctk.CTkFrame(self, width=200, corner_radius=10)
        self.whitelist_frame.grid(row=0, column=1, rowspan=3, sticky='nesw', padx=20, pady=20)
        # self.whitelist_frame.grid_propagate(False)
        self.whitelist_frame.grid_columnconfigure(0, weight=1)  # Allow the frame to expand horizontally
        self.whitelist_frame.grid_rowconfigure(1, weight=1)    # Allow the list frame to expand vertically


        # Search bar at the top of the whitelist frame
        self.search_bar = ctk.CTkEntry(self.whitelist_frame, placeholder_text="(Whitelist) Enter an app/website name...", width=180, height=30, corner_radius=10)
        self.search_bar.grid(row=0, column=0, padx=10, pady=(10, 0), sticky='ew')

        self.create_whitelist(self.whitelist_frame, elements)

        # Bind the search bar 'Return' event to the search function
        self.search_bar.bind('<Return>', self.on_search)

    def create_whitelist(self, parent_frame, elements=[]):
        # Frame for the list of whitelist entries
        self.whitelist_list_frame = ctk.CTkFrame(parent_frame, width=180, height=300, corner_radius=10)
        self.whitelist_list_frame.grid(row=1, column=0, padx=10, pady=10, sticky='nsew')
        self.whitelist_list_frame.grid_propagate(False)

        # Scrollable canvas for whitelist entries
        self.whitelist_canvas = tk.Canvas(self.whitelist_list_frame, bg="#d9d9d9")
        self.whitelist_canvas.pack(side='left', fill='both', expand=True)

        # Scrollbar for the whitelist entries
        self.whitelist_scrollbar = ttk.Scrollbar(self.whitelist_list_frame, orient='vertical', command=self.whitelist_canvas.yview)
        self.whitelist_scrollbar.pack(side='right', fill='y')

        # Configure the canvas to work with the scrollbar
        self.whitelist_canvas.configure(yscrollcommand=self.whitelist_scrollbar.set)
        self.whitelist_canvas.bind('<Configure>', lambda e: self.whitelist_canvas.configure(scrollregion=self.whitelist_canvas.bbox('all')))

        # Frame to hold the actual whitelist entry widgets
        self.whitelist_entries_frame = ctk.CTkFrame(self.whitelist_canvas, corner_radius=10)
        self.whitelist_canvas.create_window((0, 0), window=self.whitelist_entries_frame, anchor='nw')

        # Add whitelist entries to the whitelist_entries_frame
        # This part will be dynamic based on the actual whitelist entries you have
        # For demonstration, here's how you could add a few static entries:
        # example_whitelist = ['example.com', 'appname', 'anotherapp']
        for idx, entry in enumerate(elements):
            # entry_label = ctk.CTkLabel(self.whitelist_entries_frame, text=entry, height=25)
            # entry_label.grid(row=idx, column=0, sticky='ew', padx=5, pady=2)
            entry_frame = ctk.CTkFrame(self.whitelist_entries_frame, corner_radius=10, height=30, fg_color="#ffffff")
            entry_frame.grid(row=idx, column=0, sticky='ew', padx=5, pady=2)
            entry_frame.grid_propagate(False)
            
            entry_label = ctk.CTkLabel(entry_frame, text=entry, anchor="w")
            entry_label.pack(side="left", fill="both", expand=True, padx=10)

            delete_button = ctk.CTkButton(entry_frame, text="✕", command=lambda e=entry: self.delete_whitelist_entry(e))
            delete_button.pack(side="right", padx=10)
            
            # Make sure the frame expands to fill the canvas
            self.whitelist_entries_frame.grid_rowconfigure(idx, weight=1)
            self.whitelist_entries_frame.grid_columnconfigure(0, weight=1)


    def clear_whitelist(self):
        for widget in self.whitelist_entries_frame.winfo_children():
            widget.destroy()

    # def clear_category_buttons(self):
    #     # print("Attempting refresh of homepage...")
    #     # for widget in self.winfo_children():
    #     #     if isinstance(widget, tk.Frame) and widget != self.navbar_frame:
    #     #         widget.destroy()
    #     for widget in self.category_frame.winfo_children():
    #         widget.destroy()

    def on_search(self, event):
        search_term = self.search_bar.get()
        print(f"Search for: {search_term}")

        # Add the search term to the whitelist
        self.on_enter(event)

    def create_timer_and_controls(self):
        self.timer_and_controls_frame = ctk.CTkFrame(self)
        self.timer_and_controls_frame.grid(row=0, column=0, sticky='nesw', padx=20, pady=20)
        self.timer_and_controls_frame.grid_propagate(False)
        
        # Configure the internal grid of the frame
        self.timer_and_controls_frame.grid_rowconfigure(0, weight=1)
        self.timer_and_controls_frame.grid_rowconfigure(1, weight=1)
        self.timer_and_controls_frame.grid_columnconfigure(0, weight=1)
        
        self.create_sliders(self.timer_and_controls_frame)
        self.create_timer_label(self.timer_and_controls_frame)
        self.create_start_button(self.timer_and_controls_frame)

    def create_navbar(self):
        # Navbar frame setup
        self.navbar_frame = tk.Frame(self, bg="#656565")
        self.navbar_frame.grid(column=0, row=5, sticky="ew", columnspan=3)
        self.navbar_frame.grid_columnconfigure(0, weight=1)
        self.navbar_frame.grid_columnconfigure(1, weight=1)
        self.navbar_frame.grid_columnconfigure(2, weight=1)
        self.navbar_frame.grid_columnconfigure(3, weight=1)

        commands = [
            self.parent.focus_button, self.parent.home_button, self.parent.stats_button
        ]

        labels = ["Focus", "Home", "Stats"]

        # Create buttons within the navbar
        for i in range(0, 3):
            button_text = labels[i]
            btn = Button(self.navbar_frame,
                         text=button_text,
                         font=self.btn_font,
                        #  height=button_height,
                         bg="#656565",
                         fg="#ffffff",
                         borderless=1,
                         activebackground="#656565",
                         activeforeground="#ffffff",
                         command=commands[i])
            btn.grid(row=0, column=i, sticky="nsew")

        # Settings button
        settings_btn = Button(self.navbar_frame,
                              bg="#656565",
                              fg="#ffffff",
                              height=percent(height=0.10),
                              activebackground="#656565",
                              activeforeground="#ffffff",
                              command=lambda: settings.show_settings(self))
        settings_btn.grid(row=0, column=3, sticky="nsew")

    def get_timer_string(self):
        timer_length = int(self.workSlider.get() if self.parent.singleton.is_working else self.restSlider.get()) * 60
        timer_str = self.format_timer(timer_length)
        return timer_str

    def create_timer_label(self, parent_frame):
        timer_str = self.get_timer_string()
        self.timerText = ctk.CTkLabel(parent_frame,
                                      text=self.get_timer_string(),
                                      font=self.text_font_large,
                                      text_color=self.timer_color)
        self.timerText.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)

    def create_sliders(self, parent_frame):
        self.workText = ctk.CTkLabel(parent_frame,
                                        text="Work: 10 minutes",
                                        font=self.text_font_small)
        self.workText.grid(row=1, column=0, sticky="ew", padx=10, pady=10)
        self.workSlider = ctk.CTkSlider(parent_frame,
                                        from_=10, to=130,
                                        number_of_steps=12,
                                        command=lambda x: self.slider_callback(self.workSlider))
        self.workSlider.grid(row=2, column=0, sticky="ew", padx=10, pady=10)

        self.restText = ctk.CTkLabel(parent_frame,
                                        text="Rest: 5 minutes",
                                        font=self.text_font_small)
        self.restText.grid(row=3, column=0, sticky="ew", padx=10, pady=10)
        self.restSlider = ctk.CTkSlider(parent_frame,
                                        from_=5, to=85,
                                        number_of_steps=8,
                                        command=lambda x: self.slider_callback(self.restSlider))
        self.restSlider.grid(row=4, column=0, sticky="ew", padx=10, pady=10)

    def create_start_button(self, parent_frame):

        timer_length = int(self.workSlider.get() if self.parent.singleton.is_working else self.restSlider.get()) * 60
        self.start_btn = ctk.CTkButton(parent_frame,
                                       text="Start",
                                       height=percent(0.09),
                                       width=percent(0.1),
                                       font=self.btn_font,
                                       command=lambda: self.start_timer(timer_length))
        self.start_btn.grid(row=5, column=0, sticky="ew", padx=60, pady=20)

    def create_debug_entries(self):
        self.debug_work_entry = ctk.CTkEntry(self)
        self.debug_rest_entry = ctk.CTkEntry(self)

        # Position the debug entries below the sliders
        self.debug_work_entry.grid(row=7, column=0, pady=20)
        self.debug_rest_entry.grid(row=7, column=2, pady=20)

        self.debug_work_entry.bind("<Return>", self.on_entry_submit)
        self.debug_rest_entry.bind("<Return>", self.on_entry_submit)

    def bind_events(self):
        self.parent.bind("<<SliderSave>>", self.handle_slider_event)

    def slider_callback(self, value):
        self.workText.configure(text=f"Work: {int(value.get())} minutes") if self.workSlider == value else self.restText.configure(text=f"Rest: {int(value.get())} minutes")

    def handle_slider_event(self, event):
        # Example of saving slider values
        work_value = self.workSlider.get()
        rest_value = self.restSlider.get()
        database_ref = self.parent.db.child("users").child(self.parent.uid).child("settings")
        print(f"Saving slider values: Work={work_value}, Rest={rest_value}")

        database_ref.child("pomodoro_work_slider_val").set(work_value)
        database_ref.child("pomodoro_rest_slider_val").set(rest_value)

    def on_entry_submit(self, event):
        work_entry_val = int(self.debug_work_entry.get()) if len(
            self.debug_work_entry.get()) > 0 else 10
        rest_entry_val = int(self.debug_rest_entry.get()) if len(
            self.debug_rest_entry.get()) > 0 else 5

        print(f"WORK: {work_entry_val} REST: {rest_entry_val}")
        self.parent.db.child("users").child(self.parent.uid).child(
            "settings").child("pomodoro_work_slider_val").set(work_entry_val)
        self.parent.db.child("users").child(self.parent.uid).child(
            "settings").child("pomodoro_rest_slider_val").set(rest_entry_val)

    def create_category_buttons(self, include_search=False, elements=[]):
        # Container frame for category buttons
        self.category_frame = tk.Frame(self, bg="#d9d9d9")
        self.category_frame.grid(row=1, column=0, sticky="nsew")
        self.category_frame.grid_columnconfigure(0, weight=1)

        # Optionally include a search bar at the top of the category list
        if include_search:
            self.create_search_bar(self.category_frame)

        # Create a button for each category element
        for i, element in enumerate(elements):
            self.create_category_button(self.category_frame, element, i + int(include_search))


    def create_search_bar(self, parent_frame):
        search_bar_frame = tk.Frame(parent_frame, bg="#bbbbbb", padx=16, pady=16)
        search_bar_frame.grid(row=0, column=0, padx=10, pady=10, sticky="ew")
        self.search_bar = ctk.CTkEntry(search_bar_frame, width=300, font=("Arial", 25), bg_color="#d9d9d9")
        self.search_bar.grid(sticky="ew")
        self.search_bar.bind("<Return>", self.on_enter)

    def create_category_button(self, parent_frame, element, row):
        # Create a canvas for rounded corners if needed
        category_canvas = tk.Canvas(parent_frame, bg="#d9d9d9", height=self.entry_height, width=percent(width=0.45))
        category_canvas.configure(highlightthickness=0)
        category_canvas.grid(row=row, column=0, padx=10, pady=5, sticky="ew")

        # Create rounded rectangle on the canvas if your UI design requires it
        shapes.round_rectangle(category_canvas, 0, 0, category_canvas.winfo_reqwidth(), self.entry_height, radius=50, fill="#bbbbbb")

        # Category label
        label = tk.Label(category_canvas, text=element, font=("Arial", 25), bg="#bbbbbb")
        label.place(x=10, y=10)

        # Delete button associated with each category
        delete_btn = ttk.Button(category_canvas, text="Delete", command=lambda e=element: self.delete_whitelist_entry(e))
        delete_btn.place(x=category_canvas.winfo_reqwidth() - 80, y=22.5)

    def clear_sliders(self):
        print("Attempting clear of sliders...")
        for widget in self.winfo_children():
            if isinstance(widget, tk.Canvas) and widget != self.navbar_frame:
                # print(widget)
                widget.destroy()

    def format_timer(self, value):
        minutes, seconds = divmod(value, 60)
        return f"{minutes:02d}:{seconds:02d}"

    def start_timer(self, amount):
        print(f"TIMER RUNNING: {self.parent.singleton.is_timer_running()}")

        if not self.parent.singleton.is_timer_running():
            self.update_timer_text(amount)
            self.start_btn.configure(state=ctk.DISABLED)
            user_data = UserData.get_instance()
            user_data.start_timer(amount, self.update_timer_text, self.parent)
            
    def update_timer_text(self, value):
        # print(f"UPDATE TIMER TEXT: {value}")

        if value >= 0:
            minutes, seconds = divmod(value, 60)
            # self.timerText["text"] = f"{minutes:02d}:{seconds:02d}"
            self.timerText.configure(text=f"{minutes:02d}:{seconds:02d}")

            if value > 0:
                self.after(1000, self.update_timer_text, value - 1)
            else:
                self.start_btn["state"] = "normal"
                self.start_btn.configure(state=ctk.NORMAL)
                # if self.parent.singleton.get_user_data()["settings"]["consecutive_cycles"] > 0:
                #     print("Must transition!")
                #     self.is_work_mode = not self.is_work_mode
                #     self.transition_timer(self.is_work_mode)

    def reset_timer(self, amount):
        self.parent.singleton.reset_timer(reset_value=amount)
        self.start_btn["state"] = "normal"
        self.timerText["text"] = self.get_timer_string()

    def transition_timer(self, going_to_rest):
        self.reset_timer(10)
        if going_to_rest:
            # self.timer_mode = "rest"
            print("Going to rest!")
            self.timerText.fg = "#4F799F"
            self.start_timer(10)
        else:
            # self.timer_mode = "work"
            print("Going to work!")
            self.timerText.fg = "#ef5959"
            self.start_timer(10)

    def on_enter(self, event):
        print("Enter key pressed!")
        print(self.search_bar.get())
        enter_value = self.search_bar.get().strip().lower()

        current_whitelist = {}
        print(
            f"Singleton's current whitelist {self.parent.singleton.get_user_data()}"
        )
        if "whitelist" in self.parent.singleton.get_user_data():
            current_whitelist = self.parent.singleton.get_user_data(
            )["whitelist"]
        print(f"Here is the whitelist before adding: {current_whitelist}")

        if enter_value in self.parent.singleton.valid_program_names:
            # assume user is blocking a program
            if "programs" in current_whitelist:
                current_whitelist["programs"].append(enter_value)
            else:
                current_whitelist["programs"] = [enter_value]
        elif self.parent.singleton.check_if_website(enter_value):
            # assume website
            if "websites" in current_whitelist:
                current_whitelist["websites"].append(enter_value)
            else:
                current_whitelist["websites"] = [enter_value]
        else:
            print("Invalid whitelist entry!")
            return False

        if "merged" in current_whitelist:
            current_whitelist["merged"].append(enter_value)
        else:
            current_whitelist["merged"] = [enter_value]

        self.parent.db.child("users").child(
            self.parent.uid).child("whitelist").set(current_whitelist)
        print(f"Here is what we are adding to the db now: {current_whitelist}")
        return True

    def delete_whitelist_entry(self, entry_name):
        current_whitelist = {}
        print(f"Attempting to delete {entry_name} from whitelist")
        if "whitelist" in self.parent.singleton.get_user_data():
            current_whitelist = self.parent.singleton.get_user_data(
            )["whitelist"]
        print(f"Here is the whitelist before deleting: {current_whitelist}")
        current_whitelist["merged"].remove(entry_name)

        if self.parent.singleton.check_if_website(entry_name):
            current_whitelist["websites"].remove(entry_name)
        else:
            current_whitelist["programs"].remove(entry_name)

        print(f"Here is the whitelist after deleting: {current_whitelist}")
        self.parent.db.child("users").child(
            self.parent.uid).child("whitelist").set(current_whitelist)

    def update_slider(self, slider, value):
        slider.set(value)

    def clear_category_buttons(self):
        # print("Attempting refresh of homepage...")
        # for widget in self.winfo_children():
        #     if isinstance(widget, tk.Frame) and widget != self.navbar_frame:
        #         widget.destroy()
        for widget in self.category_frame.winfo_children():
            widget.destroy()

    def update_with_new_data(self, data):
        print("Updating focus screen with new data...")
        merged_list = []
        if "whitelist" in self.parent.singleton.get_user_data(
        ) and "merged" in self.parent.singleton.get_user_data()["whitelist"]:
            merged_list = self.parent.singleton.get_user_data(
            )["whitelist"]["merged"]

        rest_slider_val = self.parent.singleton.get_user_data(
        )["settings"]["pomodoro_rest_slider_val"]
        work_slider_val = self.parent.singleton.get_user_data(
        )["settings"]["pomodoro_work_slider_val"]

        print(f"REST: {rest_slider_val} WORK: {work_slider_val}")

        # Update sliders and text labels within the timer_and_controls_frame
        self.update_slider(self.workSlider, work_slider_val)
        self.update_slider(self.restSlider, rest_slider_val)

        # print(type(work_slider_val))
        # print(type(rest_slider_val))

        self.workText.configure(text=f"Work: {int(work_slider_val)} minutes")
        self.restText.configure(text=f"Rest: {int(rest_slider_val)} minutes")

        # Clear and recreate category buttons
        # self.clear_category_buttons()
        # self.create_category_buttons(include_search=True, elements=merged_list)
        self.clear_whitelist()
        self.create_whitelist(self.whitelist_frame, elements=merged_list)

        # Update the timer display
        timer_amount = self.format_timer(self.parent.singleton.timer_seconds_remaining)
        self.timerText.configure(text=timer_amount)
