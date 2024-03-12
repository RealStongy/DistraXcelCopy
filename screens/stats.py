"""
1. logout

2. *enable parental feature

3. auto block based on time
-pomodoro
-option to change time intervals from pomo default

4. Stats Summary (stored in database)
-time spent focused on X
-amount of times triggered
-*time saved

"""

import tkinter as tk
from services.size import *
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
import numpy as np
from tkmacosx import Button
import services.settings as settings
import customtkinter as ctk
import sys

class ScrollableStatFrame(ctk.CTkScrollableFrame):
    def __init__(self, parent, **kwargs):
        super().__init__(parent, **kwargs)
        self.grid_columnconfigure(0, weight=1)

        self.entry_list = []

    def format_name(self, name):
        name = name.replace("_", " ")
        return name

    def add_item(self, item, icon=None):
        label = ctk.CTkLabel(self, text=self.format_name(item), image=icon, compound="left", padx=5, anchor="w")
        label.grid(row=len(self.entry_list), column=0, pady=(0, 10), sticky="w")
        self.entry_list.append(label)

    def remove_item(self, item):
        for label in self.entry_list:
            if item == label.cget("text"):
                label.destroy()
                self.entry_list.remove(label)
                return


class StatsScreen(ctk.CTkFrame):

    def __init__(self, parent, bg_color="#000000"):
        super().__init__(parent)
        self.parent = parent
        if sys.platform == "darwin":
            print("We are running in Mac OS")
            btn_font = ("Arial", 20)
            entry_height = 65
        else:
            print("We are running in Windows")
            btn_font = ("Arial", 24)
            entry_height = 75

        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=0)
        self.grid_rowconfigure(1, weight=1)

        toggleFrame = tk.Frame(self)
        toggleFrame.grid(column=0, row=0, sticky=tk.NW)

        # stat_frame = tk.Frame(self,
        #                       bg="#000000",
        #                       width=percent(0.5),
        #                       height=percent(height=0.75),
        #                       padx=10,
        #                       pady=10)
        # category_frame = tk.Frame(stat_frame,
        #                           bg="#5C5C5C",
        #                           width=percent(width=0.15),
        #                           height=percent(height=0.65),
        #                           padx=10,
        #                           pady=10)
        # program_frame = tk.Frame(stat_frame,
        #                          bg="#ececec",
        #                          width=percent(width=0.15),
        #                          height=percent(height=0.65),
        #                          padx=10,
        #                          pady=10)

        # category_frame.grid(column=0, row=1)
        # program_frame.grid(column=1, row=1)
        # stat_frame.grid(row=1, column=0)


        self.scrollable_category_frame = ScrollableStatFrame(parent=self, width=100,)
        self.scrollable_category_frame.grid(row=1, column=0, padx=0, pady=0, sticky="nsew")
        for i in range(20):
            self.scrollable_category_frame.add_item(f"TESTING: {i}")

        self.scrollable_program_frame = ScrollableStatFrame(parent=self, width=100,)
        self.scrollable_program_frame.grid(row=1, column=1, padx=0, pady=0, sticky="nsew")
        for i in range(20):
            self.scrollable_program_frame.add_item(f"TESTING: {i}")


        fig = Figure(figsize=(4.5, 4.5))
        ax = fig.add_subplot()

        size = 0.3
        vals = np.array([[60., 32.], [37., 40.], [29., 10.]])

        cmap = plt.colormaps["tab20c"]
        outer_colors = cmap(np.arange(3) * 4)
        inner_colors = cmap([1, 2, 5, 6, 9, 10])

        ax.pie(vals.sum(axis=1),
               radius=1,
               colors=outer_colors,
               wedgeprops=dict(width=size, edgecolor='w'))

        ax.pie(vals.flatten(),
               radius=1 - size,
               colors=inner_colors,
               wedgeprops=dict(width=size, edgecolor='w'))

        ax.set(aspect="equal", title='Pie plot with `ax.pie`')
        # plt.show()

        fig_canvas = FigureCanvasTkAgg(fig, master=self)
        fig_canvas.draw()
        fig_canvas.get_tk_widget().grid(row=1, column=2)

        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(2, weight=1)
        self.grid_rowconfigure(3, weight=0)

        # Navbar frame setup
        self.navbar_frame = tk.Frame(self, bg="#656565")
        self.navbar_frame.grid(column=0, row=3, sticky="ew", columnspan=3)
        self.navbar_frame.grid_columnconfigure(0, weight=1)
        self.navbar_frame.grid_columnconfigure(1, weight=1)
        self.navbar_frame.grid_columnconfigure(2, weight=1)
        self.navbar_frame.grid_columnconfigure(3, weight=1)
        # self.navbar_frame.grid_columnconfigure(4, weight=1)
        self.parent = parent

        # Create buttons within the navbar
        # btn_font = ("Arial", 24)
        # btn_bg_color = "#656565"
        # btn_fg_color = "#ffffff"
        # btn_active_bg_color = "#656565"
        # btn_active_fg_color = "#ffffff"
        # btn1 = tk.Button(self.navbar_frame, width=20, height=2, font=btn_font, text="Focus", bg=btn_bg_color, fg=btn_fg_color, activebackground=btn_active_bg_color, activeforeground=btn_active_fg_color, command=parent.focus_button)
        # btn1.grid(row=0, column=1)
        # btn2 = tk.Button(self.navbar_frame, width=20, height=2, font=btn_font, text="Home", bg=btn_bg_color, fg=btn_fg_color, activebackground=btn_active_bg_color, activeforeground=btn_active_fg_color, command = parent.home_button)
        # btn2.grid(row=0, column=2)
        # btn3 = tk.Button(self.navbar_frame, width=20, height=2, font=btn_font, text="Stats", bg=btn_bg_color, fg=btn_fg_color, activebackground=btn_active_bg_color, activeforeground=btn_active_fg_color)
        # btn3.grid(row=0, column=3)
        # setting_btn = tk.Button(self.navbar_frame, width = 5, height = 2, font = btn_font, text = "", bg=btn_bg_color, fg=btn_fg_color, activebackground=btn_active_bg_color, activeforeground=btn_active_fg_color, command=lambda: settings.show_settings(self))
        # setting_btn.grid(row=0, column=4)

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
                              command=lambda: settings.show_settings(self))
        settings_btn.grid(row=0, column=3, sticky="nsew")
