import tkinter as tk
from tkinter import ttk

root = tk.Tk()  # create first screen
msg = tk.Label(root, text = "Hello world")  # display text on root screen
msg.pack()  # puts in the msg on the screen
root.title("screen1")  # change the title of the root window
root.geometry(
    "1000x800+400+200")  # change the dimensions of the root screen (width x height + xstartingfromleft + ystartingfromtop)
root.resizable(True, True)  # resize the window (width, length)
root.minsize(200, 200)  # set the minimum window size
root.maxsize(1200, 1200)  # set the maximum window size


# root.attributes("-alpha", 0.9)  # set how transparent the window is


def buttonPress(event):
    print("button")


button = ttk.Button(root, text = "press", command = buttonPress)  # create button on root screen
button.pack()

button.bind("<Return>", buttonPress)  # binds the return the button to function "buttonPress"



root.mainloop()  # loop the root screen and update it
