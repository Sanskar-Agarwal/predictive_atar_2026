cd /d %~dp0
echo Pulling from remote branch to check for update
:: Check if git is installed

for /f %%i in ('git rev-parse --abbrev-ref HEAD') do set "current_branch=%%i"
if "%current_branch%"=="usage" (
    echo Current branch is 'usage'.
    echo Stashing change
    git stash
    echo Clearing Stash
    git stash clear
    echo Moving to main
    git checkout main
    echo Downloading the update
    git pull origin main
    git checkout usage
    git merge main
) else (
    echo Current branch is not 'usage'.
    git stash
    git checkout main
    git pull origin main
    git checkout -B usage
)

call :executeAndWait python run.py

echo Script execution completed.
pause
exit /b

:executeAndWait
cd /d %~dp0
%*
if %ERRORLEVEL% neq 0 pause
exit /b
