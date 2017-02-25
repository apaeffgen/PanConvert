# Readme first (Version 0.1.3 and above)

## Installation

Running the program you must have installed the following additional software-packages:

- pandoc (all versions are supported)
- multimarkdown (optional for Lyx conversion)
- python3
- QT5
- pyqt5

## Update from previous versions
If Panconvert 0.1.1 or above had been used, the previous settings have to be deleted, or Panconvert may crash:

- On Windows, open registry editor go to HKEY_CURRENT_USER/Software and delete the folder Pandoc
- On MacOS delete /Users/<USERNAME>/Library/Preferences/com.apaeffgen.PanConvert.plist
- On Linux delete /home/<USERNAME>/.config/Pandoc/PanConvert.conf

## Known Problems

Not working is python2, QT4 and pyqt4. There can be some issues with older versions of QT5 and pyqt5. QT5.3.0 is
initially used.

## Extended installation instructions

On Linux most actual distributions come preinstalled with the last 3 packages. Package-Managers allow to install pandoc.
Multimarkdown has to be compiled from source

On Windows you have to manually install all the packages by hand. See all the links below.

On MacOS homebrew can be used to install python3, QT5 and pyqt5. Pandoc has to be downloaded from the pandoc-homepage.


- http://johnmacfarlane.net/pandoc/
- http://fletcherpenney.net/multimarkdown/
- https://www.python.org/downloads/
- http://qt-project.org/downloads
- http://www.riverbankcomputing.co.uk/software/pyqt/download5
- http://brew.sh

If all the dependencies are properly installed, you can run the program:
On the commandline you have to first cd into the appropriate directory.

- on windows by double-clicking on Panconvert.py
- on Linux by starting the commandline: python3 Panconvert.py
- on MaOS by opening the terminal and typing python3 Panconvert.py

## Usage

There is help available at http://panconvert.sourceforge.net/help.html
The help can be used also inside the started Gui.

## License

The software is licensed under the GNU General Public License.
Thanks Juho Vepsäläinen, at https://github.com/bebraw/pypandoc, interface_pandoc.py is licensed under MIT license


