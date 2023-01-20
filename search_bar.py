from PyQt5.QtWidgets import QLineEdit, QCompleter, QApplication, QDesktopWidget, QTextEdit, QLabel, QMessageBox
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap, QTextCursor, QFont

import fonts
import random


class SlashMenu(QLineEdit):
    def __init__(self, text_edit: QTextEdit):
        super().__init__()
        self.options = ["/", "slash (no parameters)",
                        "\\", "backslash", "b", "bold", "lorem", "i", "itallic"]
        self.text_edit = text_edit
        self.initUI()

        self.width_in_css = 1000

    def initUI(self):
        # Remove close, minimize and fullscreen options
        self.setWindowFlags(Qt.Dialog | Qt.FramelessWindowHint)

        # Make the search bar non-resizable
        screen = QDesktopWidget().screenGeometry()

        # Create a QCompleter
        self.completer = QCompleter(self.options)
        self.completer.setCompletionMode(QCompleter.UnfilteredPopupCompletion)
        self.setCompleter(self.completer)

        # Remove the window name
        self.setWindowTitle("")
        self.setPlaceholderText("Start typing to see options...")

        self.setObjectName("slash_menu")

        self.icon_label = QLabel(self)
        self.icon_label.setPixmap(QPixmap("icons/slash_light.png"))
        self.icon_label.setScaledContents(True)
        self.icon_label.setFixedSize(35, 35)
        self.icon_label.move(7, 7)

    def focusOutEvent(self, event):
        self.close()
        self.completer.popup().close()
        super().focusOutEvent(event)
        cursor = self.text_edit.textCursor()
        cursor.insertText("/")

    def show(self):
        # clear last input
        self.setText("")

        text_widget_geometry = self.text_edit.geometry()
        x = int(text_widget_geometry.x() +
                (text_widget_geometry.width()) - self.width_in_css // 2)
        y = int(text_widget_geometry.y() +
                (text_widget_geometry.height()) - self.height() // 2 - 90)
        self.move(x, y)

        super().show()
        self.activateWindow()

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Escape:
            self.completer.popup().close()
            self.close()
            self.processOption("")
        elif event.key() == Qt.Key_Return or event.key() == Qt.Key_Tab:
            print(f"Searched: \"{self.text()}\"")
            self.completer.popup().close()
            self.close()
            self.processOption(self.text())
        else:
            super().keyPressEvent(event)

    def optionError(self, title, text, info):
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Warning)
        msg.setWindowTitle(title)
        msg.setText(text)
        msg.setInformativeText(info)
        msg.exec_()

    def processOption(self, text: str):
        if " " in text:
            command, parameter = text.split(" ", 1)
        else:
            command = text
            parameter = ""

        match command:
            case "" | "slash" | "/":
                cursor = self.text_edit.textCursor()
                cursor.insertText("/")

            case "\\" | "backslash":
                cursor = self.text_edit.textCursor()
                cursor.insertText("\\")

            case "b" | "bold":
                if parameter and parameter != "":
                    cursor = self.text_edit.textCursor()
                    char_format = cursor.charFormat()
                    char_format.setFontWeight(QFont.Bold)
                    cursor.insertText(parameter, char_format)
                else:
                    fonts.make_text_bold(self.text_edit)

            case "i" | "itallic":
                cursor = self.text_edit.textCursor()
                if parameter and parameter != "":
                    char_format = cursor.charFormat()
                    char_format.setFontItalic(True)
                    cursor.insertText(parameter, char_format)
                else:
                    if cursor.anchor() != cursor.position():
                        fonts.make_text_italic(self.text_edit)

            case "lorem":

                if not parameter:
                    num_words = 15
                else:
                    if parameter.isdigit():
                        num_words = int(parameter)
                    else:
                        num_words = 15

                # Check if parameters are legal
                if num_words < 1 or num_words > 1000:
                    print("illegal parameters")
                    return False

                lorem_ipsum = "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Sed euismod, nisi in hendrerit iaculis, nibh dolor viverra ligula, eget euismod magna augue id nulla. Curabitur viverra pharetra bibendum. Fusce dapibus, augue at egestas iaculis, elit massa condimentum erat, non auctor elit mauris non augue. Sed euismod, nisi in hendrerit iaculis, nibh dolor viverra ligula, eget euismod magna augue id nulla."
                words = lorem_ipsum.split(" ")

                if num_words > 5:
                    selected_words = ["Lorem", "ipsum", "dolor", "sit",
                                      "amet,"] + random.choices(words, k=num_words - 5)
                else:
                    selected_words = ["Lorem", "ipsum", "dolor", "sit",
                                      "amet,"]
                    selected_words = selected_words[:num_words]

                generated = " ".join(selected_words)

                cursor = self.text_edit.textCursor()
                cursor.insertText(generated)

            
            
            case other:
                print(f"selected invalid option: {text}")
                cursor = self.text_edit.textCursor()
                cursor.insertText(text)
