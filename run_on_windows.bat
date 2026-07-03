:: Check if running as Administrator
net session >nul 2>&1
if %errorlevel% == 0 (
    echo Running with administrative privileges
) else (
    echo This script requires administrative privileges.
    echo Please right-click the batch file and select 'Run as administrator'.
    pause
    exit /b
)

SET "SCRIPT_PATH=%~dp0"

:: Check if Chocolatey is installed
where choco >nul 2>&1
if %errorlevel% neq 0 (
    echo Installing Chocolatey...
    PowerShell -Command "Set-ExecutionPolicy Bypass -Scope Process -Force; [System.Net.ServicePointManager]::SecurityProtocol = [System.Net.ServicePointManager]::SecurityProtocol -bor 3072; iex ((New-Object System.Net.WebClient).DownloadString('https://chocolatey.org/install.ps1'))"
    SET "CHOCO_PATH=C:\ProgramData\chocolatey\bin"
    SET "PATH=%CHOCO_PATH%;%PATH%"
    powershell -Command "Start-Process '%~dpnx0' -Verb RunAs"
    exit /b
) else (
    echo Chocolatey is already installed.
)

call :executeAndWait choco install git -y
call :executeAndWait choco install python -y
call :executeAndWait choco install nodejs -y

:: Uncomment the following lines if you want to run a Python script
cd /d "%SCRIPT_PATH%"
set "filename=boot.bat"
set "fullpath=%SCRIPT_PATH%%filename%"
explorer "%fullpath%"
echo Pulling from remote branch to check for update
pause

:executeAndWait
%*
if %ERRORLEVEL% neq 0 pause
exit /b
