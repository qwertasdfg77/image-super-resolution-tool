#define AppName "图片超分辨率工具"
#define AppVersion "1.0.2"
#define AppPublisher "qwertasdfg77"
#define AppURL "https://github.com/qwertasdfg77/image-super-resolution-tool"

[Setup]
AppId={{8F5393E3-15DD-4B52-A7B4-648720175B10}
AppName={#AppName}
AppVersion={#AppVersion}
AppPublisher={#AppPublisher}
AppPublisherURL={#AppURL}
AppSupportURL={#AppURL}/issues
AppUpdatesURL={#AppURL}/releases
DefaultDirName={localappdata}\Programs\ImageSuperResolutionTool
DefaultGroupName={#AppName}
DisableProgramGroupPage=no
OutputDir=output
OutputBaseFilename=ImageSuperResolutionToolWebSetup
Compression=lzma2
SolidCompression=yes
WizardStyle=modern
PrivilegesRequired=lowest
ArchitecturesAllowed=x64compatible
ArchitecturesInstallIn64BitMode=x64compatible
UninstallDisplayName={#AppName}

[Tasks]
Name: "desktopicon"; Description: "创建桌面快捷方式"; GroupDescription: "快捷方式："; Flags: checkedonce

[Files]
Source: "..\install-from-github.ps1"; DestDir: "{app}\installer"; Flags: ignoreversion

[Run]
Filename: "powershell.exe"; Parameters: "-NoProfile -ExecutionPolicy Bypass -File ""{app}\installer\install-from-github.ps1"" -InstallDir ""{app}"" -SkipShortcut"; StatusMsg: "正在下载并安装完整程序，请耐心等待..."; Flags: waituntilterminated

[Icons]
Name: "{group}\图片超分辨率工具"; Filename: "{app}\start_gui.bat"; WorkingDir: "{app}"
Name: "{group}\卸载图片超分辨率工具"; Filename: "{uninstallexe}"
Name: "{autodesktop}\图片超分辨率工具"; Filename: "{app}\start_gui.bat"; WorkingDir: "{app}"; Tasks: desktopicon

[UninstallDelete]
Type: filesandordirs; Name: "{app}"
