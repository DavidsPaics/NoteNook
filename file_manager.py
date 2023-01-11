import os
from PyQt5.QtCore import QSize, Qt
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QListWidgetItem, QListWidget, QTextEdit, QFileDialog, QMessageBox
from pathlib import Path
import utils

ignoreChanges = False


class fileListItem(QListWidgetItem):
    def __init__(self, parent: QListWidgetItem, text_edit: QTextEdit, savable=True, editable=True):
        global open_files

        self.currentHtml = ""

        self.path = None
        self.file_name = "Untitled"
        self.savable = savable

        self.text_edit = text_edit
        self._editable = editable

        self.parent = parent

        if editable:
            self.text_edit.setReadOnly(False)
            self.text_edit.setTextInteractionFlags(
                Qt.TextSelectableByMouse | Qt.TextSelectableByKeyboard | Qt.TextEditorInteraction)
        else:
            self.text_edit.setReadOnly(True)

        icon = QIcon("./icons/file_icon.svg")
        super().__init__(icon, self.file_name, parent)
        super().setSizeHint(QSize(32, 32))
        self._unsaved = False

    def makeUnsaved(self):
        self._unsaved = True
        super().setText(self.file_name + "*")

    def makeSaved(self):
        self._unsaved = False
        super().setText(self.file_name)

    def getNameAndStar(self):
        return "*" + self.file_name if self._unsaved else self.file_name

    def openNewFile(self):
        global ignoreChanges
        print("Created new file")
        ignoreChanges = True

        self.text_edit.setReadOnly(False)
        self.text_edit.setTextInteractionFlags(
            Qt.TextSelectableByMouse | Qt.TextSelectableByKeyboard)

        self.text_edit.setText("")

        self.currentHtml = self.text_edit.toHtml()
        self.activate()

        return True

    def open(self, path=None):
        global active
        global ignoreChanges
        ignoreChanges = True

        if not path:
            path, _ = QFileDialog.getOpenFileName(self.text_edit, "Open File", os.path.expanduser(
                "~/Documents/"), "All Supported File Formats - .html .txt .md .markdown(*.html *.txt *.md *.markdown)")
            if not path:
                print("No file selected")
                return False

        self.path = path
        with open(self.path, 'r') as f:
            data = f.read()

        self.file_name = Path(self.path).stem
        super().setText(self.file_name)

        extension = self.path.split(".")[-1]

        if extension == "html":
            self.text_edit.setHtml(data)
            print(f"opened file {self.file_name}.{extension} as html")
        elif extension == "md" or extension == "markdown":
            print(f"opened file {self.file_name}.{extension} as markdown")
            self.text_edit.setMarkdown(data)
        elif extension == "txt":
            print(f"opened file {self.file_name}.{extension} as plain text")
            self.text_edit.setText(data)

        if not self._editable:
            print("Opened file is read only")
        if not self.savable:
            print("Opened file can't be saved by the user")

        self.currentHtml = self.text_edit.toHtml()
        ignoreChanges = False
        self.activate()

        return True

    def save(self):
        if not self.savable:
            msg = QMessageBox()
            msg.setText(
                "This file cannot be saved")
            msg.setWindowTitle("Can't save")
            msg.setStandardButtons(QMessageBox.Ok)
            msg.exec_()
            return

        filepath, _ = QFileDialog.getSaveFileName(self.text_edit, "Save File", os.path.expanduser(
            f"~/Documents/{self.file_name}.html"), "All Supported File Formats - .html .txt .md .markdown(*.html *.txt *.md *.markdown)")
        if not filepath:
            print("No file selected")
            return

        extension = filepath.split(".")[-1]
        print(f"extension: {extension}")

        if extension == "txt":
            # Display warning message
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Warning)
            msg.setText(
                "Saving to a .txt file will remove all formatting. Are you sure you want to continue?")
            msg.setWindowTitle("Warning")
            msg.setStandardButtons(QMessageBox.Cancel | QMessageBox.Ok)

            # Get user response
            response = msg.exec_()

            if response == QMessageBox.Cancel:
                # User clicked cancel, return from function
                print("Canceled save to .txt file")
                return
            elif response == QMessageBox.Ok:
                data = self.text_edit.toPlainText()
                print("saved as text")

        elif extension == "html":
            data = self.text_edit.toHtml()
            print("saved as html")
        elif extension == "md" or extension == "markdown":
            data = self.text_edit.toMarkdown()
            print("saved as markdown")
        else:
            print(f"Unsuported extension: \"{extension}\"")
            return

        with open(filepath, 'w') as f:
            f.write(data)

        self.path = filepath
        self.file_name = Path(self.path).stem
        self.makeSaved()

    def deactivate(self):
        global ignoreChanges
        global active
        ignoreChanges = True

        active = None
        self.text_edit.setText("")
        self.text_edit.setReadOnly(True)
        ignoreChanges = False

    def activate(self):
        global ignoreChanges
        global active

        ignoreChanges = True

        if "active" in globals() and active is not None:
            active.deactivate()
            ignoreChanges = True

        self.setSelected(True)

        active = self
        self.text_edit.setHtml(self.currentHtml)

        ignoreChanges = False


active: fileListItem
