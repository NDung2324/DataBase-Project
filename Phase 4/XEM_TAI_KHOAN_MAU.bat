@echo off
setlocal
cd /d "%~dp0"
set "PYTHONUTF8=1"
if not exist ".venv\Scripts\python.exe" call CAI_DAT_MOI_TRUONG.bat
if not exist ".venv\Scripts\python.exe" goto done
".venv\Scripts\python.exe" tai_khoan_mau.py
:done
pause
