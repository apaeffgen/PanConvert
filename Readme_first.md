## Filelist Overview

- In the Folder Newest there are all actual versions of Panconvert
- In the Xtras_Archive there are older versions
- If you have problems with the newest version, try one of the older versions instead. Or use the source code.

## Windows Binary

- There is an installer and a zip-file provided
- If you use the zip-file, extract it wherever you want and doubleclick Panconvert.exe in the main folder.
- The installer will guide you through the process

## Mac Binary

### Installer-Version

- Unzip the Installer-Package
- Doubble-Click on the Installer
- All MacOS Versions and Intel+M1/2 should work
- Pandoc is bundled with the app, but you can use your own version
- Panconvert is installed in a folder called Pandoc in the application folder.

### DMG-Version

- Mount the dmg-Image
- Move Panconvert.app to the application folder
- Start the app like any other MacOS application


## Linux Binary

Attention: Because there are so many flavours of linux with a lot of different versions of the basic system, it can be,
that the binary will not start. Also because of the hassle, in future releases no binary versions will be produced but testet.

- So use the the source code version if you run into troubles with the old binaries.
- Mainly glibc versions could be to old or to new. But when something goes wrong, your are in the wild.

## To Install from Source

### Before you beginn

* Install all required components. See  the Installation Checklist below.
* The newest source code supports all pandoc versions
* (Optional: Multimarkdown: for markdown to Lyx-Support)

###  Installation Checklist
Check which packets are already installed on your system. Normally Python3 exists on many supported platforms. On Linux somethimes QT5 is preinstalled.

* Install Python3
* Install QT5.11. Other versions of QT may or may not work
* Install Pyqt5.11.3
* Install Pandoc
* Optional_Install: multimarkdown
* See also http://panconvert.readthedocks.io
