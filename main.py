import os
import pathlib
import sys
from PyQt5 import QtCore
from PyQt5.QtCore import Qt, QRect, QRectF
from PyQt5.QtGui import QTextCursor, QTextCharFormat, QKeySequence, QFont, QIcon
from PyQt5.QtWidgets import QApplication, QMainWindow, QTextEdit, QListWidget, QDockWidget, QMenuBar, QMenu, QAction
from PyQt5.QtWidgets import QLineEdit, QCompleter, QMessageBox, QListWidgetItem, QAbstractItemView, QDesktopWidget
from utils import show_exception_popup, show_custom_exception_popup
import fonts
import file_manager
import setup
import search_bar


def createMenuAction(text: str, parent, function, shortcut=None, autoRepeat=False):
    action = QAction(text, parent)
    action.triggered.connect(function)
    action.setAutoRepeat(autoRepeat)
    if shortcut:
        action.setShortcut(QKeySequence(shortcut))
    return action


class mainTextField(QTextEdit):
    def __init__(self, main_window):
        self.main_window = main_window
        self.keyPressEvent = self.key_event
        super().__init__()

    def key_event(self, event):
        if event.key() == QtCore.Qt.Key_Slash or event.key() == QtCore.Qt.Key_Backslash:
            self.main_window.slashMenu()
        else:
            super().keyPressEvent(event)


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.closeEvent = self.handleCloseEvent

        self.setContextMenuPolicy(Qt.CustomContextMenu)

        # Set the window title
        self.setWindowTitle('NoteNook')
        self.setWindowIcon(QIcon("./icons/NoteNookIcon.png"))

        # Create a QTextEdit widget and set it as the central widget
        self.text_edit = mainTextField(self)
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

        self.openNewFile("./Getting Started.html",
                         savable=False, editable=False)

        self.menuBar()

        self.slashMenuWidget = search_bar.SlashMenu(self.text_edit)

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

        self.file_menu.addAction(createMenuAction(
            'Close', self, self.closeCurrentFile, "Ctrl+W"))

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

    def closeCurrentFile(self):
        file_manager.active.close()

    def createNewFile(self):
        file = file_manager.fileListItem(
            self.sidebar, self.text_edit, savable=True, editable=True)
        file.openNewFile()
        self.setWindowTitle(f'{file.getNameAndStar()} - NoteNook')

    def slashMenu(self):
        self.slashMenuWidget.show()

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

    def keyPressEvent(self, event):
        if event.key() == QtCore.Qt.Key_Slash:
            self.on_slash_key_pressed()
        super().keyPressEvent(event)

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

    def copy_text(self):
        # Get the selected text and copy it to the clipboard
        selected_text = self.text_edit.textCursor().selectedText()
        clipboard = QApplication.clipboard()
        clipboard.setText(selected_text)

    def paste_text(self):
        # Get the text from the clipboard and insert it into the text edit
        clipboard = QApplication.clipboard()
        self.text_edit.insertPlainText(clipboard.text())

    def handleCloseEvent(self, event):
        unsaved_files = False
        for i in range(self.sidebar.count()):
            item = self.sidebar.item(i)
            if item._unsaved:
                unsaved_files = True
                break

        if unsaved_files:
            # Show a confirmation dialog to the user
            reply = QMessageBox.question(self, 'Confirm Exit',
                                         "Are you sure you want to exit without saving?\n\nAny unsaved changes will be lost", QMessageBox.Yes |
                                         QMessageBox.No, QMessageBox.No)
            if reply == QMessageBox.Yes:
                # If the user chooses "Yes", close the app
                sys.exit()
            else:
                # If the user chooses "No", ignore the close event
                event.ignore()

        else:
            event.accept()


def quit_app():
    sys.exit()


if __name__ == '__main__':
    setup.install_if_needed()

    app = QApplication(sys.argv)

    window = MainWindow()

    setup.load_theme(app)

    window.resize(1800, 1000)
    window.show()
    sys.exit(app.exec_())
