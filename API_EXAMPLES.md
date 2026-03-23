# 📚 EJEMPLOS DE USO DE LA API

Aquí encontrarás ejemplos de cómo usar los endpoints de la API del sistema de login.

## 🔗 URLs Base

```
API Base URL: http://localhost:8000
Documentación: http://localhost:8000/docs
```

---

## 1️⃣ REGISTRO DE USUARIO

### Descripción
Crea una nueva cuenta de usuario en el sistema.

### Endpoint
```http
POST /auth/register
```

### Headers
```
Content-Type: application/json
```

### Body
```json
{
  "username": "juan_perez",
  "email": "juan@example.com",
  "password": "MiPassword123!",
  "role": "user"
}
```

### Respuesta Exitosa (200)
```json
{
  "id": 1,
  "username": "juan_perez",
  "email": "juan@example.com",
  "role": "user",
  "is_active": true
}
```

### Errores Posibles
```json
{
  "detail": "el usuario debe estar entre 3 y 50 caracteres"
}
```

### Ejemplos por Lenguaje

#### cURL
```bash
curl -X POST "http://localhost:8000/auth/register" \
  -H "Content-Type: application/json" \
  -d '{
    "username": "juan_perez",
    "email": "juan@example.com",
    "password": "MiPassword123!",
    "role": "user"
  }'
```

#### Python (requests)
```python
import requests

payload = {
    "username": "juan_perez",
    "email": "juan@example.com",
    "password": "MiPassword123!",
    "role": "user"
}

response = requests.post(
    "http://localhost:8000/auth/register",
    json=payload
)

print(response.json())
```

#### JavaScript (fetch)
```javascript
const payload = {
  username: "juan_perez",
  email: "juan@example.com",
  password: "MiPassword123!",
  role: "user"
};

fetch("http://localhost:8000/auth/register", {
  method: "POST",
  headers: {
    "Content-Type": "application/json"
  },
  body: JSON.stringify(payload)
})
  .then(r => r.json())
  .then(data => console.log(data));
```

#### PowerShell
```powershell
$body = @{
    username = "juan_perez"
    email = "juan@example.com"
    password = "MiPassword123!"
    role = "user"
} | ConvertTo-Json

Invoke-WebRequest -Uri "http://localhost:8000/auth/register" `
  -Method POST `
  -Headers @{"Content-Type" = "application/json"} `
  -Body $body
```

---

## 2️⃣ INICIAR SESIÓN

### Descripción
Autentica un usuario y retorna un JWT token de acceso.

### Endpoint
```http
POST /auth/login
```

### Headers
```
Content-Type: application/x-www-form-urlencoded
```

### Body
```
username=juan_perez&password=MiPassword123!
```

### Respuesta Exitosa (200)
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJqdWFuX3BlcmV6Iiwicm9sZSI6InVzZXIiLCJleHAiOjE2NDk3MDEyMzR9.abc123...",
  "token_type": "bearer"
}
```

### Errores Posibles
```json
{
  "detail": "Usuario o contraseña incorrectos"
}
```

### Ejemplos por Lenguaje

#### cURL
```bash
curl -X POST "http://localhost:8000/auth/login" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "username=juan_perez&password=MiPassword123!"
```

#### Python (requests)
```python
import requests

response = requests.post(
    "http://localhost:8000/auth/login",
    data={
        "username": "juan_perez",
        "password": "MiPassword123!"
    }
)

data = response.json()
token = data["access_token"]
print(f"Token: {token}")
```

#### JavaScript (fetch)
```javascript
const params = new URLSearchParams();
params.append("username", "juan_perez");
params.append("password", "MiPassword123!");

fetch("http://localhost:8000/auth/login", {
  method: "POST",
  body: params
})
  .then(r => r.json())
  .then(data => {
    const token = data.access_token;
    console.log("Token:", token);
    localStorage.setItem("token", token);
  });
```

