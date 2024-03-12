import tkinter as tk
from PIL import Image, ImageTk
import os
"""
KNOWN ISSUES:
Max value calulation is fine, but the min value can often be off by a few minutes
The issue is probably due to how segments are calculated as the handle sometimes snaps
in the wrong place
"""


class PomodoroSlider(tk.Canvas):

    def __init__(self,
                 parent,
                 min_val=0,
                 max_val=100,
                 current_val=50,
                 slider_height=10,
                 fill_color="#59B0EF",
                 divider_color="#000000",
                 database_path="",
                 on_value_changed_callback=None,
                 **kwargs):
        super().__init__(parent, **kwargs)
        self.min_val = min_val
        self.max_val = max_val
        self.value = current_val
        self.padding = 40
        self.current_x = (self.value // max_val) * self.winfo_width()
        self.slider_height = slider_height
        self.fill_color = fill_color
        self.divider_color = divider_color
        self.database_path = database_path
        self.on_value_changed_callback = on_value_changed_callback

        script_dir = os.path.dirname(os.path.abspath(__file__))
        handle_path = os.path.join(script_dir, "handle.png")
        self.handle_image_origin = Image.open(handle_path)
        # self.handle_image_origin = Image.open(open("handle.png", "rb"))
        self.handle_image = ImageTk.PhotoImage(self.handle_image_origin)

        self.segment_count = 10

        self.after(100, self.draw_slider)
        # self.draw_slider()
        self.bind("<ButtonPress-1>", self.on_click)
        self.bind("<B1-Motion>", self.on_drag)

    def draw_slider(self):
        self.delete("all")
        self.current_x = (self.value // self.max_val) * self.winfo_width()
        line_y = self.slider_height // 2
        padding = 40
        min_label_x = self.padding
        max_label_x = self.winfo_width() - self.padding
        label_y = self.winfo_height() // 2
        self.create_line(self.padding,
                         self.winfo_height() // 2,
                         self.winfo_width() - self.padding,
                         self.winfo_height() // 2,
                         fill=self.fill_color,
                         width=10)

        # draw labels
        self.create_text(
            min_label_x,
            label_y,
            text=f"{self.minutes_to_string(self.min_val, digital=True)}")
        # minLabel = tk.Label(self, text = "10 min", font = ("Arial", 15), fg = "#858585")
        # minLabel.grid(row=1, column=0, sticky="e")

        # maxLabel = tk.Label(self, text = "2 hours", font = ("Arial", 15), fg = "#858585")
        # maxLabel.grid(row=1, column=2, sticky="w")

        # draw segmentation lines
        for i in range(self.segment_count + 1):
            x = self.padding + i * (self.winfo_width() -
                                    2 * self.padding) / self.segment_count
            self.create_line(x,
                             self.winfo_height() // 2 - 4.5,
                             x,
                             self.winfo_height() // 2 + 5,
                             width=2,
                             fill=self.divider_color)

        # Draw shadow
        handle_radius = 10
        initial_x = self.padding + (self.value - self.min_val) * (
            self.winfo_width() - 2 * self.padding) / (self.max_val -
                                                      self.min_val)
        initial_x = self.padding + (self.value - self.min_val) / (
            self.max_val - self.min_val) * (self.winfo_width() -
                                            2 * self.padding)
        # shadow_offset = 3
        # self.shadow = self.create_oval(initial_x - handle_radius + shadow_offset,
        #                                 line_y - handle_radius + shadow_offset,
        #                                 initial_x + handle_radius + shadow_offset,
        #                                 line_y + handle_radius + shadow_offset, fill="gray", outline="")

        # Draw the handle

        # self.handle = self.create_oval(initial_x - handle_radius,
        #                                 line_y - handle_radius,
        #                                 initial_x + handle_radius,
        #                                 line_y + handle_radius, fill="white", outline="")

        self.handle = self.create_image(initial_x,
                                        line_y,
                                        image=self.handle_image)
        self.height_diff = 30
        self.handle_label = self.create_text(initial_x,
                                             line_y - self.height_diff,
                                             text=str(self.value),
                                             fill="black")

        # self.coords(self.handle, initial_x - 10, self.winfo_height()//2 - 10, initial_x + 10, self.winfo_height()//2 + 10)
        self.coords(self.handle, initial_x, self.winfo_height() // 2)
        # self.coords(self.handle, 10, self.winfo_height()//2 - 10, 10, self.winfo_height()//2 + 10)

    def on_click(self, event):
        self.update_handle(event.x)

    def on_drag(self, event):
        self.update_handle(event.x)

    def update_handle(self, x):
        padding = 20
        # handle_radius = 10
        # x = max(padding + handle_radius, min(x, self.winfo_width() - padding - handle_radius))
        x = max(self.padding, min(x, self.winfo_width() - self.padding))
        # line_y = self.slider_height // 2
        # self.create_line(10, line_y, self.winfo_width() - 10, line_y, fill="blue", width=15)

        # get nearest segment position
        nearest_segment = None
        min_distance = float("inf")
        for i in range(self.segment_count + 1):
            segment = i * (self.winfo_width() -
                           self.padding) / self.segment_count
            distance = abs(x - segment)
            if distance < min_distance:
                min_distance = distance
                nearest_segment = segment

        snap_threshold = 10

        if min_distance <= snap_threshold:
            x = nearest_segment

        # self.coords(self.handle, x - 10, self.winfo_height()//2 - 10, x + 10, self.winfo_height()//2 + 10)
        self.coords(self.handle, x, self.winfo_height() // 2)
        self.coords(self.handle_label, x,
                    self.winfo_height() // 2 - self.height_diff)
        self.itemconfig(self.handle_label,
                        text=self.minutes_to_string(self.value, digital=True))

        self.value = self.min_val + (self.max_val - self.min_val) * (
            x - (self.padding)) / (self.winfo_width() - self.padding)
        self.value = self.min_val + (self.max_val - self.min_val) * (
            x - self.padding) / (self.winfo_width() - 2 * self.padding)
        # print("value changed to ", self.value)

        self.value = int(self.value)

        if self.on_value_changed_callback:
            self.on_value_changed_callback(path=self.database_path,
                                           value=self.value)

    def minutes_to_string(self, value, shorten=False, digital=False):
        hours = int(value // 60)
        minutes = int(value % 60)

        if (digital):
            return f"{hours:02}:{minutes:02}:00"
        else:
            if (hours > 0 and minutes > 0):
                return f"{hours} {'hour' if hours > 0 else ''} {'s' if hours > 1 else ''} {minutes} minute{'s' if minutes > 1 else ''}"
            elif (hours > 0 and minutes == 0):
                return f"{hours} {'hour' if hours > 0 else ''} {'s' if hours > 1 else ''}"
            else:
                return f"{minutes} min{'s' if minutes > 1 else ''}"
