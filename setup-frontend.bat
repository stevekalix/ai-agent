@echo off
REM ============================================================
REM AI Agent System - Run Backend & Frontend Together
REM ============================================================

echo.
echo ====================================================
echo  AI Agent System - Full Stack Runner
echo ====================================================
echo.

REM Check if Node.js is installed
where node >nul 2>nul
if %errorlevel% neq 0 (
    echo ERROR: Node.js is not installed!
    echo Download from: https://nodejs.org/
    echo.
    pause
    exit /b 1
)

echo ✅ Node.js found
echo.

REM Check if backend venv exists
if not exist "venv" (
    echo Creating Python virtual environment...
    python -m venv venv
    echo.
)

REM Activate venv
echo Activating Python virtual environment...
call venv\Scripts\activate.bat

echo.
echo ✅ Backend environment ready
echo.

REM Install/update frontend dependencies
cd frontend
echo Installing frontend dependencies...
if not exist "node_modules" (
    call npm install
) else (
    echo Frontend dependencies already installed
)

cd ..
echo.
echo ====================================================
echo  SETUP COMPLETE! Ready to run
echo ====================================================
echo.
echo To start both frontend and backend:
echo.
echo 1. Open TWO separate terminals
echo.
echo Terminal 1 (Backend):
echo   cd E:\Vibe-Coding-AI\Ai-Agent
echo   python startup.py
echo.
echo Terminal 2 (Frontend):
echo   cd E:\Vibe-Coding-AI\Ai-Agent\frontend
echo   npm start
echo.
echo Then visit: http://localhost:3000
echo.
echo ====================================================
echo.
pause

