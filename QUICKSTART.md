# 📋 GUÍA RÁPIDA DE CONFIGURACIÓN

## ✅ Checklist de Setup Inicial

### 1️⃣ Configurar Base de Datos PostgreSQL
```
[ ] PostgreSQL instalado y corriendo
[ ] Crear base de datos: proyecto_login
   En pgAdmin o terminal:
   CREATE DATABASE proyecto_login;
```

### 2️⃣ Configurar Variables de Entorno
```
[ ] Copiar .env.example a .env
[ ] Editar .env con tus credenciales:
   - POSTGRES_USER
   - POSTGRES_PASSWORD
   - POSTGRES_DB
   - SECRET_KEY (generar valor fuerte)
```

### 3️⃣ Instalar Dependencias
```
[ ] Crear virtual environment: python -m venv venv
[ ] Activar: venv\Scripts\activate (Windows)
[ ] Instalar: pip install -r requirements.txt
```

### 4️⃣ Ejecutar la Aplicación
```
Windows:
[ ] Doble click en run.bat (abre Backend y Frontend)

Linux/macOS:
[ ] chmod +x run.sh
[ ] ./run.sh

Manual (2 terminales):
[ ] Terminal 1: uvicorn main:app --reload
[ ] Terminal 2: streamlit run streamlit_app.py
```

### 5️⃣ Verificar que funciona
```
[ ] Backend accesible en http://localhost:8000/docs
[ ] Frontend accesible en http://localhost:8501
[ ] Probar registro de usuario
[ ] Probar login con usuario creado
[ ] Probar acceso como admin
```

---

## 🔑 Generar SECRET_KEY Seguro

**Opción 1: Python**
```python
import secrets
print(secrets.token_urlsafe(32))
```

**Opción 2: OpenSSL**
```bash
openssl rand -base64 32
```

Copiar el resultado en `.env` como `SECRET_KEY=...`

---

## 📍 URLs Importantes

| Componente | URL | Descripción |
|-----------|-----|-------------|
| **Frontend** | http://localhost:8501 | Interfaz Streamlit |
| **API Docs** | http://localhost:8000/docs | Swagger UI |
| **API ReDoc** | http://localhost:8000/redoc | Documentación alternativa |
| **Health Check** | http://localhost:8000/ | Verificar API |

---

## 🧪 Usuarios de Prueba

Estos están listos para usar después de la primera ejecución:

```
👤 Usuario Regular
   Username: user1
   Password: password123
   
👨‍💼 Administrador
   Username: admin1
   Password: adminpass123
```

O crea los tuyos en la página de registro de Streamlit.

---

## 🐛 Problemas Comunes y Soluciones

### PostgreSQL no encuentra conexión
```
❌ Error: could not connect to server
✅ Solución:
   1. Verificar que PostgreSQL está corriendo
   2. Verificar credenciales en .env
   3. Verificar host y puerto (localhost:5432 por defecto)
```

### ModuleNotFoundError: No module named 'streamlit'
```
❌ Error: ModuleNotFoundError
✅ Solución:
   pip install streamlit
```

### CORS Error en el navegador
```
❌ Error: Access to XMLHttpRequest blocked
✅ Solución:
   - Confirmar Backend en http://localhost:8000
   - Confirmar Frontend en http://localhost:8501
   - Ambos deben estar corriendo
```

### Token expirado después de 30 minutos
```
❌ Error: Token inválido
✅ Solución:
   - Hacer login nuevamente
   - El token JWT expira cada 30 minutos por seguridad
```

### El archivo .env no se carga
```
❌ Error: Variables de entorno vacías
✅ Solución:
   - Instalar: pip install python-dotenv
   - Reiniciar la aplicación
   - Verificar que .env está en la carpeta raíz
```

---

## 📊 Estructura de Directorios

```
proyecto_login/
├── 📄 main.py                    ← Punto de entrada Backend
├── 📄 streamlit_app.py           ← Frontend Streamlit (NUEVO ✨)
├── 📄 requirements.txt           ← Dependencias
├── 📄 README.md                  ← Documentación (NUEVO ✨)
├── 📄 .env.example               ← Plantilla variables (NUEVO ✨)
├── 📄 run.bat                    ← Script ejecución Windows (NUEVO ✨)
├── 📄 run.sh                     ← Script ejecución Linux (NUEVO ✨)
│
├── 📁 core/                      ← Configuración central
├── 📁 database/                  ← Conexión BD
├── 📁 models/                    ← Modelos ORM
├── 📁 routers/                   ← Endpoints API
├── 📁 schemas/                   ← Validación Pydantic
├── 📁 services/                  ← Lógica negocio
└── 📁 logs/                      ← Archivos log (auto-generado)
```

---

## 🚀 Siguientes Pasos

Después de la configuración inicial:

1. **Explorar la API:**
   - Ir a http://localhost:8000/docs
   - Probar endpoints directamente

2. **Usar el Frontend:**
   - Ir a http://localhost:8501
   - Registrarse e iniciar sesión
   - Explorar dashboard

3. **Entender el código:**
   - Revisar `main.py` para estructura FastAPI
   - Revisar `streamlit_app.py` para interfaz
   - Revisar `services/auth_service.py` para lógica

4. **Expandir funcionalidades:**
   - Agregar más modelos en `models/`
   - Agregar más endpoints en `routers/`
   - Agregar páginas en `streamlit_app.py`

---

## 📧 Ayuda Adicional

Si necesitas ayuda:
1. Revisa el `README.md` completo
2. Ejecuta `streamlit run streamlit_app.py --help`
3. Ejecuta `uvicorn main:app --help`
4. Revisa los logs en carpeta `logs/`

---

**¡Tu sistema de login está listo! 🎉**
