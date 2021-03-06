@ECHO OFF

SETLOCAL

SET TOOLKIT_PATH=%~d0%~p0
SET SCRIPTS_PATH=%TOOLKIT_PATH%Scripts\
SET TOOLKIT_PY="%SCRIPTS_PATH%toolkit.py"
SET PRISTINE=%TOOLKIT_PATH%DefaultIniFiles

SET ORIGINAL=%~f1
SET TARGET=%~f2
SET LOAD_ORDER=%3

SET PATH=%PATH%;%SCRIPTS_PATH%

>CON ECHO Starting up...

>CON ECHO toolkit.py is set at %TOOLKIT_PY%

>CON ECHO Finding Python 3.x path
>CON CALL "%SCRIPTS_PATH%FIND_PYTHON_PATH"
IF ERRORLEVEL 1 GOTO pythonError

>CON ECHO Found Python 3.x path

ROBOCOPY "%PRISTINE%" "%TARGET%" /MIR /XF .gitignore

"%PYTHON3%" %TOOLKIT_PY% load_order "%ORIGINAL%" "%TARGET%" %LOAD_ORDER%

GOTO :EOF

:pythonError
>CON ECHO Error finding Python path