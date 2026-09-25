@echo off
setlocal
cd /d "%~dp0"
where py >nul 2>&1
if %ERRORLEVEL%==0 (
  py -3 setup.py %*
  exit /b %ERRORLEVEL%
)
where python >nul 2>&1
if %ERRORLEVEL%==0 (
  python setup.py %*
  exit /b %ERRORLEVEL%
)
echo Python 3 not found. Install from https://www.python.org/downloads/ and retry.
exit /b 1
