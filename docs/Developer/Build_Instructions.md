# Building Self-Contained Executables

## Running the Build Script

### Mac OS
```bash
cd packaging/macos
./build.sh
```

### Windows
```bash
cd packaging/windows
python build_exe.py
```

### Linux
```bash
cd packaging/linux
./build_linux.sh
```

### Common PyInstaller Options

- `--onefile`: Create a single executable file
- `--windowed`: No console window (GUI mode)

### Packaging

- **macOS:** `create-dmg` for DMG creation
- **Windows:** Inno Setup for installer
- **Linux:** ZIP archive

## Known Issues

- Builds are not thoroughly tested on all platforms.
- Windows builds require `PyQt6<6.7.0` to avoid crashes. 

## Manual Installation
You need the following Software and the sourcecode installed.
- Panconvert source code
- pandoc binary
- Python 3.12+ (tested with 3.12 and 3.14)
- PyQt6 (>=6.5.0). **On Windows, pin to <6.7.0** due to a known stack-buffer-overflow crash.
- PyInstaller >=6.0
- Test that you can run `Panconvert.py` with your Python3 interpreter





