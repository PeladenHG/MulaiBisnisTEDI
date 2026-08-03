"""
Auth System untuk MulaiBisnis App
Mengelola login, sign-up, dan approval dari admin
"""

import sqlite3
import hashlib
from datetime import datetime
import streamlit as st
from pathlib import Path

# ─────────────────────────────────────────────────────────────────
# DATABASE INITIALIZATION
# ─────────────────────────────────────────────────────────────────

DB_PATH = "mulai_bisnis.db"

def init_database():
    """Inisialisasi database dengan tabel yang diperlukan"""
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    
    # Tabel Users
    c.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            email TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            full_name TEXT,
            status TEXT DEFAULT 'pending',
            is_admin BOOLEAN DEFAULT 0,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            approved_at TIMESTAMP
        )
    ''')
    
    # Tabel untuk approval history
    c.execute('''
        CREATE TABLE IF NOT EXISTS approval_history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            action TEXT,
            admin_notes TEXT,
            approved_by TEXT,
            action_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users(id)
        )
    ''')
    
    conn.commit()
    conn.close()

# ─────────────────────────────────────────────────────────────────
# PASSWORD HASHING
# ─────────────────────────────────────────────────────────────────

def hash_password(password):
    """Hash password menggunakan SHA256"""
    return hashlib.sha256(password.encode()).hexdigest()

def verify_password(password, hashed_password):
    """Verifikasi password"""
    return hash_password(password) == hashed_password

# ─────────────────────────────────────────────────────────────────
# USER REGISTRATION
# ─────────────────────────────────────────────────────────────────

def register_user(username, email, password, full_name):
    """
    Mendaftarkan user baru
    Status: 'pending' (menunggu approval admin)
    """
    try:
        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()
        
        # Check jika username atau email sudah ada
        c.execute('SELECT id FROM users WHERE username = ? OR email = ?', (username, email))
        if c.fetchone():
            return False, "Username atau Email sudah terdaftar"
        
        # Insert user baru dengan status 'pending'
        hashed_pwd = hash_password(password)
        c.execute('''
            INSERT INTO users (username, email, password, full_name, status)
            VALUES (?, ?, ?, ?, 'pending')
        ''', (username, email, hashed_pwd, full_name))
        
        conn.commit()
        user_id = c.lastrowid
        conn.close()
        
        return True, f"Pendaftaran berhasil! Menunggu persetujuan admin."
    
    except sqlite3.IntegrityError:
        return False, "Username atau Email sudah terdaftar"
    except Exception as e:
        return False, f"Error: {str(e)}"

# ─────────────────────────────────────────────────────────────────
# USER LOGIN
# ─────────────────────────────────────────────────────────────────

def login_user(username, password):
    """
    Login user
    Return: (success, message, user_data)
    """
    try:
        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()
        
        c.execute('SELECT * FROM users WHERE username = ?', (username,))
        user = c.fetchone()
        conn.close()
        
        if not user:
            return False, "Username tidak ditemukan", None
        
        # user tuple: (id, username, email, password, full_name, status, is_admin, created_at, approved_at)
        user_id, username_db, email, hashed_pwd, full_name, status, is_admin, created_at, approved_at = user
        
        # Verifikasi password
        if not verify_password(password, hashed_pwd):
            return False, "Password salah", None
        
        # Check status user
        if status == 'pending':
            return False, "Akun Anda masih menunggu persetujuan admin", None
        elif status == 'rejected':
            return False, "Akun Anda ditolak oleh admin", None
        elif status != 'approved':
            return False, f"Status akun tidak valid: {status}", None
        
        user_data = {
            'id': user_id,
            'username': username_db,
            'email': email,
            'full_name': full_name,
            'is_admin': bool(is_admin),
            'status': status
        }
        
        return True, "Login berhasil", user_data
    
    except Exception as e:
        return False, f"Error: {str(e)}", None

# ─────────────────────────────────────────────────────────────────
# ADMIN FUNCTIONS
# ─────────────────────────────────────────────────────────────────

def get_pending_users():
    """Ambil semua user dengan status 'pending'"""
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('''
        SELECT id, username, email, full_name, created_at 
        FROM users 
        WHERE status = 'pending'
        ORDER BY created_at ASC
    ''')
    users = c.fetchall()
    conn.close()
    return users

def get_all_users():
    """Ambil semua user"""
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('''
        SELECT id, username, email, full_name, status, is_admin, created_at, approved_at
        FROM users
        ORDER BY created_at DESC
    ''')
    users = c.fetchall()
    conn.close()
    return users

def approve_user(user_id, admin_username, notes=""):
    """Approve user yang mendaftar"""
    try:
        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()
        
        # Update status menjadi 'approved'
        c.execute('''
            UPDATE users 
            SET status = 'approved', approved_at = CURRENT_TIMESTAMP
            WHERE id = ?
        ''', (user_id,))
        
        # Catat di approval history
        c.execute('''
            INSERT INTO approval_history (user_id, action, admin_notes, approved_by)
            VALUES (?, 'approved', ?, ?)
        ''', (user_id, notes, admin_username))
        
        conn.commit()
        conn.close()
        return True, "User berhasil di-approve"
    except Exception as e:
        return False, f"Error: {str(e)}"

def reject_user(user_id, admin_username, notes=""):
    """Reject user yang mendaftar"""
    try:
        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()
        
        # Update status menjadi 'rejected'
        c.execute('''
            UPDATE users 
            SET status = 'rejected'
            WHERE id = ?
        ''', (user_id,))
        
        # Catat di approval history
        c.execute('''
            INSERT INTO approval_history (user_id, action, admin_notes, approved_by)
            VALUES (?, 'rejected', ?, ?)
        ''', (user_id, notes, admin_username))
        
        conn.commit()
        conn.close()
        return True, "User berhasil di-reject"
    except Exception as e:
        return False, f"Error: {str(e)}"

def get_approval_history(user_id):
    """Ambil history approval untuk user tertentu"""
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('''
        SELECT action, admin_notes, approved_by, action_date
        FROM approval_history
        WHERE user_id = ?
        ORDER BY action_date DESC
    ''', (user_id,))
    history = c.fetchall()
    conn.close()
    return history

def make_admin(user_id):
    """Ubah user menjadi admin"""
    try:
        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()
        c.execute('UPDATE users SET is_admin = 1 WHERE id = ?', (user_id,))
        conn.commit()
        conn.close()
        return True, "User berhasil dijadikan admin"
    except Exception as e:
        return False, f"Error: {str(e)}"

def remove_admin(user_id):
    """Hapus status admin dari user"""
    try:
        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()
        c.execute('UPDATE users SET is_admin = 0 WHERE id = ?', (user_id,))
        conn.commit()
        conn.close()
        return True, "Status admin berhasil dihapus"
    except Exception as e:
        return False, f"Error: {str(e)}"

# ─────────────────────────────────────────────────────────────────
# SESSION STATE MANAGEMENT
# ─────────────────────────────────────────────────────────────────

def init_session():
    """Inisialisasi session state untuk auth"""
    if 'logged_in' not in st.session_state:
        st.session_state.logged_in = False
    if 'user' not in st.session_state:
        st.session_state.user = None

def logout():
    """Logout user"""
    st.session_state.logged_in = False
    st.session_state.user = None

# Initialize database on module load
init_database()
