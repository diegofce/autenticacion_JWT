# 🎯 GUÍA PASO A PASO - DESDE CERO HASTA FUNCIONANDO

## Paso 1: Verificar Requisitos Previos ✅

```bash
# Verificar Python 3.8+
python --version

# Verificar pip
pip --version

# Verificar PostgreSQL está corriendo
# En Windows: Services (busca PostgreSQL)
# En Linux: sudo systemctl status postgresql
# En macOS: brew services list
```

---

## Paso 2: Crear y Configurar la Base de Datos 🗄️

### Opción A: Usando psql (línea de comandos)

```bash
# Conectar a PostgreSQL
psql -U postgres

# Dentro de psql:
CREATE DATABASE proyecto_login;
\q
```

### Opción B: Usando pgAdmin (interfaz gráfica)

1. Abrir pgAdmin (http://localhost:5050)
2. Click derecho en "Databases"
3. "Create" > "Database"
4. Nombre: `proyecto_login`
5. Click "Save"

---

## Paso 3: Configurar Variables de Entorno ⚙️

### Paso 3.1: Crear archivo .env

```bash
# En la carpeta proyecto_login
copy .env.example .env

# O en Linux/macOS:
cp .env.example .env
```

### Paso 3.2: Editar el archivo .env

Abrir `.env` con tu editor favorito y llenar:

```env
# BASE DE DATOS
POSTGRES_USER=postgres
POSTGRES_PASSWORD=tu_contraseña_postgres
POSTGRES_DB=proyecto_login
POSTGRES_HOST=localhost
POSTGRES_PORT=5432

# AUTENTICACIÓN
SECRET_KEY=tu_clave_secreta_aqui_minimo_32_caracteres
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

**Para generar SECRET_KEY:**

```bash
# Opción 1: Python
python -c "import secrets; print(secrets.token_urlsafe(32))"

# Opción 2: OpenSSL
openssl rand -base64 32

# Opción 3: Windows PowerShell
[System.Convert]::ToBase64String((Get-Random -Count 32 -InputObject (0..255)))
```

---

## Paso 4: Instalar Dependencias 📦

### Paso 4.1: Crear Virtual Environment

```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Linux/macOS
python3 -m venv venv
source venv/bin/activate
```

Deberías ver `(venv)` al inicio de la línea de comando.

### Paso 4.2: Instalar Paquetes

```bash
pip install -r requirements.txt
```

Esperar a que terminen de instalar todos los paquetes.

---

## Paso 5: Ejecutar la Aplicación 🚀

### Opción A: Windows (Más Fácil)

```bash
# Simplemente hacer doble click en:
run.bat

# Se abrirán automáticamente 2 ventanas:
# - Ventana 1: Backend FastAPI
# - Ventana 2: Frontend Streamlit
```

### Opción B: Linux/macOS

```bash
chmod +x run.sh
./run.sh
```

### Opción C: Manual (2 Terminales)

**Terminal 1 - Backend:**
```bash
# Asegúrate de tener el venv activado
uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

Deberías ver:
```
Uvicorn running on http://127.0.0.1:8000
```

**Terminal 2 - Frontend:**
```bash
# Abre otra terminal en la misma carpeta
# Activa el venv si no está activado
streamlit run streamlit_app.py --server.port=8501
```

Deberías ver:
```
You can now view your Streamlit app in your browser
Local URL: http://localhost:8501
```

---

## Paso 6: Acceder a la Aplicación 🌐

### Frontend (Interfaz Usuario)
```
http://localhost:8501
```

### API Swagger (Documentación Interactiva)
```
http://localhost:8000/docs
```

### API ReDoc (Alternativa)
```
http://localhost:8000/redoc
```

---

## Paso 7: Probar el Sistema 🧪

### En el Frontend (http://localhost:8501)

#### 7.1 Crear Cuenta

1. Ir a pestaña "📝 Registro"
2. Llenar formulario:
   - Usuario: `testuser`
   - Email: `test@example.com`
   - Contraseña: `Test123456`
   - Confirmar: `Test123456`
   - Rol: `user`
3. Click "🚀 Registrarse"
4. Ver mensaje de éxito ✅

#### 7.2 Iniciar Sesión

1. Volver a pestaña "🔐 Login"
2. Ingresar:
   - Usuario: `testuser`
   - Contraseña: `Test123456`
3. Click "✅ Ingresar"
4. Ver dashboard 📊

#### 7.3 Explorar Dashboard

- Ver perfil personal
- Ver información de sesión
- Ver token (enmascarado)
- Cerrar sesión

### En Swagger UI (http://localhost:8000/docs)

1. Hacer click en "POST /auth/register"
2. Click "Try it out"
3. Modificar JSON:
```json
{
  "username": "apiuser",
  "email": "api@example.com",
  "password": "ApiPass123",
  "role": "user"
}
```
4. Click "Execute"
5. Ver respuesta 200 ✅

---

## Paso 8: Solucionar Problemas 🔧

### Error: "could not connect to server"

**Problema:** No puede conectar a PostgreSQL

**Solución:**
1. Verificar que PostgreSQL está corriendo
2. Verificar credenciales en .env
3. Verificar que la database `proyecto_login` existe

```bash
# Verificar desde psql:
psql -U postgres -l
```

### Error: "ModuleNotFoundError: No module named 'streamlit'"

**Problema:** Streamlit no está instalado

**Solución:**
```bash
# Asegurate que venv está activado
pip install streamlit
```

### Error: "Conexión rechazada"

**Problema:** Ports ocupados (8000 o 8501)

**Solución:**
```bash
# Cambiar puertos:
uvicorn main:app --port 8001  # Cambiar a 8001
streamlit run streamlit_app.py --server.port=8502  # Cambiar a 8502
```

### Frontend no carga

**Problema:** Backend no está corriendo

**Solución:**
1. Verificar que Backend está corriendo en Terminal 1
2. Ver mensaje "Uvicorn running..."
3. Reintentar en browser

---

## Paso 9: Crear Usuarios de Prueba ✨

### Método 1: Frontend (Fácil)

1. Ir a http://localhost:8501
2. Click "📝 Crear Nueva Cuenta"
3. Llenar formulario
4. Listo!

### Método 2: API Swagger

1. Ir a http://localhost:8000/docs
2. Abrir "POST /auth/register"
3. Click "Try it out"
4. Modificar JSON y enviar

### Método 3: cURL

```bash
curl -X POST "http://localhost:8000/auth/register" \
  -H "Content-Type: application/json" \
  -d '{
    "username": "newuser",
    "email": "new@example.com",
    "password": "NewPass123",
    "role": "user"
  }'
```

---

## Paso 10: Siguientes Pasos 📚

Ahora que todo funciona:

1. **Explora el código:**
   - Abre `streamlit_app.py` (600+ líneas)
   - Revisa `main.py` (estructura FastAPI)
   - Mira `services/auth_service.py` (lógica)

2. **Lee la documentación:**
   - README.md (guía completa)
   - API_EXAMPLES.md (ejemplos)
   - QUICKSTART.md (referencia rápida)

3. **Experimenta:**
   - Crea más usuarios
   - Prueba roles admin
   - Prueba endpoints en Swagger

4. **Desarrolla:**
   - Agrega nuevos modelos en `models/`
   - Crea nuevos endpoints en `routers/`
   - Agrega nuevas páginas en Streamlit

---

## 📊 Checklist de Verificación

```
[ ] Python 3.8+ instalado
[ ] PostgreSQL corriendo
[ ] Database `proyecto_login` creada
[ ] .env configurado con credenciales
[ ] Virtual environment activado
[ ] Dependencias instaladas (pip install -r requirements.txt)
[ ] Backend corriendo en http://localhost:8000
[ ] Frontend corriendo en http://localhost:8501
[ ] Puedo registrarse en el formulario
[ ] Puedo iniciar sesión
[ ] Puedo ver el dashboard
[ ] Puedo ver mis datos de usuario
[ ] Puedo cerrar sesión
```

---

## 🎉 ¡LISTO!

Si completaste todos los pasos, tu aplicación está:
- ✅ Instalada
- ✅ Configurada
- ✅ Corriendo
- ✅ Probada
- ✅ Lista para usar

**¡Felicidades! 🚀**

Ahora puedes:
- Usar la aplicación
- Estudiar el código
- Expandir funcionalidades
- Desplegar a producción (con ajustes de seguridad)

---

## 📞 Ayuda Rápida

| Problema | Solución |
|----------|----------|
| Token expirado | Volver a iniciar sesión (expira en 30 min) |
| CORS error | Verificar que Backend está en :8000 |
| Port ocupado | Cambiar puerto en comandos |
| BD no conecta | Verificar PostgreSQL y credenciales en .env |
| Módulo no encontrado | Instalar con pip install <nombre> |

---

**¡Disfruta tu aplicación de login segura! 🔐**
