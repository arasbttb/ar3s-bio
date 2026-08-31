# 🚀 GitHub & Deployment Rehberi - Adım Adım

Bu dokümanda sana GitHub'a yüklemek ve canlı ortama deploy etmek için gerekli tüm adımları anlatacağım.

## 1️⃣ GitHub Repository Oluştur

### Adım 1: GitHub Hesabı Aç

1. **https://github.com** adresine git
2. Sağ üstte **"Sign Up"** tıkla
3. Email, password ve username belirle
4. Doğrulama işlemini tamamla

### Adım 2: Yeni Repository Oluştur

1. GitHub'a giriş yap
2. Sağ üstte **"+"** simgesine tıkla
3. **"New repository"** seç
4. Repository adı: `gunstore` (veya istediğin ad)
5. Description: `GunStore - Modern Silah Mağazası Yönetim Sistemi`
6. **"Public"** seçeneğini işaretle (böylece herkes görebilir)
7. **"Initialize this repository with a README"** işaretle
8. **"Create repository"** tıkla

✅ Repository oluşturuldu!

---

## 2️⃣ Bilgisayarında Git Kur

### Windows:
1. https://git-scm.com/download/win indir
2. İndirileni çalıştır
3. "Install" tıkla ve tamamla

### macOS:
```bash
# Terminal'i aç ve yaz:
brew install git
```

### Linux (Ubuntu/Debian):
```bash
sudo apt-get install git
```

### Doğrulama:
```bash
git --version
```

---

## 3️⃣ Dosyaları GitHub'a Yükle

### Adım 1: Git Yapılandır

```bash
git config --global user.name "Senin Adın"
git config --global user.email "senin@email.com"
```

### Adım 2: Proje Klasörüne Git

```bash
# Windows:
cd C:\Users\Adınız\Desktop\gunstore

# macOS/Linux:
cd ~/Desktop/gunstore
```

### Adım 3: GitHub Repository'nizi Link Et

GitHub repository sayfanda **"Code"** yeşil butonuna tıkla ve HTTPS linkini kopyala. Sonra:

```bash
git remote add origin https://github.com/GITHUB_KULLANICIADI/gunstore.git
```

### Adım 4: Dosyaları Hazırla ve Yükle

```bash
# Tüm dosyaları sahnele
git add .

# Commit et (kaydını yaz)
git commit -m "GunStore ilk version"

# GitHub'a gönder
git push -u origin main
```

✅ Dosyaların GitHub'da olması gerekir!

---

## 4️⃣ Vercel'de Deploy Et (Önerilir)

**Vercel**, Python Flask uygulamalarını ücretsiz olarak host edebilir ve GitHub'dan otomatik olarak deploy eder.

### Adım 1: Vercel Hesabı Oluştur

1. **https://vercel.com** adresine git
2. **"Sign Up"** tıkla
3. **"GitHub ile başla"** seçeneğini seç
4. GitHub hesabını yetkilendir
5. Proje adını belirle

### Adım 2: Repository'i Seç

1. Vercel dashboard'da **"Import Project"** tıkla
2. GitHub repository'ni seç (`gunstore`)
3. **"Import"** tıkla

### Adım 3: Ayarlar

- **Environment Variables**: Boş bırak (şimdilik)
- **Framework Preset**: "Other" seç
- **Root Directory**: `.` bırak
- **Build Command**: `pip install -r requirements.txt`
- **Output Directory**: Boş bırak
- **Install Command**: `pip install -r requirements.txt`

### Adım 4: Deploy Et

1. **"Deploy"** butonuna tıkla
2. Vercel uygulamayı deploy eder (2-3 dakika)
3. **Deployment complete!** yazısını görünce, sana verilen URL'ye tıkla

✅ Sited canlıda! 🎉

**Örnek URL:** https://gunstore.vercel.app

### Otomatik Deployment

Artık GitHub'a her push yaptığında Vercel otomatik olarak deploy eder!

```bash
# Değişiklik yap, sonra:
git add .
git commit -m "Admin panelini güncelle"
git push
# Vercel otomatik deploy eder!
```

---

## 5️⃣ Heroku'da Deploy Et (Alternatif)

### Adım 1: Heroku Hesabı Oluştur

1. **https://www.heroku.com** adresine git
2. **"Sign Up"** tıkla
3. Email ve password belirle

### Adım 2: Heroku CLI Yükle

https://devcenter.heroku.com/articles/heroku-cli adresinden indir ve kur.

Doğrulama:
```bash
heroku --version
```

### Adım 3: Proje Dosyasına Git

```bash
cd ~/Desktop/gunstore
```

### Adım 4: Heroku'ya Giriş Yap

```bash
heroku login
```

Tarayıcı açılır, login yap.

### Adım 5: Uygulama Oluştur

```bash
heroku create gunstore-uygulama-adi
```

