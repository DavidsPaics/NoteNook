# Notenook
## Installation
### Dependencies:
- Python 3
- PyInstaller
- PyQt5
- Git (To clone this repository)

### Linux (I tested this only on debian):

#### Compiling from source:

1. Install the latest version of python from [python.org](https://www.python.org)

2. Install the required dependencies with Pip
    ```
    pip install PyQt5 pyinstaller --user
    ```
3. Clone the repository 
    ```
    git clone https://github.com/that-skyfox/NoteNook.git
    cd NoteNook
    ```

3. Compile the python code
    ```
    pyinstaller --noconsole --onedir --add-data "styles/global.qss:styles/" --add-data "./icons/:./icons/" --add-data "./Getting Started.html:./" -n NoteNook --icon "./icons/NoteNookIcon.png" --noconfirm main.py
    ```
4. Run the executable
    ```
    ./dist/NoteNook/NoteNook
    ```

#### The full code to compile from source and run the app:

```
pip install PyQt5 pyinstaller --user
git clone https://github.com/that-skyfox/NoteNook.git
cd NoteNook
pyinstaller --noconsole --onedir --add-data "styles/global.qss:styles/" --add-data "./icons/:./icons/" --add-data "./Getting Started.html:./" -n NoteNook --icon "./icons/NoteNookIcon.png" --noconfirm main.py
./dist/NoteNook/NoteNook
```
