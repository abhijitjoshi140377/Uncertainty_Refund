@echo off
echo ========================================
echo Travel Refund Uncertainty Estimation
echo Starting Application...
echo ========================================
echo.

echo [1/2] Starting Backend Server...
start "Backend Server" cmd /k "cd backend && venv\Scripts\activate && python main.py"

echo Waiting for backend to initialize...
timeout /t 8 /nobreak >nul

echo [2/2] Starting Frontend Server...
start "Frontend Server" cmd /k "cd frontend && npm run dev"

echo.
echo ========================================
echo Application Started Successfully!
echo ========================================
echo.
echo Backend API: http://localhost:8000
echo API Docs: http://localhost:8000/api/docs
echo Frontend: http://localhost:3000
echo.
echo Press any key to exit this window...
pause >nul

@REM Made with Bob
