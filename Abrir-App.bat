@echo off
cd /d "%~dp0"

REM Intentar ejecutar con pythonw (sin consola). Si no existe, usar python para ver errores.
where pythonw >nul 2>&1
if %ERRORLEVEL%==0 goto use_pythonw
echo pythonw no encontrado en PATH, usando python (ver consola para mensajes)...
start "" python "%~dp0main.py"
goto :eof
:use_pythonw
start "" pythonw "%~dp0main.py"