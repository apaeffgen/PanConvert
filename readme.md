# Readme first
## Help and further information
At the [official Website](https://panconvert.sourceforge.net) you will find more detailed information.
There is help available at [ReadTheDocs](https://panconvert.readthedocs.io/en/latest/)


## Installation
On Windows and Mac the [automated installer](https://sourceforge.net/projects/panconvert/) walks you through the installation procedure 
and copies a bundled pandoc version with pandoc and an uninstaller. So you do not need to install pandoc yourself.
You will find the binaries [here](https://sourceforge.net/projects/panconvert/)

On Linux please read the extended installation instruction.

## Usage
In the preference settings you can specify the path of your own pandoc, if you do not want to use the bundled version.
The help, see above, can be used also inside the started Gui.

## Update from previous versions
If Panconvert previously had been used, the previous settings may have to be deleted, or Panconvert may crash:

- On Windows, open registry editor go to HKEY_CURRENT_USER/Software and delete the folder Pandoc
- On MacOS delete /Users/<USERNAME>/Library/Preferences/com.apaeffgen.PanConvert.plist
- On Linux delete /home/<USERNAME>/.config/Pandoc/PanConvert.conf

## Known Problems

* Python 2, Qt4, and PyQt4 are no longer supported. PanConvert requires Python 3.12+ and PyQt6.
* There may be issues with older or newer versions of PyQt6. PyQt6 >=6.5.0 and <6.7.0 (on Windows) is tested.
* Some pandoc versions may cause problems due to changed behavior or bugs in PanConvert.
* Linux binaries may not work on older distributions due to glibc requirements. Use the source install.

If you find a bug or problem, submit a bug report to the GitHub issue tracker.

## Extended installation instructions for running the source code or running on Linux

Running the program requires the following additional software packages:

- [pandoc](https://pandoc.org/) (all newer versions are supported, tested with 3.1.8+)
- [Python 3.12+](https://www.python.org/downloads/)
- [PyQt6](https://www.riverbankcomputing.com/software/pyqt/) (>=6.5.0)
- Qt6 WebEngine

On Linux, most current distributions come preinstalled with Python3. Use package managers to install pandoc and PyQt6.

On Windows, install all packages manually:
```bash
pip install "PyQt6<6.7.0"
pip install PyQt6-WebEngine
```

On macOS, Homebrew can be used:
```bash
brew install pandoc
brew install python@3.12
pip3 install PyQt6 PyQt6-WebEngine
```

If all dependencies are properly installed, you can run the program:
- On Windows: double-click `Panconvert.py`
- On Linux: `python3 Panconvert.py`
- On macOS: `python3 Panconvert.py`

If all the dependencies are properly installed, you can run the program:
On the commandline you have to first cd into the appropriate directory.

- on windows by double-clicking on Panconvert.py
- on Linux by starting the commandline: python3 Panconvert.py
- on MaOS by opening the terminal and typing python3 Panconvert.py

## License

The software is licensed under the GNU General Public License.