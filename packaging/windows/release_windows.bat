@echo off
REM release_windows.bat - Publish files from the dist folder to a GitHub release
REM Usage: release_windows.bat [version]
REM
REM Prerequisites:
REM   1. Set GH_TOKEN environment variable with a GitHub Personal Access Token
REM      (scope: repo, public_repo)
REM   2. Or run gh auth login first
REM   3. Ensure dist/ contains the built artifacts
REM
REM Example:
REM   set GH_TOKEN=ghp_your_token_here
REM   release_windows.bat 0.4.0
REM
REM   Or authenticate first:
REM   gh auth login --with-token
REM   release_windows.bat 0.4.0

setlocal enabledelayedexpansion

:: ── Setup ─────────────────────────────────────────────────────────────────────
cd /d "%~dp0..\.." || exit /b 1

:: ── Detect platform ───────────────────────────────────────────────────────────
set "PLATFORM=windows"
echo Detected platform: %PLATFORM%

:: ── Check authentication ──────────────────────────────────────────────────────
gh auth status >nul 2>&1 || (
    echo Not authenticated with GitHub.
    echo.
    echo Option 1: Set GH_TOKEN environment variable:
    echo   set GH_TOKEN=ghp_your_token_here
    echo.
    echo Option 2: Login interactively:
    echo   gh auth login
    echo.
    echo Option 3: Login with token directly:
    echo   gh auth login --with-token
    exit /b 1
)

:: ── Get version ───────────────────────────────────────────────────────────────
if "%~1" neq "" (
    set "VERSION=%~1"
) else (
    REM Extract version from messages.py
    for /f "delims==" %%a in ('findstr /r "^versionnumber = " source\language\messages.py') do (
        set "VERSION=%%a"
    )
    set "VERSION=!VERSION:*'=%"
    set "VERSION=!VERSION:"=%"
)

:: Remove 'v' prefix if present
set "VERSION=!VERSION:v=%"

echo Publishing release: v!VERSION!

:: ── Check dist folder exists and has files ────────────────────────────────────
if not exist "dist" (
    echo dist/ folder not found. Build your release first.
    exit /b 1
)

dir /b dist\* >nul 2>&1 || (
    echo dist/ folder is empty. Nothing to publish.
    exit /b 1
)

echo.
echo Classifying artifacts in dist/:

:: ── Classify files by platform using temp files ───────────────────────────────
set "TMP_DIR=%TEMP%\release_%%RANDOM%%"
mkdir "!TMP_DIR!" >nul 2>&1

set "DEBIAN_TMP=!TMP_DIR!\debian"
set "RHEL_TMP=!TMP_DIR!\rhel"
set "ARCH_TMP=!TMP_DIR!\arch"
set "MACOS_TMP=!TMP_DIR!\macos"
set "WINDOWS_TMP=!TMP_DIR!\windows"
set "LINUX_TMP=!TMP_DIR!\linux"
set "UNKNOWN_TMP=!TMP_DIR!\unknown"

for %%f in (dist\*) do (
    if exist "%%f" (
        set "FILE=%%f"
        set "BASENAME=%%~nxf"
        set "LOWERNAME="
        for %%l in (a b c d e f g h i j k l m n o p q r s t u v w x y z) do (
            set "LOWERNAME=!LOWERNAME:%%l=%%l!"
        )
        set "LOWERNAME=!BASENAME!"

        call :classify "!LOWERNAME!" "!FILE!"
    )
)

