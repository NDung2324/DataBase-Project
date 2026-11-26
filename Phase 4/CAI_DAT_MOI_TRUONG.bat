@echo off
setlocal
cd /d "%~dp0"
set "PYTHONUTF8=1"
set "PHASE4_PYTHON="
where py >nul 2>nul
if not errorlevel 1 for /f "delims=" %%P in ('py -3 -c "import sys; print(sys.executable)" 2^>nul') do set "PHASE4_PYTHON=%%P"
if defined PHASE4_PYTHON goto setup
for /f "delims=" %%P in ('powershell.exe -NoProfile -Command "$phase4Command=Get-Command python -ErrorAction SilentlyContinue; if($phase4Command -and $phase4Command.Source -notlike '*Microsoft\WindowsApps\python.exe'){ $phase4Command.Source }"') do set "PHASE4_PYTHON=%%P"
if defined PHASE4_PYTHON goto setup
for /f "delims=" %%P in ('powershell.exe -NoProfile -Command "try { $phase4Package=Get-AppxPackage -Name 'OpenAI.CodexPrimaryRuntime*' -ErrorAction Stop | Sort-Object Version -Descending | Select-Object -First 1; if($phase4Package){ $phase4Runtime=Join-Path $phase4Package.InstallLocation 'dependencies\python\python.exe'; if(Test-Path -LiteralPath $phase4Runtime){$phase4Runtime} } } catch {}"') do set "PHASE4_PYTHON=%%P"
if defined PHASE4_PYTHON goto setup
if exist "C:\Program Files\WindowsApps\OpenAI.CodexPrimaryRuntime.v26-1123-915-0_26.1123.915.0_x64__3k8sg7r9htsxt\dependencies\python\python.exe" set "PHASE4_PYTHON=C:\Program Files\WindowsApps\OpenAI.CodexPrimaryRuntime.v26-1123-915-0_26.1123.915.0_x64__3k8sg7r9htsxt\dependencies\python\python.exe"
if defined PHASE4_PYTHON goto setup
echo Chua tim thay Python. Cai Python 3.12 tu https://www.python.org/downloads/windows/
exit /b 1
:setup
echo Dang chuan bi moi truong Python rieng cho project...
if exist ".venv\Scripts\python.exe" (
    "%PHASE4_PYTHON%" -m venv --upgrade .venv
) else (
    "%PHASE4_PYTHON%" -m venv .venv
)
if errorlevel 1 exit /b 1
".venv\Scripts\python.exe" -m pip install -r requirements.txt
if errorlevel 1 exit /b 1
echo Da cai xong. Bam dup CHAY_WEB.bat de mo website.
exit /b 0