#### PowerShell
```powershell
$body = "username=juan_perez&password=MiPassword123!"

$response = Invoke-WebRequest -Uri "http://localhost:8000/auth/login" `
  -Method POST `
  -Headers @{"Content-Type" = "application/x-www-form-urlencoded"} `
  -Body $body

$data = $response.Content | ConvertFrom-Json
$token = $data.access_token
Write-Host "Token: $token"
```

---

## 3️⃣ OBTENER DATOS DEL USUARIO

### Descripción
Retorna los datos del usuario autenticado.

### Endpoint
```http
GET /auth/me
```

### Headers
```
Authorization: Bearer <access_token>
```

### Respuesta Exitosa (200)
```json
{
  "id": 1,
  "username": "juan_perez",
  "email": "juan@example.com",
  "role": "user",
  "is_active": true
}
```

### Errores Posibles
```json
{
  "detail": "Not authenticated"
}
```

### Ejemplos por Lenguaje

#### cURL
```bash
TOKEN="eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."

curl -X GET "http://localhost:8000/auth/me" \
  -H "Authorization: Bearer $TOKEN"
```

#### Python (requests)
```python
import requests

token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."

headers = {"Authorization": f"Bearer {token}"}

response = requests.get(
    "http://localhost:8000/auth/me",
    headers=headers
)

user = response.json()
print(f"Usuario: {user['username']}")
print(f"Email: {user['email']}")
```

#### JavaScript (fetch)
```javascript
const token = localStorage.getItem("token");

fetch("http://localhost:8000/auth/me", {
  method: "GET",
  headers: {
    "Authorization": `Bearer ${token}`
  }
})
  .then(r => r.json())
  .then(user => {
    console.log("Usuario:", user.username);
    console.log("Email:", user.email);
  });
```

#### PowerShell
```powershell
$token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."

$headers = @{"Authorization" = "Bearer $token"}

$response = Invoke-WebRequest -Uri "http://localhost:8000/auth/me" `
  -Method GET `
  -Headers $headers

$user = $response.Content | ConvertFrom-Json
Write-Host "Usuario: $($user.username)"
```

---

## 4️⃣ ACCESO SOLO PARA ADMINS

### Descripción
Endpoint que solo permite acceso a usuarios con rol de administrador.

### Endpoint
```http
GET /auth/admin-only
```

### Headers
```
Authorization: Bearer <access_token>
```

### Respuesta Exitosa (200)
```json
{
  "message": "Bienvenido, admin!",
  "username": "admin1",
  "role": "admin"
}
```

### Errores Posibles
```json
{
  "detail": "Acceso denegado: solo administradores pueden acceder a este recurso"
}
```

### Ejemplos por Lenguaje

#### cURL
```bash
ADMIN_TOKEN="eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."

curl -X GET "http://localhost:8000/auth/admin-only" \
  -H "Authorization: Bearer $ADMIN_TOKEN"
```

#### Python (requests)
```python
import requests

admin_token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."

headers = {"Authorization": f"Bearer {admin_token}"}

response = requests.get(
    "http://localhost:8000/auth/admin-only",
    headers=headers
)

if response.status_code == 200:
    print("✅ Acceso de admin confirmado")
    print(response.json())
else:
    print(f"❌ {response.json()['detail']}")
```

#### JavaScript (fetch)
```javascript
const adminToken = localStorage.getItem("token");

fetch("http://localhost:8000/auth/admin-only", {
  method: "GET",
  headers: {
    "Authorization": `Bearer ${adminToken}`
  }
})
  .then(async r => {
    if (r.ok) {
      console.log("✅ Admin confirmado");
      return r.json();
    } else {
      console.log("❌ No tienes permisos de admin");
      throw new Error((await r.json()).detail);
    }
  })
  .then(data => console.log(data));
```

---

## 🔄 FLUJO COMPLETO DE AUTENTICACIÓN

### Paso a Paso

```
1. Registrar usuario
   POST /auth/register
   
