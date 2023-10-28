### Version 0.2.9
- Fixed markdown problems with newer pandoc versions

### Version 0.2.8
- Fixed some Binary Build bugs
- Fixed some Preference bugs
- Support of newer pandoc versions

### Version 0.2.7
- Maximized the Option filed for more input
- Simplified the from / to format dialogs
- Made the batch Widget hidable
- Fixed find pandoc in from / to dialog
- Extended Old-Gui Batch Dialog with Output-directory

### Version 0.2.6
- Batch Converter save file without the original extension
- Added seperat Batch Ouptut directory
- Added Buffer SaveToFile Option
- Added BufferSaveSuffix and BufferSaveName fields
- Switched binary creation tool to pyinstaller
- Code Cleanup

### Version 0.2.5
- Code Cleanup
- Bug Fix for the MacBinary Version

### Version 0.2.4
- Added new Interface
- Added possibility to use the old Interface instead

### Version 0.2.3
- Added Counter for written log messages
- Code Cleanup of converters
- Code Cleanup of Functions for Check of Converters
- All errors are written to the log viewer, except a fatal error message


### Version 0.2.2
- Added seperated Log-Viewer
- Added Make the Windows Position + Size savable
- Added Make the Log-Viewer Position + Size savable
- Added Make the Dialogs Position + Size sabable
- Added Date / Time of the Log-Messages
- Added Adjust the LogViewer Position manually
- Fixed From / To Formats Dialogs


### Version 0.2.1
- Added Multilanguage Support
- Supported languages: English, German, (Spanish: 40%)
- Added Blank Translation File
- Fixed Error when inserting a new Path in Preferences

### Version 0.2.0
- Fixed About Dialog in Binary Versions
- Fixed Error handling of Path detection in windows

### Version 0.1.9
- Added Batch Conversion for Standard Converters
- Added Batch Conversion for Lyx in Standard Conversion
- Added Filefilter option for Batch Conversion
- Code Cleanup
- Cleaner Error handling

### Version 0.1.8
- Added: Standard Batch Conversion support
- Missing: Lyx Standard Batch Conversion support

### Version 0.1.7
- Added: Support pandoc Versions greater 1.18
- Fixed: Change of the Help-System Windows

### Version 0.1.6
- Code Cleanup
- Fixed: Gui Cleanup (Deleted the menu functions for the converters)
- Fixed: a bug for FreeBSD (Posix-System)

### Version 0.1.5
- Added: Batch Converion Mode (Files, Directories, Recursive Directories)
- Added: OpenDirectory-Buttons for path input
- Added: Help-Buttons for from-formats, to-formats and options

### Version 0.1.4
- Added: Preference for Open/Safe-Path (Standard is the Home-Directory)
- Added: a Help menu for the pandoc user guide
- Added: a undo function
- Removed: save button, changed to save buffer (Only in Memory)

### Version 0.1.3
- Added Support for the binary format docx in the from section (Manual Converter only (Needs Pandoc 1.13.1 or better)
- Added Preferences for the Manual Converter
- Added Support for error-messages from the Manual Converter
- Bugfix: Binary Handling of the Manual Converter (For odt, docx formats)

### Version 0.1.2
- Fixed: Message after filewrite to filesystem (e.g. odt-Export)
- Fixed: Change to multiple Arguments

### Version 0.1.1
- Added: integrated Lyx Support via Multimarkdown
- Added: Change the Default Converters via Preferences
- Added: Preferences are saved as QSettings
- Added: Set open/save-path to homefolder
