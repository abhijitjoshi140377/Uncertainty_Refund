@echo off
echo ========================================
echo MCP Server for Refund Estimation System
echo ========================================
echo.

REM Check if virtual environment exists
if not exist "venv\" (
    echo Creating virtual environment...
    python -m venv venv
    echo.
)

REM Activate virtual environment
echo Activating virtual environment...
call venv\Scripts\activate
echo.

REM Install dependencies
echo Installing dependencies...
pip install -r requirements.txt
echo.

REM Check if FastAPI backend is running
echo Checking if FastAPI backend is running...
curl -s http://localhost:8000/api/health >nul 2>&1
if %errorlevel% neq 0 (
    echo.
    echo WARNING: FastAPI backend is not running!
    echo Please start the backend first:
    echo   cd backend
    echo   python main.py
    echo.
    pause
    exit /b 1
)

echo Backend is running!
echo.

REM Start MCP server
echo Starting MCP Server...
echo.
python refund_mcp_server.py

pause

@REM Made with Bob
