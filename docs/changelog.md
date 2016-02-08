## Version 0,1.6
Code Cleanup
Gui Cleanup (Deleted the menu functions for the converters)
Fixed a bug for FreeBSD (Posix-System)



## Version 0.1.5

### New Features
- Added Batch Converion Mode (Files, Directories, Recursive Directories)
- Added OpenDirectory-Buttons for path input
- Added Help-Buttons for from-formats, to-formats and options

## Version 0.1.4

### New Features
- Added Preference for Open/Safe-Path (Standard is the Home-Directory)
- Added a Help menu for the pandoc user guide
- Added a undo function
- Removed save button, changed to save buffer (Only in Memory)

## Version 0.1.3

### New Features
- Added Support for the binary format docx in the from section (Manual Converter only (Needs Pandoc 1.13.1 or better)
- Added Preferences for the Manual Converter
- Added Support for error-messages from the Manual Converter

### Bug Fixes
- Binary Handling of the Manual Converter (For odt, docx formats)

## Version 0.1.2

### Bug Fixes
- Fixed: Message after filewrite to filesystem (e.g. odt-Export)
- Fixed: Change to multiple Arguments

## Version 0.1.1

### New Features

- integrated Lyx Support via Multimarkdown
- Change the Default Converters via Preferences

### Bug Fixes

- Preferences are saved as QSettings
- Set open/save-path to homefolder
