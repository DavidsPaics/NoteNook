import os
import pathlib
import sys
from PyQt5 import QtCore
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QTextCursor, QTextCharFormat, QKeySequence, QFont, QIcon
from PyQt5.QtWidgets import QApplication, QMainWindow, QTextEdit, QListWidget, QDockWidget, QMenuBar, QMenu, QAction, QMessageBox, QListWidgetItem, QAbstractItemView
from utils import show_exception_popup, show_custom_exception_popup
import fonts
import file_manager


def createMenuAction(text: str, parent, function, shortcut=None, autoRepeat=False):
    action = QAction(text, parent)
    action.triggered.connect(function)
    action.setAutoRepeat(autoRepeat)
    if shortcut:
        action.setShortcut(QKeySequence(shortcut))
    return action


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        # Set the window title
        self.setWindowTitle('NoteNook')
        self.setWindowIcon(QIcon("./icons/NoteNookIcon.png"))

        # Create a QTextEdit widget and set it as the central widget
        self.text_edit = QTextEdit()
        self.text_edit.setObjectName("note_text_field")
        self.text_edit.textChanged.connect(
            lambda: self.textChanged(self.text_edit.toPlainText()))
        self.setCentralWidget(self.text_edit)

        # Create a QListWidget for the sidebar and add it to a QDockWidget
        self.sidebar = QListWidget()
        self.dock = QDockWidget("My Notes:")
        self.dock.setWidget(self.sidebar)
        self.dock.setFeatures(QDockWidget.NoDockWidgetFeatures)
        self.addDockWidget(Qt.LeftDockWidgetArea, self.dock)

        self.sidebar.itemClicked.connect(lambda item: item.activate())
        self.sidebar.setSelectionMode(QAbstractItemView.SingleSelection)

        self.menuBar()

        self.openNewFile("./Getting Started.html",
                         savable=False, editable=False)

    def menuBar(self):
        # Create a QMenuBar
        self.menu_bar = QMenuBar()
        self.setMenuBar(self.menu_bar)

        # Create the "File" menu
        self.file_menu = QMenu('File')
        self.menu_bar.addMenu(self.file_menu)

        self.file_menu.addAction(createMenuAction(
            'New File', self, self.createNewFile, "Ctrl+N"))

        self.file_menu.addAction(createMenuAction(
            'Open', self, self.openNewFile, "Ctrl+O"))

        self.file_menu.addAction(createMenuAction(
            'Save', self, self.saveOpenFile, "Ctrl+S"))

        self.file_menu.addSeparator()

        self.file_menu.addAction(createMenuAction(
            'Quit', self, quit_app))
        # Create the "Edit" menu
        self.edit_menu = QMenu('Edit')
        self.menu_bar.addMenu(self.edit_menu)

        # Create the "Format" menu
        self.format_menu = QMenu('Format')
        self.edit_menu.addMenu(self.format_menu)

        # Create the "Bold" action
        self.format_menu.addAction(createMenuAction(
            'Bold', self, lambda: fonts.make_text_bold(self.text_edit), "Ctrl+B"))

        # Create the "Italic" action
        self.format_menu.addAction(createMenuAction(
            'Italic', self, lambda: fonts.make_text_italic(self.text_edit), "Ctrl+I"))

        # Create the "View" menu
        self.view_menu = QMenu('View')
        self.menu_bar.addMenu(self.view_menu)

        # Create the "Tools" menu
        self.tools_menu = QMenu('Tools')
        self.menu_bar.addMenu(self.tools_menu)

        # Create the "Help" menu
        self.help_menu = QMenu('Help')
        self.menu_bar.addMenu(self.help_menu)

    def createNewFile(self):
        file = file_manager.fileListItem(
            self.sidebar, self.text_edit, savable=True, editable=True)
        file.openNewFile()
        self.setWindowTitle(f'{file.getNameAndStar()} - NoteNook')

    def slashMenu(self, text: str):
        pass

    def openNewFile(self, path=None, savable=True, editable=True):
        file = file_manager.fileListItem(
            self.sidebar, self.text_edit, savable=savable, editable=editable)
        file.ignoreChanges = True
        if path != None:
            res = file.open(path=path)
        else:
            res = file.open()

        if res == False:
            row = self.sidebar.row(file)
            self.sidebar.takeItem(row)
            file.deactivate()
            return False

        self.setWindowTitle(f'{file.getNameAndStar()} - NoteNook')
        file.ignoreChanges = False

    def saveOpenFile(self):
        if hasattr(file_manager, "active") and file_manager.active is not None:
            file = file_manager.active
        else:
            return

        file.save()
        self.setWindowTitle(f'{file.getNameAndStar()} - NoteNook')

    def textChanged(self, textEdit: str):
        if file_manager.ignoreChanges:
            return

        if hasattr(file_manager, "active") and file_manager.active is not None:
            active_file = file_manager.active
        else:
            return
        if active_file._unsaved == False:
            print(
                f"{active_file.file_name} is now unsaved")
            active_file.makeUnsaved()
            self.setWindowTitle(f'{active_file.getNameAndStar()} - NoteNook')

        if len(textEdit) > 0:
            if textEdit[-1] == "/" or textEdit[-1] == "\\":
                self.slashMenu(textEdit)

    def copy_text(self):
        # Get the selected text and copy it to the clipboard
        selected_text = self.text_edit.textCursor().selectedText()
        clipboard = QApplication.clipboard()
        clipboard.setText(selected_text)

    def paste_text(self):
        # Get the text from the clipboard and insert it into the text edit
        clipboard = QApplication.clipboard()
        self.text_edit.insertPlainText(clipboard.text())


def quit_app():
    sys.exit()


if __name__ == '__main__':
    app = QApplication(sys.argv)

    window = MainWindow()

    with open('styles/global.qss', 'r') as f:
        style_sheet = f.read()
    # Set the global style sheet
    app.setStyleSheet(style_sheet)

    # check if theme is installed
    if os.path.exists("./.NoteNook/themes/theme.qss"):
        try:
            with open("./.NoteNook/themes/theme.qss", 'r') as f:
                user_theme = f.read()

            if user_theme:
                window.setStyleSheet(user_theme)
                print("applied custom theme")
            else:
                print("WARNING: Custom theme.qss is blank")

        except Exception as e:
            print(e)
            show_custom_exception_popup("Warning", "Failed to load custom theme",
                                        "check if the theme.qss file is acessible and not used by another program. Press OK to continue.")

    window.resize(1800, 1000)
    window.show()
    sys.exit(app.exec_())
