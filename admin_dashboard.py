"""
Admin Dashboard untuk mengelola approval user
"""

import streamlit as st
from auth import (
    get_pending_users, get_all_users, approve_user, 
    reject_user, get_approval_history, make_admin, 
    remove_admin, init_session, logout
)
from datetime import datetime

# ─────────────────────────────────────────────────────────────────
# PAGE CONFIG
# ─────────────────────────────────────────────────────────────────

st.set_page_config(
    page_title="Admin Dashboard",
    page_icon="⚙️",
    layout="wide"
)

# ─────────────────────────────────────────────────────────────────
# CSS STYLING
# ─────────────────────────────────────────────────────────────────

st.markdown(
    """
    <style>
        .admin-header {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 2rem;
            border-radius: 10px;
            margin-bottom: 2rem;
        }
        .admin-title { font-size: 2rem; font-weight: bold; margin: 0; }
        .status-badge {
            display: inline-block;
            padding: 0.25rem 0.75rem;
            border-radius: 20px;
            font-size: 0.85rem;
            font-weight: bold;
        }
        .status-pending {
            background-color: #fff3cd;
            color: #856404;
        }
        .status-approved {
            background-color: #d4edda;
            color: #155724;
        }
        .status-rejected {
            background-color: #f8d7da;
            color: #721c24;
        }
        .user-card {
            border: 1px solid #ddd;
            border-radius: 8px;
            padding: 1.5rem;
            margin-bottom: 1rem;
            background-color: #f8f9fa;
        }
        .action-buttons { margin-top: 1rem; }
        .action-buttons button {
            margin-right: 0.5rem;
            padding: 0.5rem 1rem;
        }
    </style>
    """,
    unsafe_allow_html=True
)

# ─────────────────────────────────────────────────────────────────
# INITIALIZATION & AUTH CHECK
# ─────────────────────────────────────────────────────────────────

init_session()

# Check if user is logged in and is admin
if not st.session_state.logged_in:
    st.warning("⚠️ Silakan login terlebih dahulu")
    st.switch_page("login.py")
elif not st.session_state.user.get('is_admin', False):
    st.error("❌ Anda tidak memiliki akses ke halaman ini. Hanya admin yang dapat mengakses.")
    st.stop()

# ─────────────────────────────────────────────────────────────────
# HEADER
# ─────────────────────────────────────────────────────────────────

col1, col2 = st.columns([0.9, 0.1])

with col1:
    st.markdown(
        f"<div class='admin-header'>"
        f"<div class='admin-title'>⚙️ Admin Dashboard</div>"
        f"<p>Selamat datang, {st.session_state.user['full_name']}!</p>"
        f"</div>",
        unsafe_allow_html=True
    )

with col2:
    if st.button("🚪 Logout"):
        logout()
        st.switch_page("login.py")

# ─────────────────────────────────────────────────────────────────
# TABS
# ─────────────────────────────────────────────────────────────────

tab1, tab2 = st.tabs(["⏳ Pending Approvals", "👥 All Users"])

# ─────────────────────────────────────────────────────────────────
# TAB 1: PENDING APPROVALS
# ─────────────────────────────────────────────────────────────────

with tab1:
    st.subheader("📋 Pengajuan Pendaftaran Menunggu Approval")
    
    pending_users = get_pending_users()
    
    if not pending_users:
        st.info("✅ Tidak ada pengajuan yang menunggu persetujuan")
    else:
        st.warning(f"⏳ Ada {len(pending_users)} pengajuan menunggu persetujuan")
        
        for user in pending_users:
            user_id, username, email, full_name, created_at = user
            
            with st.container():
                st.markdown(
                    f"""
                    <div class='user-card'>
                        <h4>👤 {full_name}</h4>
                        <p><strong>Username:</strong> {username}</p>
                        <p><strong>Email:</strong> {email}</p>
                        <p><strong>Tanggal Daftar:</strong> {created_at}</p>
                        <span class='status-badge status-pending'>PENDING</span>
                    </div>
                    """,
                    unsafe_allow_html=True
                )
                
                col1, col2, col3 = st.columns(3)
                
                with col1:
                    notes = st.text_area(
                        "Catatan (opsional)",
                        key=f"notes_{user_id}",
                        height=60
                    )
                
                with col2:
                    if st.button("✅ Approve", key=f"approve_{user_id}"):
                        success, message = approve_user(
                            user_id, 
                            st.session_state.user['username'],
                            notes
                        )
                        if success:
                            st.success(f"✅ {message}")
                            st.rerun()
                        else:
                            st.error(f"❌ {message}")
                
                with col3:
                    if st.button("❌ Reject", key=f"reject_{user_id}"):
                        success, message = reject_user(
                            user_id,
                            st.session_state.user['username'],
                            notes
                        )
                        if success:
                            st.success(f"✅ {message}")
                            st.rerun()
                        else:
                            st.error(f"❌ {message}")
                
                st.divider()

