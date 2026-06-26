#define MyAppName "VisionX"
#define MyAppVersion "1.0"
#define MyAppExeName "HMELVision.exe"



; ===============================
; SETUP
; ===============================

[Setup]

AppId={{A7F38C2D-91E8-4A3D-9F4A-VISIONX01}

AppName={#MyAppName}

AppVersion={#MyAppVersion}

AppPublisher=VisionX

DefaultDirName={autopf}\VisionX

DefaultGroupName={#MyAppName}

DisableProgramGroupPage=yes

OutputDir=Output

OutputBaseFilename=VisionXSetup

Compression=lzma2

SolidCompression=yes

WizardStyle=modern

PrivilegesRequired=admin

UninstallDisplayName=VisionX Platform





; ===============================
; LANGUAGE
; ===============================

[Languages]

Name: "english"; MessagesFile: "compiler:Default.isl"






; ===============================
; TASKS
; ===============================

[Tasks]

Name: "desktopicon"; \
Description: "Create Desktop Shortcut"; \
GroupDescription: "Additional icons:"; \
Flags: unchecked








; ===============================
; FILES
; ===============================

[Files]


; VisionX application

Source: "VisionX\*"; \
DestDir: "{app}"; \
Flags: ignoreversion recursesubdirs createallsubdirs





; PostgreSQL installer

Source: "postgresql-18.4-1-windows-x64.exe"; \
DestDir: "{tmp}"; \
Flags: deleteafterinstall









; ===============================
; SHORTCUTS
; ===============================

[Icons]


Name: "{group}\VisionX"; \
Filename: "{app}\{#MyAppExeName}"



Name: "{commondesktop}\VisionX"; \
Filename: "{app}\{#MyAppExeName}"; \
Tasks: desktopicon









; ===============================
; RUN
; ===============================

[Run]



; Install PostgreSQL

Filename: "{tmp}\postgresql-18.4-1-windows-x64.exe"; \
Parameters: "--mode unattended --unattendedmodeui none --superpassword 14232517 --servicename postgresql-x64-18 --serverport 5432 --prefix ""C:\Program Files\PostgreSQL\18"" --datadir ""C:\Program Files\PostgreSQL\18\data"""; \
StatusMsg: "Installing PostgreSQL..."; \
Check: NeedsPostgres; \
Flags: waituntilterminated






; Start PostgreSQL service

Filename: "{sys}\net.exe"; \
Parameters: "start postgresql-x64-18"; \
StatusMsg: "Starting PostgreSQL Service..."; \
Flags: runhidden waituntilterminated







; Start VisionX

Filename: "{app}\{#MyAppExeName}"; \
Description: "Launch VisionX"; \
Flags: nowait postinstall skipifsilent










; ===============================
; CLEANUP
; ===============================

[UninstallDelete]


Type: files; Name: "{app}\_internal\storage_config.txt"









; ===============================
; CODE
; ===============================

[Code]


var

    StoragePage: TInputDirWizardPage;










// ------------------------------
// Storage selection page
// ------------------------------

procedure InitializeWizard();


begin



    StoragePage :=

        CreateInputDirPage(

            wpSelectDir,

            'VisionX Storage Location',

            'Choose VisionX AI Storage Folder',

            'Select where models, evidence images and events will be stored.',

            False,

            ''

        );






    StoragePage.Add(

        'Storage Folder:'

    );







    StoragePage.Values[0] :=

        ExpandConstant(

            '{commonappdata}\VisionXStorage'

        );



end;











// ------------------------------
// Create storage folders
// ------------------------------

procedure CurStepChanged(

    CurStep: TSetupStep

);



begin



    if CurStep = ssPostInstall then



    begin





        SaveStringToFile(

            ExpandConstant(

                '{app}\_internal\storage_config.txt'

            ),


            StoragePage.Values[0] + #13#10,


            False

        );








        ForceDirectories(

            StoragePage.Values[0] + '\models'

        );




        ForceDirectories(

            StoragePage.Values[0] + '\evidence'

        );




        ForceDirectories(

            StoragePage.Values[0] + '\events'

        );




    end;



end;











// ------------------------------
// PostgreSQL detection
// ------------------------------

function NeedsPostgres(): Boolean;


var

    ResultCode: Integer;



begin



    Exec(

        'cmd.exe',

        '/C sc query postgresql-x64-18',

        '',

        SW_HIDE,

        ewWaitUntilTerminated,

        ResultCode

    );






    if ResultCode = 0 then


        Result := False


    else


        Result := True;



end;