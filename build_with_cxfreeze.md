## Building selfcontained executables

### Prerequisites

- Installing QT5, PyQT5, Python3 (see readme.md)
- Installing the cx_freeze scripts for your platform (See http://cx-freeze.sourceforge.net)
- Test that you can run Panconvert.py with your Python3 interpreter


### Running the Build-Script
- Run the setup_cxfreeze.py script with the parameter according to your platform 
- /usr/local/bin/python3 setup_cxfreeze.py bdist_mac
- C:\Python34\python.exe setup_cxfreeze.py bdist_msi


### MacOS Quirks

Depending on your environment, you have to change some code in macdist.py on Line 186 from the first to the second line:

- if (name not in files and not path.startswith('/usr') 
- if (name not in files and not path.startswith('/usr/lib') and not

Move the folder platforms from /Contents/MacOS/lib/ to /Contents/MacOS/. This will give you a bigger, but running binary
 application on 64bit MacOS without PyQT and QT installed.