# ─────────────────────────────────────────────────────────────────
# TAB 2: ALL USERS
# ─────────────────────────────────────────────────────────────────

with tab2:
    st.subheader("👥 Daftar Semua User")
    
    all_users = get_all_users()
    
    if not all_users:
        st.info("Belum ada user terdaftar")
    else:
        # Filter options
        col1, col2 = st.columns(2)
        
        with col1:
            status_filter = st.selectbox(
                "Filter Status",
                ["Semua", "pending", "approved", "rejected"]
            )
        
        with col2:
            search_term = st.text_input("Cari username atau email")
        
        # Apply filters
        filtered_users = all_users
        
        if status_filter != "Semua":
            filtered_users = [u for u in filtered_users if u[4] == status_filter]
        
        if search_term:
            filtered_users = [
                u for u in filtered_users 
                if search_term.lower() in u[1].lower() or search_term.lower() in u[2].lower()
            ]
        
        st.info(f"📊 Total: {len(filtered_users)} user")
        
        # Display users in table format
        for user in filtered_users:
            user_id, username, email, full_name, status, is_admin, created_at, approved_at = user
            
            # Determine status badge color
            if status == "pending":
                status_class = "status-pending"
            elif status == "approved":
                status_class = "status-approved"
            else:
                status_class = "status-rejected"
            
            with st.container():
                col1, col2, col3, col4 = st.columns([2, 2, 1, 1])
                
                with col1:
                    st.write(f"**{full_name}**")
                    st.caption(username)
                
                with col2:
                    st.write(email)
                    st.caption(f"Daftar: {created_at}")
                
                with col3:
                    st.markdown(
                        f"<span class='status-badge {status_class}'>{status.upper()}</span>",
                        unsafe_allow_html=True
                    )
                    if is_admin:
                        st.markdown("<span style='color: gold;'>⭐ Admin</span>", unsafe_allow_html=True)
                
                with col4:
                    if st.button("📋 Detail", key=f"detail_{user_id}"):
                        st.session_state[f"show_detail_{user_id}"] = not st.session_state.get(f"show_detail_{user_id}", False)
                
                # Show details if clicked
                if st.session_state.get(f"show_detail_{user_id}", False):
                    with st.expander("📜 Riwayat Approval"):
                        history = get_approval_history(user_id)
                        if history:
                            for action, admin_notes, approved_by, action_date in history:
                                st.write(f"**{action.upper()}** oleh {approved_by}")
                                st.write(f"Tanggal: {action_date}")
                                if admin_notes:
                                    st.write(f"Catatan: {admin_notes}")
                                st.divider()
                        else:
                            st.info("Belum ada riwayat approval")
                    
                    # Admin management
                    col_admin1, col_admin2 = st.columns(2)
                    
                    with col_admin1:
                        if not is_admin:
                            if st.button("⭐ Jadikan Admin", key=f"make_admin_{user_id}"):
                                success, message = make_admin(user_id)
                                if success:
                                    st.success(message)
                                    st.rerun()
                                else:
                                    st.error(message)
                    
                    with col_admin2:
                        if is_admin and user_id != st.session_state.user['id']:
                            if st.button("✖️ Hapus Admin", key=f"remove_admin_{user_id}"):
                                success, message = remove_admin(user_id)
                                if success:
                                    st.success(message)
                                    st.rerun()
                                else:
                                    st.error(message)
                
                st.divider()

# ─────────────────────────────────────────────────────────────────
# STATISTICS
# ─────────────────────────────────────────────────────────────────

st.markdown("---")
st.subheader("📊 Statistik")

col1, col2, col3, col4 = st.columns(4)

total_users = len(all_users)
pending = len([u for u in all_users if u[4] == "pending"])
approved = len([u for u in all_users if u[4] == "approved"])
rejected = len([u for u in all_users if u[4] == "rejected"])

with col1:
    st.metric("Total Users", total_users)

with col2:
    st.metric("Pending", pending)

with col3:
    st.metric("Approved", approved)

with col4:
    st.metric("Rejected", rejected)