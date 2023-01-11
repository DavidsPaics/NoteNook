from utils import show_exception_popup
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import QTextEdit


def make_text_bold(text_edit: QTextEdit):
    # Get the current cursor position and selection
    cursor = text_edit.textCursor()

    # Check if there is a selection
    if cursor.hasSelection():
        # Get the selected text
        selected_text = cursor.selectedText()

        # Get the font weight of the first character
        char_format = cursor.charFormat()
        font_weight = char_format.fontWeight()

        # If the font weight is bold, set it to regular
        if font_weight == QFont.Bold:
            char_format.setFontWeight(QFont.Normal)
            cursor.setCharFormat(char_format)
        else:
            # If the font weight is not bold, set it to bold
            char_format.setFontWeight(QFont.Bold)
            cursor.insertText(selected_text, char_format)
    else:
        # If there is no selection, set the font weight of the current character to bold
        char_format = cursor.charFormat()
        char_format.setFontWeight(QFont.Bold)
        cursor.setCharFormat(char_format)


def make_text_italic(text_edit: QTextEdit):
    # Get the current cursor position and selection
    cursor = text_edit.textCursor()

    # Check if there is a selection
    if cursor.hasSelection():
        # Get the selected text
        selected_text = cursor.selectedText()

        # Get the font weight of the first character
        char_format = cursor.charFormat()

        # If the font weight is bold, set it to regular
        if char_format.fontItalic() == True:
            char_format.setFontItalic(False)
            cursor.setCharFormat(char_format)
        else:
            # If the font weight is not bold, set it to bold
            char_format.setFontItalic(True)
            cursor.insertText(selected_text, char_format)
    else:
        # If there is no selection, set the font weight of the current character to bold
        char_format = cursor.charFormat()
        char_format.setFontItalic(True)
        cursor.setCharFormat(char_format)
