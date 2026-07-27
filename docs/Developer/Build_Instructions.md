# Building selfcontained executables

## Prerequisites

- Installing QT6 PyQT6, Python3.12.x. The Version QT6.11 on Windows seems to make problems.
- Installing the pyinstaller scripts for your platform (See http://pyinstaller.readthedocs.io)
- Test that you can run Panconvert.py with your Python3 interpreter


## Running the Build-Script
- Run pyinstaller Panconvert.spec
- some usefull optins for all plattforms: --onefile --windowed
- The programs can be to packaged: create-dmg for Macos, Inno Setup for windows or Zipped for Linux


## Known Issues:

- Not thourougly tested. 






