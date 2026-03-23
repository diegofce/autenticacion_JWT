# 🔐 Sistema de Login Seguro - Proyecto Completo

Sistema de autenticación y autorización con roles basado en **FastAPI** (backend) y **Streamlit** (frontend).

## 📋 Características

### ✅ Backend (FastAPI)
- Registro de usuarios con validación completa
- Login con generación de JWT tokens
- Autenticación OAuth2
- Control de acceso basado en roles (RBAC)
- Contraseñas hasheadas con bcrypt
- Logging automático con rotación
- Base de datos PostgreSQL con SQLAlchemy ORM

### ✅ Frontend (Streamlit)
- Interfaz moderna y responsive
- Página de login intuitiva
- Página de registro con validaciones
- Dashboard personalizado por rol
- Panel de administrador
- Visualización segura del token (enmascarado)
- Gestión de sesión automática

## 🛠️ Requisitos Previos

- Python 3.8+
- PostgreSQL 12+
- Git

## ☁️ Preparar para GitHub (sin datos sensibles)

Antes de hacer `git add .`:

- Usa `.env.example` como plantilla y mantén `.env` solo local (ya está ignorado en `.gitignore`).
- Nunca subas credenciales reales, tokens, claves privadas ni logs.
- Verifica que `venv/`, `logs/`, `__pycache__/` y archivos temporales estén ignorados.

Si ya agregaste secretos por error al staging, límpialos antes del commit:

```bash
git restore --staged .env
git restore --staged logs/app.log
```

## 📦 Instalación

### 1. Clonar o descargar el proyecto
```bash
cd proyecto_login
```

### 2. Crear virtual environment
```bash
python -m venv venv

# En Windows
venv\Scripts\activate

# En Linux/macOS
source venv/bin/activate
```

### 3. Instalar dependencias
```bash
pip install -r requirements.txt
```

### 4. Configurar variables de entorno

Copiar el archivo `.env.example` a `.env`:
```bash
cp .env.example .env
```

Editar `.env` con tus valores:
```env
# BASE DE DATOS
POSTGRES_USER=postgres
POSTGRES_PASSWORD=tu_contraseña
POSTGRES_DB=proyecto_login
POSTGRES_HOST=localhost
POSTGRES_PORT=5432

# SEGURIDAD
SECRET_KEY=tu_clave_super_secreta_aqui_minimo_32_caracteres
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

### 5. Crear base de datos PostgreSQL
```bash
# Conectar a PostgreSQL
psql -U postgres

# Crear database
CREATE DATABASE proyecto_login;

# Salir
\q
```

## 🚀 Ejecutar la Aplicación

### Opción 1: Ejecutar Backend y Frontend por separado

**Terminal 1 - Backend (FastAPI)**
```bash
# En la carpeta del proyecto
uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

**Terminal 2 - Frontend (Streamlit)**
```bash
# En la carpeta del proyecto
streamlit run streamlit_app.py --server.port=8501
```

Luego acceder a:
- **Frontend Streamlit:** http://localhost:8501
- **API Swagger UI:** http://localhost:8000/docs
- **API ReDoc:** http://localhost:8000/redoc

### Opción 2: Usar script de ejecución (Windows)

Crear archivo `run.bat`:
```batch
@echo off
echo Iniciando Backend y Frontend...
start "Backend FastAPI" cmd /k "venv\Scripts\activate && uvicorn main:app --reload"
timeout /t 2
start "Frontend Streamlit" cmd /k "venv\Scripts\activate && streamlit run streamlit_app.py"
```

Ejecutar:
```bash
run.bat
```

## 👥 Usuarios de Prueba

Estos usuarios se crean automáticamente en la primera ejecución del backend (si no existen):

### Usuario Regular
```
Usuario: user1
Email: user1@example.com
Contraseña: password123
Rol: user
```

### Administrador
```
Usuario: admin1
Email: admin1@example.com
Contraseña: adminpass123
Rol: admin
```

### Para crear más usuarios:
1. Ir a http://localhost:8501
2. Click en "📝 Crear Nueva Cuenta"
3. Rellenar formulario

## 📁 Estructura del Proyecto

```
proyecto_login/
├── main.py                      # Punto de entrada FastAPI
├── streamlit_app.py             # Frontend Streamlit
├── requirements.txt             # Dependencias Python
├── .env.example                 # Plantilla de configuración
│
├── core/
│   ├── config.py               # Configuración central
│   ├── logger.py               # Sistema de logging
│   └── __init__.py
│
├── database/
│   ├── session.py              # Conexión a PostgreSQL
│   └── __init__.py
│
├── models/
│   ├── user_task.py            # Modelo ORM User
│   └── __init__.py
│
├── routers/
│   ├── auth_routers.py         # Endpoints /auth
│   └── __init__.py
│
├── schemas/
│   ├── user_task.py            # Esquemas Pydantic
│   └── __init__.py
│
├── services/
│   ├── auth_service.py         # Lógica de autenticación
│   ├── task_service.py         # Lógica de tareas
│   └── __init__.py
│
└── logs/                        # Archivos de log (auto-generado)
```

