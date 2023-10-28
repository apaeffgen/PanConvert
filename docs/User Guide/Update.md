# Important Notes
## Update from previous versions
If Panconvert 0.1.1 or above had been used, the previous settings have to be deleted, or Panconvert may crash: 

- On Windows, open registry editor go to HKEY_CURRENT_USER/Software and delete the folder Pandoc
- On MacOS delete /Users/<USERNAME>/Library/Preferences/com.apaeffgen.PanConvert.plist
- On Linux delete /home/<USERNAME>/.config/Pandoc/PanConvert.conf