@echo off
cd /d "%~dp0"
where py >nul 2>nul
if errorlevel 1 (
  python patcher.py %*
) else (
  py -3 patcher.py %*
)
echo.
echo Python 3.10 or newer is required. See README.md.
pause
