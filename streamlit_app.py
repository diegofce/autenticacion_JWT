import streamlit as st
import requests
import os
from datetime import datetime

# ===========================
# CONFIGURACIÓN INICIAL
# ===========================
st.set_page_config(
    page_title="Sistema de Login Seguro",
    page_icon="🔐",
    layout="wide",
    initial_sidebar_state="expanded"
)

# API Configuration
API_BASE_URL = os.getenv("API_BASE_URL", "http://localhost:8000")
REQUEST_TIMEOUT_SECONDS = 10

# ===========================
# ESTILOS CSS PERSONALIZADOS
# ===========================
st.markdown("""
<style>
    :root {
        --primary-color: #FF6B6B;
        --secondary-color: #4ECDC4;
        --success-color: #95E1D3;
        --danger-color: #FF6B6B;
        --warning-color: #FFE66D;
    }

    .main {
        padding: 2rem;
    }

    .stTabs [data-baseweb="tab-list"] button [data-testid="stMarkdownContainer"] p {
        font-size: 1rem;
        font-weight: 600;
    }

    .auth-container {
        max-width: 400px;
        margin: 0 auto;
    }

    .success-box {
        background: linear-gradient(135deg, #d4edda 0%, #c3e6cb 100%);
        padding: 1.5rem;
        border-radius: 0.5rem;
        border-left: 4px solid #28a745;
        border-top: 4px solid #28a745;
        color: #155724;
        margin-bottom: 1rem;
        box-shadow: 0 4px 6px rgba(40, 167, 69, 0.2);
    }

    .success-box h2 {
        margin-top: 0;
        color: #155724;
        text-align: center;
    }

    .success-box p {
        margin: 0.5rem 0;
        text-align: center;
    }

    .error-box {
        background-color: #f8d7da;
        padding: 1rem;
        border-radius: 0.5rem;
        border-left: 4px solid #dc3545;
        color: #721c24;
        margin-bottom: 1rem;
    }

    .info-box {
        background-color: #d1ecf1;
        padding: 1rem;
        border-radius: 0.5rem;
        border-left: 4px solid #17a2b8;
        color: #0c5460;
        margin-bottom: 1rem;
    }

    .admin-badge {
        display: inline-block;
        background-color: #FF6B6B;
        color: white;
        padding: 0.25rem 0.75rem;
        border-radius: 20px;
        font-size: 0.8rem;
        font-weight: bold;
        margin-left: 0.5rem;
    }

    .user-badge {
        display: inline-block;
        background-color: #4ECDC4;
        color: white;
        padding: 0.25rem 0.75rem;
        border-radius: 20px;
        font-size: 0.8rem;
        font-weight: bold;
        margin-left: 0.5rem;
    }
</style>
""", unsafe_allow_html=True)

# ===========================
# GESTIÓN DE SESIÓN
# ===========================


def init_session_state():
    """Inicializa variables de sesión"""
    if 'token' not in st.session_state:
        st.session_state.token = None
    if 'user' not in st.session_state:
        st.session_state.user = None
    if 'authenticated' not in st.session_state:
        st.session_state.authenticated = False
    if 'page' not in st.session_state:
        st.session_state.page = "login"


init_session_state()

# ===========================
# FUNCIONES DE API
# ===========================


def register_user(username: str, email: str, password: str, role: str) -> dict:
    """Registra un nuevo usuario"""
    try:
        response = requests.post(
            f"{API_BASE_URL}/auth/register",
            json={
                "username": username,
                "email": email,
                "password": password,
                "role": role
            },
            timeout=REQUEST_TIMEOUT_SECONDS,
        )
        response_data = response.json()
        return {
            "success": response.status_code == 200,
            "data": response_data,
            "status_code": response.status_code,
            "message": response_data.get("detail", "Registro exitoso")
        }
    except requests.exceptions.ConnectionError:
        return {
            "success": False,
            "message": "❌ Error de conexión: No se puede conectar al servidor API en " + API_BASE_URL,
            "status_code": 0
        }
    except requests.exceptions.Timeout:
        return {
            "success": False,
            "message": "❌ Tiempo de espera agotado al conectar con la API",
            "status_code": 0
        }
    except requests.exceptions.RequestException as e:
        return {
            "success": False,
            "message": f"❌ Error HTTP: {str(e)}",
            "status_code": 0
        }
    except Exception as e:
        return {
            "success": False,
            "message": f"❌ Error: {str(e)}",
            "status_code": 0
        }


