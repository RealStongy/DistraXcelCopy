import tkinter as tk
# from tkinter import ttk

class ToggleSwitch(tk.Canvas):
    def __init__(self, parent, default_state=False, callback=None, *args, **kwargs):
        tk.Canvas.__init__(self, parent, width=54, height=29, *args, **kwargs)
        self.configure(bg="#BBBBBB", bd=0, highlightthickness=0)
        self.toggle_state = False
        self.callback = callback
        # self.oval1 = self.create_oval(24, 24, 52, 52, fill="red")
        self.background1 = self.create_oval(2, 2, 28, 28, fill="gray", outline="")
        self.background2 = self.create_oval(26, 2, 52, 28, fill="gray", outline="")
        self.background3 = self.create_rectangle(15, 2, 39, 28, fill="gray", outline="")
        self.switch = self.create_oval(4, 4, 26.5, 26.5, fill="white", outline="")
        if default_state:
            self.toggle(run_callback=False)

        # self.create_rounded_rect(0,0,50,25,radius=5,fill="gray")
        # self.switch.pack(pady=50)
        self.bind("<Button-1>", self.toggle)

    def toggle(self, event=None, run_callback=True):
        if self.toggle_state:
            # self.configure(bg="gray")
            self.move(self.switch, -24, 0)
            new_color = "gray"
            # self.create_oval(2, 2, 28, 28, fill="red")
        else:
            # self.configure(bg="green")
            self.move(self.switch, 24, 0)
            new_color = "#8DEE7D"
            
        self.itemconfig(self.background1, fill=new_color)
        self.itemconfig(self.background2, fill=new_color)
        self.itemconfig(self.background3, fill=new_color)
        self.toggle_state = not self.toggle_state

        if self.callback and run_callback:
            self.callback()
