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

Because there are many Linux distributions with different system library versions, binaries may not start on older systems.

- Use the source code version if you run into trouble with the binaries.
- glibc version mismatches are the most common issue on older distributions.
- Linux binaries are provided where possible; source install is recommended for older systems.

## To Install from Source

### Before you beginn

* Install all required components. See  the Installation Checklist below.
* The newest source code supports all pandoc versions
* (Optional: Multimarkdown: for markdown to Lyx-Support)

### Installation Checklist

Check which packages are already installed on your system. Normally Python3 exists on many supported platforms.

* Install Python 3.12+
* Install PyQt6 (>=6.5.0). On Windows, pin to <6.7.0.
* Install Pandoc (>=2.0)
* Optional: Install multimarkdown
* See also https://panconvert.sourceforge.net
