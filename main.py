import os
import sys
from PyQt5 import QtCore
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QTextCursor, QTextCharFormat, QKeySequence, QFont, QIcon
from PyQt5.QtWidgets import QApplication, QMainWindow, QTextEdit, QListWidget, QDockWidget, QMenuBar, QMenu, QAction, QMessageBox, QListWidgetItem
from errors import show_exception_popup, show_custom_exception_popup
import fonts
import file_manager


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        # Set the window title
        self.setWindowTitle('NoteNook')

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

        self.sidebar.itemClicked.connect(lambda: activate())

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

        open_action = QAction('Open', self)
        open_action.triggered.connect(self.openNewFile)
        open_action.setShortcut(QKeySequence("Ctrl+O"))
        self.file_menu.addAction(open_action)

        save_action = QAction('Open', self)
        save_action.triggered.connect(self.saveOpenFile)
        save_action.setShortcut(QKeySequence("Ctrl+S"))
        self.file_menu.addAction(save_action)

        self.file_menu.addSeparator()

        quit_action = QAction("Quit", self)
        quit_action.triggered.connect(quit_app)
        self.file_menu.addAction(quit_action)

        # Create the "Edit" menu
        self.edit_menu = QMenu('Edit')
        self.menu_bar.addMenu(self.edit_menu)

        # Create the "Format" menu
        self.format_menu = QMenu('Format')
        self.edit_menu.addMenu(self.format_menu)

        # Create the "Bold" action
        bold_action = QAction('Bold', self)
        bold_action.triggered.connect(
            lambda: fonts.make_text_bold(self.text_edit))
        bold_action.setShortcut(QKeySequence("Ctrl+B"))
        self.format_menu.addAction(bold_action)

        # Create the "Italic" action
        italic_action = QAction('Italic', self)
        italic_action.triggered.connect(
            lambda: fonts.make_text_italic(self.text_edit))
        italic_action.setShortcut(QKeySequence("Ctrl+I"))
        self.format_menu.addAction(italic_action)

        copy_action = QAction("Copy", self)
        paste_action = QAction("Paste", self)

        copy_action.triggered.connect(self.copy_text)
        paste_action.triggered.connect(self.paste_text)

        self.edit_menu.addAction(copy_action)
        self.edit_menu.addAction(paste_action)

        # Create the "View" menu
        self.view_menu = QMenu('View')
        self.menu_bar.addMenu(self.view_menu)

        # Create the "Help" menu
        self.help_menu = QMenu('Help')
        self.menu_bar.addMenu(self.help_menu)

    def slashMenu(self, text: str):
        pass

    def openNewFile(self, path=None, savable=True, editable=True):
        file = file_manager.fileListItem(
            self.sidebar, self.text_edit, savable=savable, editable=editable)
        file.ignoreChanges = True
        if path != None:
            file.open(path=path)
        else:
            file.open()
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
            active_file.makeUnsaved()
            self.setWindowTitle(f'{active_file.getNameAndStar()} - NoteNook')

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
    if os.path.exists("./themes/theme.qss"):
        try:
            with open("./themes/theme.qss", 'r') as f:
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