def login_user(username: str, password: str) -> dict:
    """Autentica un usuario y obtiene el token"""
    try:
        response = requests.post(
            f"{API_BASE_URL}/auth/login",
            data={
                "username": username,
                "password": password
            },
            timeout=REQUEST_TIMEOUT_SECONDS,
        )
        if response.status_code == 200:
            data = response.json()
            return {
                "success": True,
                "token": data.get("access_token"),
                "token_type": data.get("token_type"),
                "message": "✅ Login exitoso"
            }
        else:
            return {
                "success": False,
                "message": response.json().get("detail", "Usuario o contraseña incorrectos"),
                "status_code": response.status_code
            }
    except requests.exceptions.ConnectionError:
        return {
            "success": False,
            "message": "❌ Error de conexión: No se puede conectar al servidor API",
            "status_code": 0
        }
    except requests.exceptions.Timeout:
        return {
            "success": False,
            "message": "❌ Tiempo de espera agotado al conectar con la API",
            "status_code": 0
        }
    except requests.exceptions.RequestException as e:
        return {
            "success": False,
            "message": f"❌ Error HTTP: {str(e)}",
            "status_code": 0
        }
    except Exception as e:
        return {
            "success": False,
            "message": f"❌ Error: {str(e)}",
            "status_code": 0
        }


def get_current_user(token: str) -> dict:
    """Obtiene los datos del usuario autenticado"""
    try:
        headers = {"Authorization": f"Bearer {token}"}
        response = requests.get(
            f"{API_BASE_URL}/auth/me",
            headers=headers,
            timeout=REQUEST_TIMEOUT_SECONDS,
        )
        if response.status_code == 200:
            return {
                "success": True,
                "user": response.json()
            }
        else:
            return {
                "success": False,
                "message": response.json().get("detail", "Token inválido")
            }
    except requests.exceptions.Timeout:
        return {
            "success": False,
            "message": "❌ Tiempo de espera agotado al consultar usuario"
        }
    except requests.exceptions.RequestException as e:
        return {
            "success": False,
            "message": f"❌ Error HTTP: {str(e)}"
        }
    except Exception as e:
        return {
            "success": False,
            "message": f"❌ Error: {str(e)}"
        }


def check_admin_access(token: str) -> dict:
    """Verifica acceso de administrador"""
    try:
        headers = {"Authorization": f"Bearer {token}"}
        response = requests.get(
            f"{API_BASE_URL}/auth/admin-only",
            headers=headers,
            timeout=REQUEST_TIMEOUT_SECONDS,
        )
        if response.status_code == 200:
            return {
                "success": True,
                "data": response.json()
            }
        else:
            return {
                "success": False,
                "message": response.json().get("detail", "Acceso denegado")
            }
    except requests.exceptions.Timeout:
        return {
            "success": False,
            "message": "❌ Tiempo de espera agotado al verificar acceso admin"
        }
    except requests.exceptions.RequestException as e:
        return {
            "success": False,
            "message": f"❌ Error HTTP: {str(e)}"
        }
    except Exception as e:
        return {
            "success": False,
            "message": f"❌ Error: {str(e)}"
        }

# ===========================
# PÁGINA DE REGISTRO
# ===========================


