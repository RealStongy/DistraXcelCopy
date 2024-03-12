# from tkinter import Tk

SCREEN_WIDTH = 960
SCREEN_HEIGHT = 560

# Get screen width and height
# screen_width = Tk().winfo_screenwidth()
# screen_height = Tk().winfo_screenheight()

# Calculate percentage of screen width/height
# SCREEN_WIDTH = int(screen_width * 0.5)
# SCREEN_HEIGHT = int(screen_height * 0.5)


def percent(width=-1, height=-1):
    # print(f"1. width: {SCREEN_WIDTH}, height: {SCREEN_HEIGHT}")
    if width != -1:
        return int(SCREEN_WIDTH * width)
    elif height != -1:
        return int(SCREEN_HEIGHT * height)
    return 0


def tk_units(value, dimension="width", unit="px"):
    if dimension == "width":
        pixel_val = percent(width=value)
    elif dimension == "height":
        pixel_val = percent(height=value)
    else:
        raise ValueError("Invalid dimension, use 'height' or 'width'")

    # TODO investigate conversions
    if unit == "px":
        return pixel_val
    elif unit == 'i':
        pass
    elif unit == 'pt':
        pass
    elif unit == 'mm':
        pass
    elif unit == 'c':
        pass
