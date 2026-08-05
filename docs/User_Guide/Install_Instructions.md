# Installation instruction

## Before you begin

* Either install a [binary version](https://sourceforge.net/projects/panconvert/files/Newest-Releases/)) of PanConvert or

* Install all required components. See the Installation Checklist below.
* You need to have [pandoc](https://pandoc.org/) installed (>=2.0, tested with 3.1.8+).
* The newest source code supports all pandoc versions.
* (Optional: Multimarkdown: for markdown to Lyx-Support)

## Python Version

* Python 3.12 or newer is required.
* Python 3.14 is also supported.

## Installation Checklist

Check which packages are already installed on your system. Normally Python3 exists on many supported platforms.

* Install Python 3.12+
* Install [PyQt6](https://www.riverbankcomputing.com/software/pyqt/) (>=6.5.0).
  **Note:** On Windows, pin to `PyQt6<6.7.0` due to a known stack-buffer-overflow crash (see `requirements.txt`).
* Install [pandoc](https://pandoc.org/installing.html)
* Optional: Install [multimarkdown](https://fletcherpenney.net/multimarkdown/download/)



## MacOS

## Windows

## Linux