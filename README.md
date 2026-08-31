<<<<<<< HEAD
# ⚡ Ar3s Kişisel Portfolyo & Bio Link Sitesi

Bu proje, tamamen kişiselleştirilebilir, animasyonlu parçacık arka planı, müzik çaları, cam efekti (glassmorphism), Discord canlı durum entegrasyonu ve güçlü bir **Yönetici Paneli** içeren kişisel portfolyo ve bio link web sitesidir.

---

## ✨ Özellikler

- 🌟 **Ar3s Estetiği & Glassmorphism**: Ultra modern koyu tema, özel neon imleç ve tıklandığında çıkan parıltı efektleri.
- 🔒 **Gelişmiş Yönetici Paneli (`/admin`)**:
  - Profil bilgileri (Görünen isim, `@kullanıcı_adı`, biyografi, konum, meslek, unvan)
  - **Daktilo Animasyon Metinleri** (Sırayla yazılan sloganlar)
  - **Doğrudan Medya / Dosya Yükleme** (Avatar, Banner, Arka plan videosu/resmi ve MP3 yükleme)
  - **Sosyal Medya Linkleri Yönetimi** (Discord, GitHub, Spotify, Instagram, X/Twitter, Steam, Telegram, YouTube, vb.)
  - **Özel Butonlar & Proje Vitrini** (Açıklamalı, rozetli ve tıklama sayaçlı bağlantılar)
  - **Özel Rozet Sistemi (Badges)** (Verified, Developer, VIP, OG, vb. tooltip açıklamalarıyla)
  - **Müzik & Ses Çalar** (Girişte otomatik başlatma, ses dalgası animasyonu, dönen plak efekti, ses seviyesi ayarı)
  - **Tema & Görsel Özelleştirme** (Yıldız Parçacıkları, Kar Yağışı, Matrix Kodu, Video / GIF Arka Planı, renk paleti ve kart bulanıklığı ayarları)
  - **Discord Lanyard Entegrasyonu** (Canlı Discord durumu ve anlık Spotify şarkısı gösterimi)
  - **Tıklama & Ziyaretçi İstatistikleri**
- 🛡️ **Güvenlik**: SHA-256 şifreli yönetici girişi ve oturum kontrolü.

---

## 🚀 Hızlı Başlangıç

### 1. Gereksinimler
- Python 3.8 veya üzeri
- `pip install -r requirements.txt`

### 2. Uygulamayı Çalıştırma
```bash
python app.py
```

Tarayıcınızda açın:
- **Portfolyo Siteniz:** [http://127.0.0.1:5000](http://127.0.0.1:5000)
- **Yönetici Girişi:** [http://127.0.0.1:5000/admin](http://127.0.0.1:5000/admin) veya [http://127.0.0.1:5000/login](http://127.0.0.1:5000/login)

---

## 📂 Dosya Yapısı

```
site/
├── app.py                  # Flask Backend & REST API
├── portfolio.db            # SQLite Veritabanı
├── requirements.txt        # Python Bağımlılıkları
├── static/
│   └── uploads/            # Yüklenen avatar, banner ve müzik dosyaları
├── templates/
│   ├── index.html          # Ar3s Portfolyo Ana Sayfası
│   ├── admin.html          # Yönetici Paneli
│   └── login.html          # Giriş Sayfası
└── README.md
```
=======
# ar3s-bio
>>>>>>> 87e00f7fdac25366926960ce64e9c54d9b59ead9