def page_register():
    """Página de registro de nuevos usuarios"""
    col1, col2, col3 = st.columns([1, 2, 1])

    with col2:
        st.markdown("## 📝 Crear Nueva Cuenta")
        st.markdown("---")

        with st.form("register_form"):
            username = st.text_input(
                "👤 Nombre de Usuario",
                placeholder="Ingresa tu usuario (3-50 caracteres)",
                help="Debe ser único y entre 3-50 caracteres"
            )

            email = st.text_input(
                "📧 Email",
                placeholder="tu@email.com",
                help="Email debe ser único"
            )

            password = st.text_input(
                "🔒 Contraseña",
                type="password",
                placeholder="Contraseña segura",
                help="Entre 6-100 caracteres"
            )

            password_confirm = st.text_input(
                "🔒 Confirmar Contraseña",
                type="password",
                placeholder="Repite tu contraseña"
            )

            role = st.selectbox(
                "👥 Rol de Usuario",
                options=["user", "admin"],
                format_func=lambda x: "👤 Usuario Regular" if x == "user" else "👨‍💼 Administrador"
            )

            submitted = st.form_submit_button(
                "🚀 Registrarse", use_container_width=True)

        if submitted:
            # Validaciones
            if not all([username, email, password, password_confirm]):
                st.markdown(
                    '<div class="error-box">❌ Todos los campos son obligatorios</div>', unsafe_allow_html=True)
            elif password != password_confirm:
                st.markdown(
                    '<div class="error-box">❌ Las contraseñas no coinciden</div>', unsafe_allow_html=True)
            elif len(username) < 3 or len(username) > 50:
                st.markdown(
                    '<div class="error-box">❌ El usuario debe tener entre 3-50 caracteres</div>', unsafe_allow_html=True)
            elif len(password) < 6 or len(password) > 100:
                st.markdown(
                    '<div class="error-box">❌ La contraseña debe tener entre 6-100 caracteres</div>', unsafe_allow_html=True)
            elif len(email) < 5 or len(email) > 100:
                st.markdown(
                    '<div class="error-box">❌ El email debe ser válido (5-100 caracteres)</div>', unsafe_allow_html=True)
            else:
                with st.spinner("⏳ Registrando usuario..."):
                    result = register_user(username, email, password, role)

                    if result["success"]:
                        st.success("✅ ¡REGISTRO DE USUARIO EXITOSO!")
                        st.markdown(
                            '<div class="success-box"><h2>🎉 ¡BIENVENIDO!</h2><p><strong>' + username + '</strong> ha sido registrado correctamente.</p><p>Ya puedes iniciar sesión con tus credenciales.</p></div>', unsafe_allow_html=True)
                        st.balloons()
                        import time
                        time.sleep(2)
                        st.session_state.page = "login"
                        st.rerun()
                    else:
                        error_msg = result.get(
                            "message", "Error en el registro")
                        st.markdown(
                            f'<div class="error-box">❌ {error_msg}</div>', unsafe_allow_html=True)

        st.markdown("---")
        col_a, col_b = st.columns(2)
        with col_a:
            if st.button("🔙 Volver a Login", use_container_width=True):
                st.session_state.page = "login"
                st.rerun()

# ===========================
# PÁGINA DE LOGIN
# ===========================


def page_login():
    """Página de login"""
    col1, col2, col3 = st.columns([1, 2, 1])

    with col2:
        st.markdown("## 🔐 Iniciar Sesión")
        st.markdown("---")

        with st.form("login_form"):
            username = st.text_input(
                "👤 Usuario",
                placeholder="Ingresa tu usuario"
            )
            password = st.text_input(
                "🔒 Contraseña",
                type="password",
                placeholder="Ingresa tu contraseña"
            )

            submitted = st.form_submit_button(
                "✅ Ingresar", use_container_width=True)

        if submitted:
            if not username or not password:
                st.markdown(
                    '<div class="error-box">❌ Usuario y contraseña son obligatorios</div>', unsafe_allow_html=True)
            else:
                with st.spinner("⏳ Verificando credenciales..."):
                    result = login_user(username, password)

                    if result["success"]:
                        st.session_state.token = result["token"]
                        st.session_state.authenticated = True

                        # Obtener datos del usuario
                        user_result = get_current_user(result["token"])
                        if user_result["success"]:
                            st.session_state.user = user_result["user"]
                            st.session_state.page = "dashboard"
                            st.markdown(
                                '<div class="success-box">✅ Login exitoso</div>', unsafe_allow_html=True)
                            st.balloons()
                            st.rerun()
                        else:
                            st.session_state.token = None
                            st.session_state.user = None
                            st.session_state.authenticated = False
                            st.markdown(
                                f'<div class="error-box">{user_result.get("message", "Error obteniendo perfil de usuario")}</div>',
                                unsafe_allow_html=True,
                            )
                    else:
                        st.markdown(
                            f'<div class="error-box">{result.get("message", "Error en login")}</div>', unsafe_allow_html=True)

        st.markdown("---")
        st.markdown("### ¿No tienes cuenta?")
        if st.button("📝 Crear Nueva Cuenta", use_container_width=True):
            st.session_state.page = "register"
            st.rerun()

        # Datos de prueba
        with st.expander("📌 Usuarios de Prueba"):
            st.markdown("""
            **Usuario Regular:**
            - Usuario: `user1`
            - Contraseña: `password123`

            **Administrador:**
            - Usuario: `admin1`
            - Contraseña: `adminpass123`
            """)

# ===========================
# PÁGINA DE DASHBOARD
# ===========================


