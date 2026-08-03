"""
Login & Sign-up Page untuk MulaiBisnis App
"""

import streamlit as st
import sys
from auth import (
    init_session, login_user, register_user, 
    logout, init_database
)

# ─────────────────────────────────────────────────────────────────
# PAGE CONFIG
# ─────────────────────────────────────────────────────────────────

st.set_page_config(
    page_title="MulaiBisnis - Login",
    page_icon="💰",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# ─────────────────────────────────────────────────────────────────
# CSS STYLING
# ─────────────────────────────────────────────────────────────────

st.markdown(
    """
    <style>
        .main { max-width: 500px; margin: 0 auto; }
        .auth-container {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            padding: 2rem;
            border-radius: 10px;
            color: white;
            margin: 2rem 0;
        }
        .auth-title { 
            font-size: 2.5rem; 
            font-weight: bold;
            text-align: center;
            margin-bottom: 0.5rem;
        }
        .auth-subtitle {
            text-align: center;
            font-size: 0.9rem;
            opacity: 0.9;
            margin-bottom: 2rem;
        }
        .success-box {
            background-color: #d4edda;
            border: 1px solid #c3e6cb;
            color: #155724;
            padding: 1rem;
            border-radius: 5px;
            margin: 1rem 0;
        }
        .error-box {
            background-color: #f8d7da;
            border: 1px solid #f5c6cb;
            color: #721c24;
            padding: 1rem;
            border-radius: 5px;
            margin: 1rem 0;
        }
        .info-box {
            background-color: #d1ecf1;
            border: 1px solid #bee5eb;
            color: #0c5460;
            padding: 1rem;
            border-radius: 5px;
            margin: 1rem 0;
        }
        .stButton button {
            width: 100%;
            background: #667eea;
            color: white;
            border: none;
            padding: 0.75rem;
            font-size: 1rem;
            font-weight: bold;
            border-radius: 5px;
            cursor: pointer;
            transition: 0.3s;
        }
        .stButton button:hover {
            background: #764ba2;
        }
        .divider-text {
            text-align: center;
            color: #888;
            margin: 1rem 0;
        }
        .toggle-auth {
            text-align: center;
            margin-top: 1.5rem;
            font-size: 0.9rem;
        }
        .toggle-auth a {
            color: #667eea;
            text-decoration: none;
            cursor: pointer;
            font-weight: bold;
        }
    </style>
    """,
    unsafe_allow_html=True
)

# ─────────────────────────────────────────────────────────────────
# INITIALIZATION
# ─────────────────────────────────────────────────────────────────

init_database()
init_session()

# ─────────────────────────────────────────────────────────────────
# MAIN APP
# ─────────────────────────────────────────────────────────────────

# Tab selection
tab1, tab2 = st.tabs(["🔐 Login", "📝 Sign Up"])

# ─────────────────────────────────────────────────────────────────
# LOGIN TAB
# ─────────────────────────────────────────────────────────────────

with tab1:
    st.markdown(
        '<div class="auth-container">'
        '<div class="auth-title">💰 MulaiBisnis</div>'
        '<div class="auth-subtitle">Teman Diskusi Kewirausahaan Anda</div>'
        '</div>',
        unsafe_allow_html=True
    )
    
    st.subheader("Login ke Akun Anda")
    
    with st.form(key="login_form"):
        username = st.text_input(
            "Username",
            placeholder="Masukkan username Anda"
        )
        password = st.text_input(
            "Password",
            type="password",
            placeholder="Masukkan password Anda"
        )
        submit = st.form_submit_button("Login", use_container_width=True)
    
    if submit:
        if not username or not password:
            st.error("❌ Username dan Password tidak boleh kosong")
        else:
            success, message, user_data = login_user(username, password)
            
            if success:
                st.session_state.logged_in = True
                st.session_state.user = user_data
                st.markdown(
                    f'<div class="success-box">✅ {message}</div>',
                    unsafe_allow_html=True
                )
                st.success(f"Selamat datang, {user_data['full_name']}!")
                st.info("Mengarahkan ke halaman utama...")
                st.session_state.page = "home"
                
                # Redirect ke halaman utama
                import time
                time.sleep(1)
                st.switch_page("pages/1_🏠_Home.py")
            else:
                st.markdown(
                    f'<div class="error-box">❌ {message}</div>',
                    unsafe_allow_html=True
                )

# ─────────────────────────────────────────────────────────────────
# SIGN UP TAB
# ─────────────────────────────────────────────────────────────────

with tab2:
    st.markdown(
        '<div class="auth-container">'
        '<div class="auth-title">💰 MulaiBisnis</div>'
        '<div class="auth-subtitle">Daftar untuk Memulai Perjalanan Bisnis Anda</div>'
        '</div>',
        unsafe_allow_html=True
    )
    
    st.subheader("Buat Akun Baru")
    
    st.markdown(
        '<div class="info-box">'
        '📢 <strong>Catatan:</strong> Akun baru akan menunggu persetujuan dari admin sebelum dapat digunakan.'
        '</div>',
        unsafe_allow_html=True
    )
    
    with st.form(key="signup_form"):
        col1, col2 = st.columns(2)
        
        with col1:
            full_name = st.text_input(
                "Nama Lengkap",
                placeholder="Nama Anda"
            )
        
        with col2:
            username = st.text_input(
                "Username",
                placeholder="Username unik"
            )
        
        email = st.text_input(
            "Email",
            placeholder="Email Anda"
        )
        
        password = st.text_input(
            "Password",
            type="password",
            placeholder="Minimal 6 karakter"
        )
        
        password_confirm = st.text_input(
            "Konfirmasi Password",
            type="password",
            placeholder="Masukkan ulang password"
        )
        
        submit = st.form_submit_button("Daftar", use_container_width=True)
    
    if submit:
        # Validasi
        if not all([full_name, username, email, password, password_confirm]):
            st.error("❌ Semua field harus diisi")
        elif len(password) < 6:
            st.error("❌ Password minimal 6 karakter")
        elif password != password_confirm:
            st.error("❌ Password tidak cocok")
        elif len(username) < 3:
            st.error("❌ Username minimal 3 karakter")
        else:
            # Register user
            success, message = register_user(username, email, password, full_name)
            
            if success:
                st.markdown(
                    f'<div class="success-box">✅ {message}</div>',
                    unsafe_allow_html=True
                )
                st.info(
                    "📧 Silakan periksa email Anda untuk notifikasi lebih lanjut. "
                    "Admin akan segera meninjau pengajuan Anda."
                )
            else:
                st.markdown(
                    f'<div class="error-box">❌ {message}</div>',
                    unsafe_allow_html=True
                )

# ─────────────────────────────────────────────────────────────────
# FOOTER
# ─────────────────────────────────────────────────────────────────

st.markdown("---")
st.markdown(
    """
    <div style='text-align: center; color: #888; font-size: 0.8rem;'>
    <p>💡 MulaiBisnis - Platform Pembelajaran & Mentoring Kewirausahaan</p>
    <p>© 2024 - Semua hak dilindungi</p>
    </div>
    """,
    unsafe_allow_html=True
)