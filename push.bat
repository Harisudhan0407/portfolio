@echo off
echo ========================================
echo GitHub Repository Updater
echo ========================================
echo.
echo The following files have been modified:
git status -s
echo.

set /p "confirm=Do you want to commit and push these changes to GitHub? (Y/N): "
if /I "%confirm%" neq "Y" (
    echo.
    echo Push cancelled. Your files were not modified, but nothing was sent to GitHub.
    pause
    exit /b
)

echo.
set /p "msg=Enter a commit message (or press enter for default): "
if "%msg%"=="" set "msg=Apply latest updates"

echo.
echo Adding changes...
git add .
echo Committing changes...
git commit -m "%msg%"
echo Pushing to GitHub...
git push
echo.
echo Done! Successfully pushed to GitHub.
pause
