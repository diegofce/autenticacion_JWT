@echo off
REM ==========================================
REM Script para ejecutar Backend y Frontend
REM ==========================================

setlocal enabledelayedexpansion

echo.
echo ╔════════════════════════════════════════╗
echo ║  Sistema de Login Seguro - FastAPI    ║
echo ║  Backend: http://localhost:8000/docs  ║
echo ║  Frontend: http://localhost:8501      ║
echo ╚════════════════════════════════════════╝
echo.

REM Verificar si virtual environment existe
if not exist "venv" (
    echo [!] Virtual environment no encontrado
    echo [*] Creando virtual environment...
    python -m venv venv
)

REM Activar virtual environment
echo [*] Activando virtual environment...
call venv\Scripts\activate.bat

REM Verificar si .env existe
if not exist ".env" (
    echo [!] Archivo .env no encontrado
    echo [*] Copiando .env.example a .env...
    copy .env.example .env
    echo [!] Por favor, configura las variables en .env antes de continuar
    pause
)

REM Iniciar Backend y Frontend en ventanas separadas
echo [*] Iniciando Backend (FastAPI)...
start "Backend FastAPI" cmd /k "venv\Scripts\activate.bat && uvicorn main:app --host 0.0.0.0 --port 8000 --reload"

REM Esperar 2 segundos para que inicie el backend
timeout /t 2 /nobreak

echo [*] Iniciando Frontend (Streamlit)...
start "Frontend Streamlit" cmd /k "venv\Scripts\activate.bat && streamlit run streamlit_app.py --server.port=8501"

echo.
echo [✓] Ambas aplicaciones se están iniciando...
echo.
echo URLs:
echo   - Backend (FastAPI):  http://localhost:8000/docs
echo   - Frontend (Streamlit): http://localhost:8501
echo.
echo Presiona cualquier tecla para cerrar esta ventana...
pause

endlocal
