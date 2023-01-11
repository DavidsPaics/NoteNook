import traceback
from PyQt5.QtWidgets import QMessageBox


def show_exception_popup(exception: Exception):
    msg = QMessageBox()
    msg.setWindowTitle("Ooops...")
    msg.setText(f"An error occured :(")
    msg.setInformativeText(str(exception))
    msg.setDetailedText(traceback.format_exc())
    msg.exec_()


def show_custom_exception_popup(title: str, text: str, info: str):
    msg = QMessageBox()
    msg.setWindowTitle(title)
    msg.setText(text)
    msg.setInformativeText(info)
    msg.exec_()


