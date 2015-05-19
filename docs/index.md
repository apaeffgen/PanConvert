# Basic Information
## Supported Formats:

All by Pandoc supported formats can be used. See: [UserGuide
Pandoc](http://johnmacfarlane.net/pandoc/README.html)

To use all not explicitly listed formats of pandoc, you have to use the
manual converter.

## Usage of the manual converter 

The Standard – Checkbox has to be unchecked.

In the from field you have to fill in the supported pandoc formats of
the source format.

In the to field you have to fill in the supported pandoc formats of the
destination format

In the Parameter field, all known pandoc parameters, separated via semicolon ';' can be used.

For some formats the Parameter field can be left blank, for others it
has to be filled. 

To get a odt or epub file, you have to specify the name of the file. There is a working
example for odt filled in already. The file will be saved in the same directory where the panconvert directory is saved, e.g. on MacOS it will be /Applications



## Path to pandoc

The program tries to detect where your pandoc executable is installed.
If that fails, you can use the preferences dialog in the Edit – Menu to
manually save the path to the executable.

## Platforms tested: (Source-Code)

*  Windows 7 (32bit)
*  Mac OS: Lion (32bit), Mountain Lion (64bit), Mavericks (64bit)
*  Linux Mint 17: Ubuntu

Not Running: (Linux Mint Debian: does not work without tweaking the
ui-code of the main ui-file. It is a problem of the installed
QT-Version)

## System Requirements 

The binaries are self-contained. Only [pandoc](http://johnmacfarlane.net/pandoc/installing.html) and optionally [multimarkdown](http://fletcherpenney.net/multimarkdown/download/) have to be installed

For the source-code to be run, these additional Software-Packages have to be installed for running
PanConvert.

*  Python3
*  QT5
*  PyQT5


Some older Versions of Python3 or QT5 might not work