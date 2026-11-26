@echo off
setlocal
cd /d "%~dp0"
set "PYTHONUTF8=1"
if not exist ".venv\Scripts\python.exe" call CAI_DAT_MOI_TRUONG.bat
if not exist ".venv\Scripts\python.exe" goto done
".venv\Scripts\python.exe" -c "import flask, mysql.connector, dotenv" >nul 2>nul
if errorlevel 1 call CAI_DAT_MOI_TRUONG.bat
".venv\Scripts\python.exe" kiem_tra_database.py
:done
pause
