# Building selfcontained executables

## Prerequisites

- Installing QT5, PyQT5, Python3 (see readme.md)
- Installing the pyinstaller scripts for your platform (See http://pyinstaller.readthedocs.io)
- Test that you can run Panconvert.py with your Python3 interpreter


## Running the Build-Script
- Run pyinstaller Panconvert.spec
- some usefull optins for all plattforms: --onefile --windowed
- The programs have to be packaged: create-dmg for Macos, Inno Setup for windows or Zipped for Linux


## Known Issues:

- Copy the QtWebEngineProcess.app directly into the MacOS section of the Bundle
- Copy qtwebengine_devtools_resources.pak
       qtwebengine_resources_100p.pak
       qtwebengine_resources_200p.pak
       qtwebengine_resources.pak
       icudtl.dat
       to the Resources folder of the Bundle.
- The source code is not fully compatible with the --windowed option. Expect some glitches of
autodetection of pandoc