def page_dashboard():
    """Página del dashboard del usuario"""
    # Header
    col1, col2 = st.columns([3, 1])
    with col1:
        st.markdown("## 📊 Dashboard")
    with col2:
        if st.button("🚪 Cerrar Sesión", use_container_width=True):
            st.session_state.token = None
            st.session_state.user = None
            st.session_state.authenticated = False
            st.session_state.page = "login"
            st.markdown(
                '<div class="info-box">✅ Sesión cerrada correctamente</div>', unsafe_allow_html=True)
            st.rerun()

    st.markdown("---")

    if st.session_state.user:
        user = st.session_state.user

        # Tarjeta de perfil
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            st.markdown("### 👤 Mi Perfil")
            with st.container():
                col_a, col_b = st.columns([3, 1])
                with col_a:
                    st.markdown(
                        f"**Nombre de Usuario:** `{user.get('username', 'N/A')}`")
                    st.markdown(f"**Email:** `{user.get('email', 'N/A')}`")
                    st.markdown(f"**ID:** `{user.get('id', 'N/A')}`")
                with col_b:
                    role = user.get('role', 'user')
                    if role == 'admin':
                        st.markdown(
                            '<span class="admin-badge">ADMIN</span>', unsafe_allow_html=True)
                    else:
                        st.markdown(
                            '<span class="user-badge">USER</span>', unsafe_allow_html=True)

        st.markdown("---")

        # Información de sesión
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("👤 Estado", "✅ Autenticado")
        with col2:
            st.metric("🕐 Hora", datetime.now().strftime("%H:%M:%S"))
        with col3:
            st.metric("📅 Fecha", datetime.now().strftime("%d/%m/%Y"))

        st.markdown("---")

        # Panel de administrador
        if user.get('role') == 'admin':
            st.markdown("### 👨‍💼 Panel de Administrador")

            col1, col2 = st.columns(2)
            with col1:
                if st.button("🔍 Verificar Acceso Admin", use_container_width=True):
                    with st.spinner("⏳ Verificando acceso..."):
                        token = st.session_state.get("token")
                        if not token:
                            st.markdown(
                                '<div class="error-box">No hay token de sesión. Inicia sesión nuevamente.</div>', unsafe_allow_html=True)
                        else:
                            admin_result = check_admin_access(token)
                            if admin_result["success"]:
                                st.markdown(
                                    '<div class="success-box">✅ ¡Acceso de administrador confirmado!</div>', unsafe_allow_html=True)
                                st.json(admin_result["data"])
                            else:
                                st.markdown(
                                    f'<div class="error-box">{admin_result["message"]}</div>', unsafe_allow_html=True)

            with col2:
                st.info("💡 Como administrador tienes acceso a funciones especiales")

        st.markdown("---")

        # Información del token
        with st.expander("🔑 Información del Token (Desarrollo)"):
            if st.session_state.token:
                # Mostrar solo los primeros y últimos caracteres del token por seguridad
                token = st.session_state.token
                masked_token = f"{token[:20]}...{token[-20:]}"
                st.code(f"Bearer {masked_token}", language="text")
                st.warning(
                    "⚠️ Nunca compartas tu token. Es tu credencial de acceso segura.")

            st.markdown("""
            **Información del Token:**
            - **Tipo:** JWT (JSON Web Token)
            - **Algoritmo:** HS256
            - **Expiración:** 30 minutos
            - **Contenido:** Username y Role
            """)

        st.markdown("---")

        # Panel de información
        with st.expander("ℹ️ Acerca de tu Sesión"):
            st.markdown("""
            ### 🔒 Seguridad
            - Tu contraseña está protegida con **bcrypt**
            - Tu token JWT expira automáticamente en **30 minutos**
            - La comunicación es segura mediante **HTTPS** (en producción)

            ### 📊 Datos
            - Todos tus datos están almacenados en **PostgreSQL**
            - Tienes acceso a tus datos a través del endpoint `/auth/me`

            ### 🛡️ Roles
            - **Usuario Regular:** Acceso a funcionalidades básicas
            - **Administrador:** Acceso a panel administrativo y funciones especiales
            """)

# ===========================
# PÁGINA NO AUTENTICADA
# ===========================


def page_unauthenticated():
    """Página cuando el usuario no está autenticado"""
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.markdown("## 🔐 Sistema de Autenticación Seguro")
        st.markdown("---")

        tab1, tab2 = st.tabs(["🔐 Login", "📝 Registro"])

        with tab1:
            page_login()

        with tab2:
            page_register()

# ===========================
# LÓGICA PRINCIPAL
# ===========================


def main():
    """Función principal de la aplicación"""
    # Verificar si el usuario tiene token válido
    if st.session_state.authenticated and st.session_state.token:
        page_dashboard()
    else:
        page_unauthenticated()


if __name__ == "__main__":
    main()