:: ── Display classified files ──────────────────────────────────────────────────
for %%p in (debian rhel arch macos windows linux unknown) do (
    if exist "!TMP_DIR!\%%p" (
        for %%f in (!TMP_DIR!\%%p) do (
            echo   [%%p] %%~nxf
        )
    )
done

:: ── Summary ───────────────────────────────────────────────────────────────────
echo.
echo Summary:
for %%p in (debian rhel arch macos windows linux) do (
    if exist "!TMP_DIR!\%%p" (
        set "COUNT=0"
        for %%f in (!TMP_DIR!\%%p) do set /a COUNT+=1
        echo   %%p (!COUNT! file(s))
    )
)
if exist "!TMP_DIR!\unknown" (
    set "COUNT=0"
    for %%f in (!TMP_DIR!\unknown) do set /a COUNT+=1
    echo   unknown (!COUNT! file(s))
)

echo.
echo Will upload all artifacts from dist/

:: ── Create git tag ────────────────────────────────────────────────────────────
set "TAG=v!VERSION!"
git rev-parse "!TAG!" >nul 2>&1 || (
    git tag -a "!TAG!" -m "Release !TAG!"
    echo Created git tag !TAG!
)

:: ── Push tag ──────────────────────────────────────────────────────────────────
echo Pushing tag to GitHub...
if defined GH_TOKEN (
    git remote set-url origin "https://x-access-token:!GH_TOKEN%@github.com/apaeffgen/Panconvert.git"
)
git push origin "!TAG!"
echo Tag pushed

:: ── Check if release already exists ───────────────────────────────────────────
gh release view "!TAG!" >nul 2>&1 && (
    echo.
    echo Release !TAG! already exists.
    echo.
    echo Existing assets:
    gh release view "!TAG!" --json name,assets --jq '.assets[].name' 2>nul || true
    echo.
    set /p "REPLY=Re-upload the files from dist/? (y/N) "
    if /i "!REPLY!" neq "y" (
        echo Skipping upload. Release already exists.
        echo   View at: https://github.com/apaeffgen/PanConvert/releases/tag/!TAG!
        rmdir /s /q "!TMP_DIR!" >nul 2>&1
        exit /b 0
    )
)

:: ── Build release notes ───────────────────────────────────────────────────────
set "NOTES_FILE=!TMP_DIR!\notes.md"
(
echo ## Changes
echo - See [changelog](docs/Developer/changelog.md) for full details
echo.
echo ## Downloads
echo.
echo | Platform | File |
echo |----------|------|
) > "!NOTES_FILE!"

for %%p in (debian rhel arch macos windows linux) do (
    if exist "!TMP_DIR!\%%p" (
        for %%f in (!TMP_DIR!\%%p) do (
            echo | %%p | %%~nxf |
        )
    )
) >> "!NOTES_FILE!"

(
echo.
echo ## Installation
echo See [ReadTheDocs](https://panconvert.readthedocs.io/en/latest/) for installation instructions.
) >> "!NOTES_FILE!"

:: ── Create or update GitHub release ───────────────────────────────────────────
echo.
echo Creating GitHub release...

gh release view "!TAG!" >nul 2>&1 && (
    REM Update existing release
    gh release upload "!TAG!" dist\* --clobber
    echo Release v!VERSION! updated!
) || (
    REM Create new release
    gh release create "!TAG!" ^
        --title "Panconvert !TAG!" ^
        --notes-file "!NOTES_FILE!" ^
        dist\*
    echo Release v!VERSION! published!
)
echo   View at: https://github.com/apaeffgen/PanConvert/releases/tag/!TAG!

:: ── Cleanup ───────────────────────────────────────────────────────────────────
rmdir /s /q "!TMP_DIR!" >nul 2>&1

exit /b 0

:: ── Helper: classify a file by platform ───────────────────────────────────────
:classify
set "NAME=%~1"
set "FILE=%~2"

echo !NAME! | findstr /i "debian ubuntu" >nul && (
    echo !FILE! >> "!TMP_DIR!\debian"
    goto :eof
)
echo !NAME! | findstr /i "rhel centos fedora rocky" >nul && (
    echo !FILE! >> "!TMP_DIR!\rhel"
    goto :eof
)
echo !NAME! | findstr /i "arch pacman" >nul && (
    echo !FILE! >> "!TMP_DIR!\arch"
    goto :eof
)
echo !NAME! | findstr /i "macos darwin dmg pkg" >nul && (
    echo !FILE! >> "!TMP_DIR!\macos"
    goto :eof
)
echo !NAME! | findstr /i "windows msi exe zip" >nul && (
    echo !FILE! >> "!TMP_DIR!\windows"
    goto :eof
)
echo !NAME! | findstr /i "linux x86_64 bin" >nul && (
    echo !FILE! >> "!TMP_DIR!\linux"
    goto :eof
)
echo !FILE! >> "!TMP_DIR!\unknown"
goto :eof
