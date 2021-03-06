@ECHO OFF

>CON ECHO Starting up...
SET TOOLKIT_PATH=%~d0%~p0
SET SCRIPTS_PATH=%TOOLKIT_PATH%Scripts\
SET DIST_PATH=%SCRIPTS_PATH%dist\
SET TOOLKIT_EXE="%DIST_PATH%toolkit.exe"

>CON ECHO toolkit.exe is set at %TOOLKIT_EXE%

SET PATH=%PATH%;%SCRIPTS_PATH%

>CON CALL "%TOOLKIT_PATH%PS_GET_UTILITIES"
IF ERRORLEVEL 1 GOTO utilityError

SET ORIGINAL=%~f1
SET MOD_NAME=%~n1
SET TARGET=%~f1_Converted

>CON ECHO Making "%TARGET%"
ROBOCOPY "%ORIGINAL%" "%TARGET%" /MIR

>CON ECHO Converting "%TARGET%"
PUSHD "%SCRIPTS_PATH%"
%TOOLKIT_EXE% convert_path "%MOD_NAME%" "%TARGET%"
POPD
>CON ECHO Done

GOTO :EOF

:pythonError
>CON ECHO Error finding Python path
GOTO :EOF

:utilityError
>CON ECHO There was an error finding a 3rd-party tool.  Aborting.
PAUSE
GOTO :EOF