## 🔐 Seguridad

### Implementado:
- ✅ Hashing de contraseñas con **bcrypt**
- ✅ Tokens JWT con expiración de 30 minutos
- ✅ OAuth2 con Password Bearer
- ✅ CORS habilitado para frontend local
- ✅ Validación de datos con Pydantic
- ✅ Control de acceso por rol

### Para Producción:
- Usar HTTPS/SSL en lugar de HTTP
- Cambiar `SECRET_KEY` por valor aleatorio fuerte
- Habilitar CORS específicamente para tu dominio
- Usar `.env` en archivo seguro (no en el repo)
- Cambiar contraseñas de base de datos por defecto
- Implementar rate limiting

## 📚 API Endpoints

### Autenticación

#### Registrar usuario
```http
POST /auth/register
Content-Type: application/json

{
  "username": "newuser",
  "email": "newuser@example.com",
  "password": "securepass123",
  "role": "user"
}
```

#### Login
```http
POST /auth/login
Content-Type: application/x-www-form-urlencoded

username=user1&password=password123
```

**Respuesta:**
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer"
}
```

#### Obtener datos del usuario
```http
GET /auth/me
Authorization: Bearer <token>
```

#### Acceso solo admin
```http
GET /auth/admin-only
Authorization: Bearer <token>
```

## 🧪 Testing

### Con cURL
```bash
# Registrar usuario
curl -X POST "http://localhost:8000/auth/register" \
  -H "Content-Type: application/json" \
  -d '{"username":"testuser","email":"test@test.com","password":"pass123","role":"user"}'

# Login
curl -X POST "http://localhost:8000/auth/login" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "username=testuser&password=pass123"

# Obtener usuario actual
curl -X GET "http://localhost:8000/auth/me" \
  -H "Authorization: Bearer YOUR_TOKEN_HERE"
```

### Con Python
```python
import requests

# Login
response = requests.post(
    "http://localhost:8000/auth/login",
    data={"username": "user1", "password": "password123"}
)
token = response.json()["access_token"]

# Obtener usuario
headers = {"Authorization": f"Bearer {token}"}
user = requests.get("http://localhost:8000/auth/me", headers=headers).json()
print(user)
```

### Con Swagger UI
1. Ir a http://localhost:8000/docs
2. Click en "Try it out" en los endpoints
3. Ingresar datos y ejecutar

## ⚙️ Configuración importante

- `DATABASE_URL` puede definirse directamente en `.env`.
- Si no se define `DATABASE_URL`, la app la construye con:
  `POSTGRES_USER`, `POSTGRES_PASSWORD`, `POSTGRES_DB`, `POSTGRES_HOST`, `POSTGRES_PORT`.
- En frontend puedes sobrescribir la API con `API_BASE_URL` (por defecto: `http://localhost:8000`).

## 🐛 Troubleshooting

### "Connection refused" al conectar a la BD
```
Error: psycopg2.OperationalError: could not connect to server
```
**Solución:**
- Verificar que PostgreSQL está corriendo
- Verificar credenciales en `.env`
- Verificar host y puerto

### "Token inválido o expirado"
**Solución:**
- El token expira en 30 minutos, hacer login nuevamente
- Verificar que estás usando el token correcto

### "CORS error en el navegador"
**Solución:**
- El backend debe estar corriendo en http://localhost:8000
- Streamlit en http://localhost:8501

### Streamlit no encuentra el módulo requests
```
ModuleNotFoundError: No module named 'requests'
```
**Solución:**
```bash
pip install requests
```

## 📝 Próximas Mejoras

- [ ] Recuperación de contraseña
- [ ] Confirmación de email
- [ ] Autenticación de 2 factores (2FA)
- [ ] Gestión de usuarios en panel admin
- [ ] Registro de actividades (audit log)
- [ ] Despliegue a servidor remoto (Heroku, AWS)
- [ ] Tests automatizados (pytest)
- [ ] Documentación en Swagger mejorada

## 📄 Licencia

Este proyecto es de código abierto y disponible bajo licencia MIT.

## 👨‍💻 Contribuciones

Las contribuciones son bienvenidas. Para cambios importantes, abre primero un issue para discutir qué te gustaría cambiar.

## 📧 Soporte

Para preguntas o problemas:
1. Revisa el apartado Troubleshooting
2. Abre un issue en el repositorio
3. Contacta al equipo de desarrollo

---

**Hecho con ❤️ usando FastAPI + Streamlit + PostgreSQL**
