@echo off
title TalkToMao_Launcher

echo ========================================
echo   TalkToMao - Red Culture AI Dialogue
echo   Starting RAG Dialogue System...
echo ========================================

cd /d "%~dp0"

if not exist "rag_env\Scripts\activate" (
    echo [ERROR] Virtual environment not found.
    echo Please check: rag_env\Scripts\activate
    pause
    exit /b
)

if not exist "app.py" (
    echo [ERROR] app.py not found in current directory.
    pause
    exit /b
)

echo [1/2] Starting Flask backend...
start "TalkToMao_Backend" cmd /k "call rag_env\Scripts\activate && python app.py"

echo Waiting 5 seconds for backend to load...
timeout /t 5 /nobreak >nul

echo [2/2] Opening frontend page...
start "" "http://localhost:5000"

echo ========================================
echo   Launch complete.
echo   Keep the backend window open.
echo   Check backend window for errors.
echo ========================================
pause