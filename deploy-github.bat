@echo off
setlocal enabledelayedexpansion

rem =========================================================
rem  Working Mate - Deploy website to GitHub Pages
rem  Run this by DOUBLE CLICKING. Git for Windows required.
rem =========================================================

set "GIT=C:\Program Files\Git\cmd\git.exe"
set "REMOTE=https://github.com/Frederic-123-cell/working-mate.git"
set "EMAIL=wanjunjie13341418310@outlook.com"
set "USERNAME=Frederic-123-cell"

echo.
echo ============================================
echo   Working Mate  --  GitHub Pages Deploy
echo ============================================
echo.
echo   Repo : %REMOTE%
echo   Pages: https://frederic-123-cell.github.io/working-mate/
echo.

if not exist "%GIT%" (
    echo [ERROR] Git for Windows not found:
    echo         %GIT%
    echo.
    echo Install it from https://git-scm.com/ then run this again.
    echo.
    pause
    exit /b 1
)

cd /d "%~dp0"

echo [1/6] Checking remote repo exists...
"%GIT%" ls-remote "%REMOTE%" HEAD >nul 2>&1
if errorlevel 1 (
    echo.
    echo [STOP] Cannot reach the remote repo.
    echo.
    echo   Please create it first on GitHub:
    echo     https://github.com/new
    echo       Repository name : working-mate
    echo       Visibility      : Public   ^(required for free GitHub Pages^)
    echo       Do NOT check    : Add a README / .gitignore / license
    echo.
    echo   Then run this script again.
    echo.
    pause
    exit /b 1
)
echo       OK, remote reachable.
echo.

echo [2/6] git init...
if not exist ".git" (
    "%GIT%" init -b main
) else (
    echo       .git already exists, skipping init.
)
echo.

echo [3/6] Setting remote...
"%GIT%" remote remove origin >nul 2>&1
"%GIT%" remote add origin "%REMOTE%"
echo       origin = %REMOTE%
echo.

echo [4/6] Staging files ^(240MB installer excluded via .gitignore^)...
"%GIT%" add -A
echo.

echo [5/6] Committing...
"%GIT%" -c user.email="%EMAIL%" -c user.name="%USERNAME%" commit -m "Deploy website: Creem compliance (AUP + support email + Qiniu provider)" 2>&1
echo.

echo [6/6] Pushing to GitHub...
"%GIT%" push -u origin main
if errorlevel 1 (
    echo.
    echo [FAILED] Push did not succeed.
    echo.
    echo   Common fixes:
    echo     - Not logged in to GitHub in this shell.
    echo       Fix: open GitHub Desktop once and sign in, then retry.
    echo     - Branch is 'master' not 'main'. Run:
    echo       "%GIT%" branch -M main
    echo       "%GIT%" push -u origin main
    echo.
    pause
    exit /b 1
)

echo.
echo ============================================
echo   SUCCESS
echo ============================================
echo.
echo   Next steps ^(do these once, in the browser^):
echo.
echo   1. Enable Pages
echo      https://github.com/Frederic-123-cell/working-mate/settings/pages
echo      Source  : Deploy from a branch
echo      Branch  : main   /root   --^> Save
echo      Wait ~1 min, then open:
echo      https://frederic-123-cell.github.io/working-mate/
echo.
echo   2. Upload the 240MB installer to Releases
echo      https://github.com/Frederic-123-cell/working-mate/releases/new
echo        Tag version   : v1.2.6
echo        Release title : Working Mate v1.2.6
echo        Attach file   : downloads\AIAgent-Setup-1.2.6.exe
echo        --^> Publish release
echo.
echo      Then verify the auto-update link works:
echo      https://github.com/Frederic-123-cell/working-mate/releases/download/v1.2.6/AIAgent-Setup-1.2.6.exe
echo.
pause
