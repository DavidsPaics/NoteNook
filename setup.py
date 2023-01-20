# This file should not be run by the user, Instead follow the instructions in README.md and NoteNook will run setup automatically.

import os
from PyQt5.QtWidgets import QMainWindow, QApplication
import utils


def install_if_needed():
    if not os.path.exists(os.path.expanduser("~/.NoteNook")):
        print("creating ~/.NoteNook")
        os.makedirs(os.path.expanduser("~/.NoteNook/themes"))
        with open(os.path.expanduser("~/.NoteNook/themes/info.txt"), 'w') as f:
            f.write(
                "Place a qss file in this folder and enter the file name and ONLY the file name in the first line of selected.txt (if the file is coolTheme.qss, type coolTheme in selected.txt) then restart NoteNook to apply a custom theme")

        with open(os.path.expanduser("~/.NoteNook/themes/selected.txt"), 'w') as f:
            f.write(
                "default_dark")


def load_theme(app: QApplication):

    with open(os.path.expanduser("~/.NoteNook/themes/selected.txt")) as f:
        file_name = f.read()

    if not os.path.exists(os.path.expanduser(f"~/.NoteNook/themes/{file_name}.qss")):
        utils.show_custom_exception_popup("Warning", "Failed to load selected theme",
                                          f"check if {file_name}.qss exists. Press OK to continue. (The UI Will most likely be broken)")
        return False

    try:
        with open(os.path.expanduser(f"~/.NoteNook/themes/{file_name}.qss"), 'r') as f:
            user_theme = f.read()

        if user_theme:
            app.setStyleSheet(user_theme)
            print(f"loaded {file_name}.qss")
        else:
            print("WARNING: Custom theme.qss is blank")

    except Exception as e:
        print(e)
        utils.show_custom_exception_popup("Warning", "Failed to load theme",
                                          f"check if the {file_name}.qss file is acessible and not used by another program. Press OK to continue.")
        return False

    return True
