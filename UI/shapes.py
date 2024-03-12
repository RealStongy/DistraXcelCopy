from tkinter import *

def create_rounded_entry(parent, width, height, radius, **kwargs):
    canvas = Canvas(parent, width=width, height=height, highlightthickness=0, bg='#d9d9d9')

    # Draw a rounded rectangle
    round_rectangle(canvas, 2, 2, width-2, height-2, radius=radius, fill='white')

    # Create an entry widget
    entry = Entry(canvas, **kwargs)
    entry_window = canvas.create_window(4, 4, anchor='nw', window=entry, width=width-8, height=height-8)

    return canvas, entry  # Return both canvas and entry

def round_rectangle(canvas, x1, y1, x2, y2, radius=25, **kwargs):
        
    points = [x1+radius, y1,
              x1+radius, y1,
              x2-radius, y1,
              x2-radius, y1,
              x2, y1,
              x2, y1+radius,
              x2, y1+radius,
              x2, y2-radius,
              x2, y2-radius,
              x2, y2,
              x2-radius, y2,
              x2-radius, y2,
              x1+radius, y2,
              x1+radius, y2,
              x1, y2,
              x1, y2-radius,
              x1, y2-radius,
              x1, y1+radius,
              x1, y1+radius,
              x1, y1]

    return canvas.create_polygon(points, **kwargs, smooth=True)