# Customizing Panconvert

## General Settings

* **Default Converter:** Choose which converter Panconvert starts with (Standard or Manual).
* **GUI Style:** Select between the New GUI (default) or Legacy GUI.
* **Language:** Panconvert supports multiple languages (English, German, Spanish).
  The language is saved per-user in QSettings.
* **Pandoc Path:** Configure the path to your pandoc executable.
* **Open/Save Path:** Set the default directory for file open/save dialogs.

## Size Settings

Here you can configure Panconvert to remember the size and position of windows and dialogs.

* Main Window Size and Position
* Log Window Size and Position
* Dialog Positions

## Preferences Location

Preferences are stored in QSettings, which uses platform-specific storage:

| Platform | Location |
|----------|----------|
| Windows | Registry: `HKEY_CURRENT_USER\Software\Pandoc\PanConvert` |
| macOS | `~/Library/Preferences/com.apaeffgen.PanConvert.plist` |
| Linux | `~/.config/Pandoc/PanConvert.conf` |