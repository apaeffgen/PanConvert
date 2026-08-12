; Inno Setup script for Panconvert
; Build command: iscc.exe Panconvert.iss
; Run from: packaging/windows/ directory

#define MyAppName "Panconvert"
#define MyAppVersion "0.3.1"
#define MyAppPublisher "APaeffgen"
#define MyAppURL "https://github.com/apaeffgen/PanConvert"
#define MyAppExeName "Panconvert.exe"
#define MyAppId "A3B5C7D9-1234-5678-90AB-CDEF12345678"

[Setup]
; NOTE: The value of AppId uniquely identifies this application.
AppId={#MyAppId}
AppName={#MyAppName}
AppVersion={#MyAppVersion}
AppPublisher={#MyAppPublisher}
AppPublisherURL={#MyAppURL}
AppSupportURL={#MyAppURL}
AppUpdatesURL={#MyAppURL}
DefaultDirName={autopf}\{#MyAppName}
DefaultGroupName={#MyAppName}
OutputDir=..\..\dist
OutputBaseFilename=Panconvert-{#MyAppVersion}-win64-installer
Compression=lzma2
SolidCompression=yes
WizardStyle=modern
ArchitecturesAllowed=x64compatible
ArchitecturesInstallIn64BitMode=x64compatible
PrivilegesRequired=lowest
VersionInfoVersion={#MyAppVersion}
VersionInfoCompany={#MyAppPublisher}
VersionInfoDescription={#MyAppName} Converter

[Languages]
Name: "english"; MessagesFile: "compiler:Default.isl"

[Tasks]
Name: "desktopicon"; Description: "{cm:CreateDesktopIcon}"; GroupDescription: "{cm:AdditionalIcons}"; Flags: unchecked
Name: "quicklaunchicon"; Description: "{cm:CreateQuickLaunchIcon}"; GroupDescription: "{cm:AdditionalIcons}"; Flags: unchecked

[Files]
; Include all files from the PyInstaller dist folder
; Note: PyInstaller builds a single-file exe with all dependencies bundled inside
Source: "..\..\dist\Panconvert.exe"; DestDir: "{app}"; Flags: ignoreversion
; Include bundled pandoc binary
Source: "pandoc.exe"; DestDir: "{app}"; Flags: ignoreversion
; Include source files if needed (uncomment to distribute source code)
; Source: "..\..\source\*"; DestDir: "{app}\source"; Flags: ignoreversion recursesubdirs

[Icons]
Name: "{group}\{#MyAppName}"; Filename: "{app}\{#MyAppExeName}"
Name: "{group}\{cm:UninstallProgram,{#MyAppName}}"; Filename: "{uninstallexe}"
Name: "{autodesktop}\{#MyAppName}"; Filename: "{app}\{#MyAppExeName}"; Tasks: desktopicon
Name: "{userappdata}\Microsoft\Internet Explorer\Quick Launch\{#MyAppName}"; Filename: "{app}\{#MyAppExeName}"; Tasks: quicklaunchicon

[Run]
Filename: "{app}\{#MyAppExeName}"; Description: "{cm:LaunchProgram,{#StringChange(MyAppName, '&', '&&')}}"; Flags: nowait postinstall skipifsilent

[UninstallDelete]
; Clean up leftover config on uninstall (optional)
; Type: files; Name: "{app}\*"
