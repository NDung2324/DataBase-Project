@echo off
setlocal
cd /d "%~dp0"
set "PYTHONUTF8=1"
if not exist ".env" (
    copy /y ".env.example" ".env" >nul
    echo Da tao file .env. Bam MO_CAU_HINH.bat de dien mat khau MySQL roi chay lai.
    goto failed
)
if not exist ".venv\Scripts\python.exe" call CAI_DAT_MOI_TRUONG.bat
if not exist ".venv\Scripts\python.exe" goto failed
".venv\Scripts\python.exe" -c "import flask, mysql.connector, dotenv" >nul 2>nul
if errorlevel 1 call CAI_DAT_MOI_TRUONG.bat
".venv\Scripts\python.exe" run_local.py
if errorlevel 1 goto failed
pause
exit /b 0
:failed
echo.
echo Chua chay duoc web. Xem thong bao phia tren.
echo File cau hinh MySQL: .env
pause
exit /b 1