2. Iniciar sesión
   POST /auth/login
   └─> Obtener: access_token
   
3. Usar token en requests
   GET /auth/me
   Headers: Authorization: Bearer {token}
   
4. Acceso a recursos protegidos
   GET /auth/admin-only (si es admin)
   Headers: Authorization: Bearer {token}
```

### Script Python Completo

```python
import requests
import time

BASE_URL = "http://localhost:8000"

# 1. Registrar usuario
print("1️⃣ Registrando usuario...")
register_payload = {
    "username": "testuser123",
    "email": "test@example.com",
    "password": "TestPass123!",
    "role": "user"
}

register_response = requests.post(
    f"{BASE_URL}/auth/register",
    json=register_payload
)

if register_response.status_code == 200:
    print("✅ Usuario registrado exitosamente")
    print(f"   ID: {register_response.json()['id']}")
else:
    print(f"❌ Error: {register_response.json()['detail']}")
    exit()

# 2. Iniciar sesión
print("\n2️⃣ Iniciando sesión...")
login_response = requests.post(
    f"{BASE_URL}/auth/login",
    data={
        "username": "testuser123",
        "password": "TestPass123!"
    }
)

if login_response.status_code == 200:
    token = login_response.json()["access_token"]
    print("✅ Login exitoso")
    print(f"   Token: {token[:30]}...")
else:
    print(f"❌ Error: {login_response.json()['detail']}")
    exit()

# 3. Obtener datos del usuario
print("\n3️⃣ Obteniendo datos del usuario...")
headers = {"Authorization": f"Bearer {token}"}

me_response = requests.get(
    f"{BASE_URL}/auth/me",
    headers=headers
)

if me_response.status_code == 200:
    user = me_response.json()
    print("✅ Datos obtenidos:")
    print(f"   Username: {user['username']}")
    print(f"   Email: {user['email']}")
    print(f"   Role: {user['role']}")
else:
    print(f"❌ Error: {me_response.json()['detail']}")

# 4. Verificar acceso admin (si no es admin, fallará)
print("\n4️⃣ Verificando acceso de admin...")
admin_response = requests.get(
    f"{BASE_URL}/auth/admin-only",
    headers=headers
)

if admin_response.status_code == 200:
    print("✅ Acceso de admin confirmado")
    print(admin_response.json())
else:
    print(f"ℹ️ No es administrador: {admin_response.json()['detail']}")

print("\n✅ Flujo completo de autenticación completado")
```

---

## ⏰ INFORMACIÓN IMPORTANTE

### Expiración de Token
- **Duración:** 30 minutos
- **Algoritmo:** HS256 (HMAC SHA-256)
- **Renovación:** Hacer login nuevamente después de expirar

### Seguridad
- Los tokens NO deben ser compartidos
- Las contraseñas se almacenan hasheadas con bcrypt
- Los endpoints protegidos requieren token válido en header

### Testing
- Usa Swagger UI: http://localhost:8000/docs
- Usa ReDoc: http://localhost:8000/redoc
- O usa los ejemplos anteriores con tu cliente favorito

---

## 🐛 Solución de Problemas

### "Token inválido"
```
❌ "detail": "Invalid token"
✅ Verificar:
   - El token no haya expirado (30 min)
   - El token sea completo y correcto
   - El header sea: Authorization: Bearer <token>
```

### "Usuario o contraseña incorrectos"
```
❌ "detail": "Usuario o contraseña incorrectos"
✅ Verificar:
   - El usuario exista en la base de datos
   - La contraseña sea exactamente correcta
   - Revisar mayúsculas/minúsculas
```

### "CORS error"
```
❌ Error de CORS en navegador
✅ Verificar:
   - Backend corriendo en http://localhost:8000
   - Frontend (si existe) en puerto diferente
   - CORS está habilitado en main.py
```

---

**¡Ya tienes todo lo que necesitas para usar la API! 🚀**
