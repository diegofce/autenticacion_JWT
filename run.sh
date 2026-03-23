#!/bin/bash

# ==========================================
# Script para ejecutar Backend y Frontend
# Linux/macOS
# ==========================================

echo ""
echo "╔════════════════════════════════════════╗"
echo "║  Sistema de Login Seguro - FastAPI    ║"
echo "║  Backend: http://localhost:8000/docs  ║"
echo "║  Frontend: http://localhost:8501      ║"
echo "╚════════════════════════════════════════╝"
echo ""

# Obtener la ruta del script
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
cd "$SCRIPT_DIR"

# Verificar si virtual environment existe
if [ ! -d "venv" ]; then
    echo "[!] Virtual environment no encontrado"
    echo "[*] Creando virtual environment..."
    python3 -m venv venv
fi

# Activar virtual environment
echo "[*] Activando virtual environment..."
source venv/bin/activate

# Verificar si .env existe
if [ ! -f ".env" ]; then
    echo "[!] Archivo .env no encontrado"
    echo "[*] Copiando .env.example a .env..."
    cp .env.example .env
    echo "[!] Por favor, configura las variables en .env antes de continuar"
    read -p "Presiona ENTER para continuar..."
fi

# Instalar dependencias si requirements.txt existe
if [ -f "requirements.txt" ]; then
    echo "[*] Verificando dependencias..."
    pip install -q -r requirements.txt
fi

# Iniciar Backend y Frontend en background
echo "[*] Iniciando Backend (FastAPI)..."
uvicorn main:app --host 0.0.0.0 --port 8000 --reload &
BACKEND_PID=$!

# Esperar 2 segundos para que inicie el backend
sleep 2

echo "[*] Iniciando Frontend (Streamlit)..."
streamlit run streamlit_app.py --server.port=8501 &
FRONTEND_PID=$!

echo ""
echo "[✓] Ambas aplicaciones se están iniciando..."
echo ""
echo "URLs:"
echo "  - Backend (FastAPI):     http://localhost:8000/docs"
echo "  - Frontend (Streamlit):  http://localhost:8501"
echo ""
echo "Para detener las aplicaciones, presiona Ctrl+C"
echo ""

# Mantener el script corriendo
wait
