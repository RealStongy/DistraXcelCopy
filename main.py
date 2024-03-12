from app import App
import customtkinter as ctk
# import atexit

# def exit_handler():
#     print("Testing DistraXcel")

# atexit.register(exit_handler)


def main():
    try:
        ctk.set_appearance_mode("Light")
        # ctl.set_default_color_theme("")
        app = App()
        app.mainloop()
    finally:
        print("BBBBYYYYYYEEEEEEEE")


if __name__ == "__main__":
    main()
