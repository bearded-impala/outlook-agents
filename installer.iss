[Setup]
AppName=Outlook Agents
AppVersion=1.0
DefaultDirName={pf}\OutlookAgents
DefaultGroupName=OutlookAgents
OutputDir=dist
OutputBaseFilename=OutlookAgentsInstaller
SetupIconFile=src\app.ico
Compression=lzma
SolidCompression=yes

[Files]
Source: "dist\main.exe"; DestDir: "{app}"; Flags: ignoreversion

[Icons]
Name: "{group}\Outlook Agents"; Filename: "{app}\main.exe"; IconFilename: "src\app.ico"
Name: "{commondesktop}\Outlook Agents"; Filename: "{app}\main.exe"; IconFilename: "src\app.ico"; Tasks: desktopicon

[Run]
Filename: "{app}\main.exe"; Description: "Run Outlook Agent"; Flags: nowait postinstall skipifsilent

[Tasks]
Name: "desktopicon"; Description: "Create a desktop icon"; GroupDescription: "Additional icons:"; Flags: unchecked

[Code]
procedure CurStepChanged(CurStep: TSetupStep);
var
  TaskName, AppPath: string;
  ResultCode: Integer;
begin
  if CurStep = ssPostInstall then begin
    TaskName := 'OutlookAgentAutoStart';
    AppPath := ExpandConstant('{app}\main.exe');
    ShellExec('open', 'schtasks.exe', 
      '/Create /SC ONLOGON /TN "' + TaskName + '" /TR "' + AppPath + '" /RL HIGHEST /F',
      '', SW_HIDE, ewWaitUntilTerminated, ResultCode);
  end;
end;

[UninstallRun]
Filename: "schtasks.exe"; Parameters: "/Delete /TN OutlookAgentAutoStart /F"; Flags: runhidden
