# MulaiBisnis - Teman Diskusi Kewirausahaan

**MulaiBisnis** adalah aplikasi berbasis AI yang dirancang untuk membantu Anda memahami dunia kewirausahaan dengan lebih mendalam. Platform ini menyediakan mentoring interaktif, analisis proposal bisnis, dan berbagai sumber daya pembelajaran.

## 🎯 Fitur Utama

### 1. **Login & Sign Up**
- User baru dapat mendaftar dengan username, email, dan password
- Sistem approval admin untuk validasi pengguna baru
- Status account: pending → approved/rejected

### 2. **Admin Dashboard**
- Kelola pengajuan pendaftaran user
- Approve atau reject user dengan catatan
- Lihat riwayat approval
- Kelola akses admin
- Dashboard statistik pengguna

### 3. **Teman Diskusi Kewirausahaan (TEDI)**
- Mentor AI interaktif dengan pengalaman 25+ tahun di bidang entrepreneurship
- Chat dengan mentor untuk diskusi mendalam tentang bisnis
- Pertanyaan probing yang membantu berpikir kritis

### 4. **Analisis Proposal Bisnis**
- Upload file PDF proposal bisnis
- Analisis mendalam oleh mentor AI
- Evaluasi validasi ide, model bisnis, strategi go-to-market
- Identifikasi kekuatan, kelemahan, peluang, dan ancaman (SWOT)
- Rekomendasi actionable untuk perbaikan

## 🚀 Cara Memulai

### Prerequisites
- Python 3.8+
- pip (Python package manager)

### Installation

1. **Clone repository**
```bash
git clone <repository-url>
cd MulaiBisnisTEDI
```

2. **Install dependencies**
```bash
pip install -r requirements.txt
```

3. **Setup environment variables**
Buat file `.streamlit/secrets.toml`:
```toml
GROQ_API_KEY = "your_groq_api_key_here"
```

4. **Run aplikasi**
```bash
streamlit run login.py
```

## 📋 Struktur File

```
MulaiBisnisTEDI/
├── login.py                 # Halaman login & sign-up
├── auth.py                  # Sistem autentikasi & database
├── admin_dashboard.py       # Dashboard admin untuk approval
├── MulaiBisnis.py          # Aplikasi utama (TEDI Mentor)
├── requirements.txt        # Dependencies
└── mulai_bisnis.db        # Database (auto-generated)
```

## 💻 Alur Penggunaan

### Untuk User Baru:
1. Buka aplikasi → Tab "Sign Up"
2. Isi form dengan data lengkap
3. Submit pendaftaran
4. Tunggu persetujuan dari admin
5. Setelah disetujui, login dan akses TEDI Mentor

### Untuk Admin:
1. Login dengan akun admin
2. Buka Admin Dashboard
3. Lihat "Pending Approvals"
4. Approve atau reject dengan catatan
5. Kelola user dan permission di tab "All Users"

### Untuk User yang Sudah Approve:
1. Login dengan username & password
2. Akses TEDI Mentor untuk diskusi
3. Upload proposal bisnis untuk analisis

## 🛠️ Teknologi

- **Frontend**: Streamlit
- **Backend**: Python
- **Database**: SQLite3
- **AI Model**: LangChain + Groq API (Llama 3.3 70B)
- **PDF Processing**: PyPDF

## 🔐 Keamanan

- Password di-hash menggunakan SHA256
- Sistem approval untuk kontrol akses
- Role-based access (User vs Admin)
- Session management dengan Streamlit

## 📞 Support

Untuk pertanyaan atau masalah, silakan hubungi admin melalui email atau platform support.

## 📄 License

Project ini adalah bagian dari inisiatif pembelajaran TEDI.

---

**Selamat memulai perjalanan entrepreneurship Anda dengan MulaiBisnis! 💰**