(Uygulama adı benzersiz olmalı)

### Adım 6: Deploy Et

```bash
git push heroku main
```

✅ Deploy bitti!

**URL:** https://gunstore-uygulama-adi.herokuapp.com

---

## 6️⃣ Render'da Deploy Et (Alternatif 2)

### Adım 1: Render Hesabı Oluştur

1. **https://render.com** adresine git
2. **"Sign up"** tıkla
3. GitHub ile bağlan

### Adım 2: Yeni Service Oluştur

1. Dashboard'da **"New +"** tıkla
2. **"Web Service"** seç
3. GitHub repository'ni seç

### Adım 3: Ayarlar

| Ayar | Değer |
|------|-------|
| Name | gunstore |
| Environment | Python 3 |
| Build Command | `pip install -r requirements.txt` |
| Start Command | `gunicorn app:app` |

### Adım 4: Deploy

1. **"Create Web Service"** tıkla
2. Render deploy eder
3. URL sana verilir

---

## 🔄 GitHub'dan Canlı Site'ye Otomatik Update

### Vercel (En Kolay)

GitHub'a push → Vercel otomatik deploy eder. Başka bir şey yapmana gerek yok!

### Heroku

GitHub'a push → Manuel olarak:
```bash
git push heroku main
```

### Render

GitHub'a push → Render otomatik deploy eder (ayarlandıysa).

---

## 📱 Siteni Kontrol Et

Deploy ettikten sonra:

1. Verilen URL'ye git
2. Ana sayfa yüklenmeli
3. `/admin` sayfasına git
4. Admin hesap oluştur (ilk kez)
5. Ürün ekle ve test et

---

## 🔐 Production Ayarları

Deploy etmeden önce app.py'de bu değişiklikleri yap:

```python
# DEBUG mode kapat (production'da zararlı)
app.run(debug=False)  # debug=True yerine

# Secret key güvenli yap
import os
app.secret_key = os.environ.get('SECRET_KEY', 'change-this-in-production')
```

### Vercel'de Secret Key Ayarla

1. Vercel dashboard > Project settings
2. "Environment Variables" seç
3. Ekle:
   - **Name:** `SECRET_KEY`
   - **Value:** (güvenli bir string, örn: "super-secret-key-1234567890")
4. "Save"

---

## 📊 Canlı Siteni Kontrol Et

Deploy ettikten sonra:

✅ **https://gunstore.vercel.app** (veya senin URL'in)

Kontrol listesi:
- [ ] Ana sayfa yükleniyor
- [ ] Ürünler gösteriyor
- [ ] Admin paneline girebiliyorum
- [ ] Ürün ekleyebiliyorum
- [ ] Ürünü düzenleyebiliyorum
- [ ] Ürünü silebiliyorum
- [ ] Arama çalışıyor

---

## 🐛 Sorunlar

### "Build failed"

```bash
# requirements.txt'i kontrol et
cat requirements.txt

# Eksik paket varsa ekle
echo "Werkzeug==3.0.1" >> requirements.txt
git add .
git commit -m "Fix: Eksik paketleri ekle"
git push
```

### "Internal Server Error"

1. Proje ayarlarını kontrol et
2. Database file'ı silme (sunucuda otomatik oluşturulur)
3. Logs'a bak (Dashboard > Logs)

### "Repository not found"

```bash
# URL'i kontrol et
git remote -v

# Yanlışsa değiştir
git remote remove origin
git remote add origin https://github.com/KULLANICI/gunstore.git
```

---

## 💡 İleri İpuçları

### Custom Domain Ekle

1. Vercel Settings > Domains
2. Domain ekle (örn: gunstore.com)
3. DNS ayarlarını yapılandır

### Environment Variables

```python
# app.py'de
import os
DATABASE = os.environ.get('DATABASE_URL', 'gunstore.db')
SECRET_KEY = os.environ.get('SECRET_KEY')
```

### Backup Al

```bash
# Veritabanını git'e ekleme (üretim için)
echo "*.db" >> .gitignore
git add .gitignore
git commit -m "Database'i exclude et"
git push
```

---

## ✨ Tamamlandı!

Artık senin canlı, çalışan admin panelli GunStore sitin var!

- 📱 Mobil uyumlu
- 🔐 Şifreli giriş
- 🚀 Dünya çapında erişim
- ⚡ Hızlı performance

**Sayfayı paylaş:** https://gunstore.vercel.app (senin URL'in)

---

## 📞 Yardım Kaynakları

- **Vercel Dokümanı:** https://vercel.com/docs
- **Heroku Dokümanı:** https://devcenter.heroku.com
- **Render Dokümanı:** https://render.com/docs
- **Git Rehberi:** https://git-scm.com/book

---

**Son güncelleme:** 2024  
**Versiyon:** 1.0.0
