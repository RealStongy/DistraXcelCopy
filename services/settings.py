import tkinter as tk
import keyring

def show_settings(parent):
    if (parent.parent.settings_open):
        print("Settings already opened!")
        return

    parent.parent.settings_open = True
    # Create a new top-level window for settings
    parent.settings_window = tk.Toplevel(parent)
    parent.settings_window.title("Settings")
    parent.settings_window.geometry("300x200")  # Adjust size as needed

    # Add widgets to the settings window here
    # For example: tk.Label(self.settings_window, text="Settings Panel").pack()
    parent.settings_window.protocol("WM_DELETE_WINDOW",
                                    lambda: close_settings(parent))

    # Add a dismiss button
    dismiss_btn = tk.Button(parent.settings_window,
                            text="Logout",
                            command=lambda: logout(parent))
    dismiss_btn.pack()
    dismiss_btn = tk.Button(parent.settings_window,
                            text="Quit",
                            command=lambda: quit_app(parent))
    dismiss_btn.pack()


def close_settings(parent):
    parent.parent.settings_open = False
    parent.settings_window.destroy()


def logout(parent):
    try:
        keyring.delete_password("DistraXcel", "user_id_token")
        keyring.delete_password("DistraXcel", "user_refresh_token")
    except:
        print("No keyring to delete")
    parent.uid = ""
    parent.parent.returnToLogin()
    close_settings(parent)


def quit_app(parent):
    # parent.parent.quit()
    parent.parent.destroy()
