<div align="center">

# 🏠 Emlak Fiyat Tahmini - Fuzzy Logic & Machine Learning

**Fuzzy Logic ve Machine Learning modellerini kullanarak emlak fiyat tahmini yapan Python projesi. FastAPI ile RESTful API servisi sunar.**

[![Python](https://img.shields.io/badge/Python-3.12+-3776AB?logo=python&logoColor=white)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.104-009688?logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com/)
[![Fuzzy Logic](https://img.shields.io/badge/Fuzzy-Scikit--fuzzy-FF6F00?logo=scipy&logoColor=white)](https://pythonhosted.org/scikit-fuzzy/)
[![Machine Learning](https://img.shields.io/badge/ML-Scikit--learn-F7931E?logo=scikit-learn&logoColor=white)](https://scikit-learn.org/)
[![License](https://img.shields.io/badge/License-Educational-red)](LICENSE)

> ⚠️ **Eğitim Amaçlı Proje**: Bu proje yalnızca eğitim ve öğrenme amaçlı geliştirilmiştir.

</div>

---

## 📑 İçindekiler

- [🚨 Önemli Uyarılar](#-önemli-uyarılar)
- [✨ Özellikler](#-özellikler)
- [📸 Ekran Görüntüleri](#-ekran-görüntüleri)
- [🛠️ Kurulum](#️-kurulum)
- [📖 Kullanım](#-kullanım)
- [🔧 Teknik Detaylar](#-teknik-detaylar)
- [📊 API Dokümantasyonu](#-api-dokümantasyonu)
- [🐛 Sorun Giderme](#-sorun-giderme)
- [📝 Lisans ve Sorumluluk](#-lisans-ve-sorumluluk)
- [🤝 Katkıda Bulunma](#-katkıda-bulunma)

---

## 🚨 Önemli Uyarılar

<div align="center">

⚠️ **LÜTFEN DİKKATLİ OKUYUN** ⚠️

</div>

| Uyarı | Açıklama |
|-------|----------|
| 🎓 **Eğitim Amaçlı** | Bu proje sadece Fuzzy Logic ve Machine Learning tekniklerini öğrenmek için geliştirilmiştir. |
| 📊 **Tahmin Doğruluğu** | Model tahminleri yalnızca referans amaçlıdır. Gerçek emlak işlemlerinde profesyonel değerleme yapılmalıdır. |
| ⚡ **Veri Kalitesi** | Model performansı veri setinin kalitesine ve güncelliğine bağlıdır. Eski veriler yanlış tahminlere yol açabilir. |
| 📜 **Kullanım Sorumluluğu** | Bu modelin tahminlerine dayanarak yatırım kararları alınmamalıdır. **Sorumluluk kullanıcıya aittir**. |
| ⚖️ **Yasal Uyarı** | Bu araçtan kaynaklanan mali kayıplardan veya yanlış kararlardan **geliştirici sorumlu değildir**. |

---

## ✨ Özellikler

<table>
<tr>
<td width="50%">

### 🔮 Fuzzy Logic Modeli
- 🧠 **30+ Fuzzy Kural**: Gelişmiş bulanık mantık kuralları
- 📐 **6 Giriş Değişkeni**: Metrekare, oda, yaş, kat, ısıtma
- 🎯 **Dinamik Tahmin**: Gerçek zamanlı fiyat tahmini
- 📊 **İstatistiksel Analiz**: Veri seti bazlı istatistikler

</td>
<td width="50%">

### 🤖 Machine Learning Modeli
- 🌳 **Random Forest**: Ensemble learning algoritması
- 📈 **Yüksek Performans**: 2043 kayıt ile eğitilmiş model
- 🔍 **Benzer Ev Bulma**: KNN ile benzer emlak bulma
- 📊 **Model Metrikleri**: MAE, RMSE, R² skorları

</td>
</tr>
<tr>
<td width="50%">

### 🌐 RESTful API
- ⚡ **FastAPI**: Modern ve hızlı API framework
- 📖 **Otomatik Dokümantasyon**: Swagger UI ve ReDoc
- 🔄 **CORS Desteği**: Cross-origin istek desteği
- 🏥 **Health Check**: Sistem sağlık kontrolü

</td>
<td width="50%">

### 📊 Karşılaştırmalı Analiz
- 🔄 **İki Model**: Fuzzy ve ML tahminlerini karşılaştırma
- 📈 **Ortalama Tahmin**: İki modelin ortalaması
- 💰 **Fark Analizi**: Tahmin farklarının yüzdesi
- 📋 **Detaylı Rapor**: Kapsamlı tahmin sonuçları

</td>
</tr>
</table>

---

## 📸 Ekran Görüntüleri

> 💡 **Not**: Ekran görüntüleri eklemek için bu bölümü düzenleyebilirsiniz.

```
[API Dokümantasyon]        [Tahmin Sonucu]        [Model Karşılaştırma]
```

### API Dokümantasyon Örneği

Swagger UI arayüzü: `http://localhost:8000/docs`

### Tahmin Sonucu Örneği

```json
{
  "fuzzy_tahmin": 3500000.0,
  "ml_tahmin": 3450000.0,
  "ortalama_tahmin": 3475000.0,
  "m2_basina_fiyat": 28958.33
}
```

---

## 🛠️ Kurulum

### Gereksinimler

- ✅ Python 3.12+ (veya 3.10+)
- ✅ pip (Python paket yöneticisi)
- ✅ Git (projeyi klonlamak için)
- ✅ İnternet bağlantısı (paket indirmek için)

### Kurulum Adımları

<details>
<summary><b>📋 Detaylı Kurulum Rehberi</b></summary>

#### 1. Projeyi İndirin

```bash
git clone https://github.com/kullanici-adi/fuzzy_model.git
cd fuzzy_model
```

#### 2. Sanal Ortam Oluşturun

**Linux/Mac:**
```bash
python3 -m venv venv
source venv/bin/activate
```

**Windows:**
```bash
python -m venv venv
venv\Scripts\activate
```

#### 3. Bağımlılıkları Yükleyin

**Temel model için:**
```bash
pip install -r requirements.txt
```

**API servisi için (tüm bağımlılıklar):**
```bash
pip install -r requirements_api.txt
```

#### 4. Veri Dosyasını Kontrol Edin

`sehir_file/emlakverileri.csv` dosyasının mevcut olduğundan emin olun.

**Dosya yapısı:**
- Fiyat
- Oda Sayısı
- Brüt m²
- Kat Sayısı
- Bulunduğu Kat
- Bina Yaşı
- Isınma Tipi

#### 5. Kurulumu Test Edin

```bash
# Fuzzy model testi
python fuzzy_model.py
# (q tuşu ile çıkış)

# API testi
python api_server.py
# Tarayıcıda: http://localhost:8000/docs
```

</details>

### Hızlı Kurulum

```bash
# 1. Projeyi klonlayın
git clone https://github.com/kullanici-adi/fuzzy_model.git
cd fuzzy_model

# 2. Sanal ortam oluşturun ve aktifleştirin
python3 -m venv venv
source venv/bin/activate  # Linux/Mac
# veya
venv\Scripts\activate  # Windows

# 3. Bağımlılıkları yükleyin
pip install -r requirements_api.txt

# 4. API'yi başlatın
./start_api.sh
# veya
python api_server.py
```

---

## 📖 Kullanım

### 🎯 Hızlı Başlangıç

<details>
<summary><b>📝 Adım Adım Kullanım Kılavuzu</b></summary>

#### 1️⃣ Komut Satırı (CLI) Kullanımı

**Fuzzy Logic modeli ile interaktif tahmin:**

```bash
python fuzzy_model.py
```

**Örnek kullanım:**
```
Metrekare: 120
Oda sayisi: 3
Bina yasi: 5
Bulundugu kat: 3
Bina kat sayisi: 8
Isitma skoru: 5

TAHMIN: 3,500,000 TL
M2 basina: 29,167 TL/m2
```

#### 2️⃣ API Servisi Kullanımı

**API'yi başlatın:**
```bash
# Otomatik script ile
./start_api.sh

# Veya manuel olarak
python api_server.py
```

**API adresi:** `http://localhost:8000`

**Dokümantasyon:**
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

#### 3️⃣ API ile Tahmin Yapma

**cURL ile:**
```bash
curl -X POST "http://localhost:8000/predict" \
  -H "Content-Type: application/json" \
  -d '{
    "metrekare": 120,
    "oda_sayisi": 3,
    "bina_yasi": 5,
    "bulundugu_kat": 3,
    "bina_kat_sayisi": 8,
    "isitma_tipi": 5
  }'
```

**Python ile:**
```python
import requests

response = requests.post(
    "http://localhost:8000/predict",
    json={
        "metrekare": 120,
        "oda_sayisi": 3,
        "bina_yasi": 5,
        "bulundugu_kat": 3,
        "bina_kat_sayisi": 8,
        "isitma_tipi": 5
    }
)

print(response.json())
```

**JavaScript ile:**
```javascript
fetch('http://localhost:8000/predict', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json',
  },
  body: JSON.stringify({
    metrekare: 120,
    oda_sayisi: 3,
    bina_yasi: 5,
    bulundugu_kat: 3,
    bina_kat_sayisi: 8,
    isitma_tipi: 5
  })
})
.then(response => response.json())
.then(data => console.log(data));
```

</details>

### 📊 Girdi Parametreleri

| Parametre | Açıklama | Aralık | Örnek |
|-----------|----------|--------|-------|
| **metrekare** | Brüt metrekare | 40-350 m² | 120 |
| **oda_sayisi** | Toplam oda sayısı | 1-10 | 3 |
| **bina_yasi** | Bina yaşı (yıl) | 0-60 | 5 |
| **bulundugu_kat** | Dairenin bulunduğu kat | -1 ile 20 | 3 |
| **bina_kat_sayisi** | Binanın toplam kat sayısı | 1-25 | 8 |
| **isitma_tipi** | Isıtma tipi skoru | 0-10 | 5 |

### 🔥 Isıtma Tipi Skorları

| Skor | Isıtma Tipi | Açıklama |
|------|-------------|----------|
| 0 | Isıtma Yok | Isıtma sistemi yok |
| 1 | Soba | Kömür/odun sobası |
| 2 | Doğalgaz Sobası | Doğalgaz sobası |
| 4 | Kat Kaloriferi | Kat bazlı kalorifer |
| 5 | Kombi | Bireysel kombi |
| 6 | Merkezi | Merkezi ısıtma |
| 8 | Klima | Klima ile ısıtma |
| 9 | Yerden Isıtma | Yerden ısıtma sistemi |
| 10 | Güneş Enerjisi | Güneş enerjisi sistemi |

---

## 🔧 Teknik Detaylar

### 📁 Proje Yapısı

```
fuzzy_model/
│
├── 📄 api_server.py          # FastAPI RESTful API servisi
├── 🔮 fuzzy_model.py         # Fuzzy Logic model implementasyonu
├── 🤖 ml_model.py            # Random Forest ML modeli
├── 📊 veri_analiz.py         # Veri analizi ve görselleştirme
├── ⚖️ karsilastir.py         # Model karşılaştırma scripti
├── 📦 requirements.txt       # Temel Python bağımlılıkları
├── 🌐 requirements_api.txt  # API için ek bağımlılıklar
├── 🚀 start_api.sh          # API başlatma scripti (Bash)
├── 🏃 run_examples.sh       # Örnek kullanım scriptleri
├── 📖 README.md             # Bu dosya
├── 🚫 .gitignore            # Git ignore dosyası
│
├── 📁 sehir_file/
│   └── 📊 emlakverileri.csv # Veri seti (2043 kayıt)
│
└── 📁 venv/                 # Python sanal ortam (gitignore'da)
```

### 🔄 Çalışma Prensibi

```
┌─────────────┐
│   Kullanıcı │
│   (Girdi)   │
└──────┬──────┘
       │
       ▼
┌─────────────────────────────────────┐
│         FastAPI Server              │
│  (http://localhost:8000)           │
└──────┬──────────────────┬───────────┘
       │                  │
       ▼                  ▼
┌──────────────┐  ┌──────────────────┐
│ Fuzzy Logic  │  │ Machine Learning│
│   Model      │  │  (Random Forest)│
└──────┬───────┘  └────────┬─────────┘
       │                   │
       └─────────┬─────────┘
                 ▼
          ┌──────────────┐
          │   Tahmin     │
          │   Sonucu     │
          └──────────────┘
```

**Akış Şeması:**

1. **Kullanıcı Girdisi**: API'ye emlak özellikleri gönderilir
2. **Veri İşleme**: Girdiler doğrulanır ve normalize edilir
3. **Fuzzy Logic Tahmini**: Bulanık mantık kuralları ile tahmin
4. **ML Tahmini**: Random Forest modeli ile tahmin
5. **Sonuç Birleştirme**: İki tahmin karşılaştırılır ve ortalaması alınır
6. **Response**: JSON formatında detaylı sonuç döner

### ⚡ Model Özellikleri

<table>
<tr>
<th>Model</th>
<th>Algoritma</th>
<th>Özellikler</th>
<th>Performans</th>
</tr>
<tr>
<td><b>Fuzzy Logic</b></td>
<td>Mamdani Inference</td>
<td>6 giriş, 30+ kural</td>
<td>İstatistiksel tabanlı</td>
</tr>
<tr>
<td><b>Machine Learning</b></td>
<td>Random Forest</td>
<td>6 özellik, 2043 kayıt</td>
<td>R², MAE, RMSE metrikleri</td>
</tr>
</table>

### 🛠️ Teknolojiler

| Teknoloji | Versiyon | Kullanım Amacı |
|-----------|----------|----------------|
| **Python** | 3.12+ | Ana programlama dili |
| **FastAPI** | 0.104.1 | RESTful API framework |
| **scikit-fuzzy** | 0.5.0 | Fuzzy Logic implementasyonu |
| **scikit-learn** | 1.7.2 | Machine Learning algoritmaları |
| **pandas** | 2.3.3 | Veri işleme ve analiz |
| **numpy** | 2.3.4 | Sayısal hesaplamalar |
| **uvicorn** | 0.24.0 | ASGI server |

### 📊 Fuzzy Logic Model Detayları

**Giriş Değişkenleri:**

| Değişken | Aralık | Üyelik Fonksiyonları |
|----------|--------|---------------------|
| Metrekare | 40-350 m² | Küçük, Orta, Büyük |
| Oda Sayısı | 1-10 | Az, Orta, Çok |
| Bina Yaşı | 0-60 | Yeni, Orta, Eski |
| Bulunduğu Kat | -1 ile 20 | Alt, Orta, Yüksek |
| Bina Kat Sayısı | 1-25 | Az Katlı, Orta, Çok Katlı |
| Isıtma Tipi | 0-10 | Zayıf, Orta, İyi |

**Çıkış Değişkeni:**

| Değişken | Aralık | Üyelik Fonksiyonları |
|----------|--------|---------------------|
| Tahmini Fiyat | 500K-20M TL | Çok Düşük, Düşük, Orta, Yüksek, Çok Yüksek |

**Fuzzy Kurallar Örneği:**

```python
# Yüksek fiyat kuralları
IF metrekare = büyük AND oda_sayisi = çok AND 
   bina_yasi = yeni AND isitma_tipi = iyi AND 
   bulundugu_kat = yuksek
THEN tahmini_fiyat = çok_yuksek
```

---

## 📊 API Dokümantasyonu

### 🌐 Endpoints

| Endpoint | Method | Açıklama | Request Body |
|----------|--------|----------|--------------|
| `/` | GET | API bilgileri ve endpoint listesi | - |
| `/health` | GET | Sistem sağlık kontrolü | - |
| `/predict` | POST | Her iki modelle tahmin (Fuzzy + ML) | EmlakOzellikleri |
| `/predict/fuzzy` | POST | Sadece Fuzzy Logic tahmini | EmlakOzellikleri |
| `/predict/ml` | POST | Sadece Machine Learning tahmini | EmlakOzellikleri |
| `/stats` | GET | Veri seti istatistikleri | - |
| `/isitma-tipleri` | GET | Isıtma tipi skorları listesi | - |

### 📥 Request Format

```json
{
  "metrekare": 120,
  "oda_sayisi": 3,
  "bina_yasi": 5,
  "bulundugu_kat": 3,
  "bina_kat_sayisi": 8,
  "isitma_tipi": 5
}
```

### 📤 Response Format

**Combined Prediction (`/predict`):**

```json
{
  "fuzzy_tahmin": 3500000.0,
  "ml_tahmin": 3450000.0,
  "ortalama_tahmin": 3475000.0,
  "fark": 50000.0,
  "fark_yuzde": 1.43,
  "m2_basina_fiyat": 28958.33,
  "benzer_evler": [
    {
      "url": "https://...",
      "fiyat": 3400000.0,
      "metrekare": 118.0,
      "oda": 3,
      "yas": 6
    }
  ]
}
```

**Fuzzy Only (`/predict/fuzzy`):**

```json
{
  "model": "Fuzzy Logic",
  "tahmin": 3500000.0,
  "m2_basina_fiyat": 29166.67,
  "ozellikler": {...}
}
```

**ML Only (`/predict/ml`):**

```json
{
  "model": "Random Forest (ML)",
  "tahmin": 3450000.0,
  "m2_basina_fiyat": 28750.0,
  "ozellikler": {...},
  "benzer_evler": [...]
}
```

**Statistics (`/stats`):**

```json
{
  "veri_sayisi": 2043,
  "medyan_fiyat": 3500000.0,
  "medyan_m2": 120.0,
  "fiyat_min": 500000.0,
  "fiyat_max": 15000000.0
}
```

### 🔍 Örnek Kullanım Senaryoları

<details>
<summary><b>Senaryo 1: Yeni Daire Tahmini</b></summary>

**Girdi:**
- Metrekare: 150
- Oda: 4
- Bina Yaşı: 0 (Sıfır)
- Kat: 5
- Kat Sayısı: 10
- Isıtma: 9 (Yerden Isıtma)

**Beklenen:** Yüksek fiyat tahmini

</details>

<details>
<summary><b>Senaryo 2: Eski Daire Tahmini</b></summary>

**Girdi:**
- Metrekare: 80
- Oda: 2
- Bina Yaşı: 30
- Kat: 0 (Zemin)
- Kat Sayısı: 3
- Isıtma: 1 (Soba)

**Beklenen:** Düşük fiyat tahmini

</details>

---

## 🐛 Sorun Giderme

### ❓ Sık Karşılaşılan Sorunlar

<details>
<summary><b>Model yüklenemiyor / Import hatası</b></summary>

**Hata:**
```
ModuleNotFoundError: No module named 'skfuzzy'
```

**Çözümler:**
1. Sanal ortamın aktif olduğundan emin olun:
   ```bash
   source venv/bin/activate  # Linux/Mac
   venv\Scripts\activate  # Windows
   ```

2. Bağımlılıkları yeniden yükleyin:
   ```bash
   pip install -r requirements_api.txt
   ```

3. Python versiyonunu kontrol edin (3.10+ gerekli):
   ```bash
   python --version
   ```

</details>

<details>
<summary><b>CSV dosyası bulunamıyor</b></summary>

**Hata:**
```
FileNotFoundError: sehir_file/emlakverileri.csv
```

**Çözümler:**
1. Dosya yolunu kontrol edin:
   ```bash
   ls sehir_file/emlakverileri.csv
   ```

2. Dosya mevcut değilse, veri setini ekleyin

3. Çalışma dizinini kontrol edin:
   ```bash
   pwd  # Proje kök dizininde olmalısınız
   ```

</details>

<details>
<summary><b>API başlatılamıyor</b></summary>

**Hata:**
```
Port 8000 already in use
```

**Çözümler:**
1. Port'u değiştirin:
   ```python
   uvicorn.run(app, host="0.0.0.0", port=8001)
   ```

2. Kullanan process'i bulun ve kapatın:
   ```bash
   # Linux/Mac
   lsof -ti:8000 | xargs kill
   
   # Windows
   netstat -ano | findstr :8000
   taskkill /PID <PID> /F
   ```

</details>

<details>
<summary><b>Tahmin sonuçları mantıksız</b></summary>

**Sorun:** Çok yüksek veya düşük tahminler

**Çözümler:**
1. Girdi parametrelerinin aralık içinde olduğunu kontrol edin
2. Veri setinin güncel olduğundan emin olun
3. Modeli yeniden eğitin (ML modeli için)
4. Fuzzy kurallarını gözden geçirin

</details>

<details>
<summary><b>API yanıt vermiyor</b></summary>

**Sorun:** API istekleri timeout oluyor

**Çözümler:**
1. Model yükleme süresini kontrol edin (ilk başlatmada uzun sürebilir)
2. `/health` endpoint'ini kontrol edin:
   ```bash
   curl http://localhost:8000/health
   ```

3. Console loglarını kontrol edin
4. Bellek kullanımını kontrol edin

</details>

### 📞 Daha Fazla Yardım

Sorun yaşıyorsanız:

1. **GitHub Issues**: Benzer bir sorun var mı kontrol edin
2. **Yeni Issue**: Detaylı bilgi ile yeni issue açın:
   - Python versiyonu
   - İşletim sistemi
   - Hata mesajı (tam)
   - Adımlar (reproduce için)
3. **Console Logs**: `api_server.py` çalıştırırken console çıktılarını kontrol edin

---

## 📝 Lisans ve Sorumluluk

### ⚖️ Yasal Uyarı

Bu proje **eğitim amaçlı** geliştirilmiştir. Kullanıcılar:

- ✅ Model tahminlerinden kendileri sorumludur
- ✅ Gerçek emlak işlemlerinde profesyonel değerleme yapılmalıdır
- ✅ Bu araçtan kaynaklanan mali kayıplardan geliştirici sorumlu değildir
- ❌ Model tahminlerine dayanarak yatırım kararları alınmamalıdır

### 📜 Sorumluluk Reddi

Bu yazılım "olduğu gibi" sağlanmaktadır. Yazılımın kullanımından doğan veya yazılımın kullanımı ile ilgili olarak ortaya çıkan herhangi bir zarardan (mali kayıp, yanlış karar, vb.) geliştirici sorumlu tutulamaz.

### 🎓 Eğitim Amaçlı Kullanım

Bu proje:
- ✅ Fuzzy Logic kavramlarını öğrenmek için
- ✅ Machine Learning modelleme tekniklerini anlamak için
- ✅ RESTful API geliştirme pratiği yapmak için
- ✅ Veri analizi ve modelleme süreçlerini görmek için

kullanılabilir.

---

## 🤝 Katkıda Bulunma

Bu proje eğitim amaçlıdır, ancak önerileriniz ve geri bildirimleriniz değerlidir!

### 📝 Katkı Yolları

- 🐛 **Bug Report**: Hata bulursanız issue açın
- 💡 **Öneri**: Yeni özellik önerileri için issue açın
- 📖 **Dokümantasyon**: README'yi iyileştirme önerileri
- 🔧 **Kod İyileştirme**: Pull request ile katkıda bulunun
- ⭐ **Star**: Projeyi beğendiyseniz yıldız vermeyi unutmayın!

### 🔄 Pull Request Süreci

1. **Fork** yapın
2. **Feature branch** oluşturun:
   ```bash
   git checkout -b feature/amazing-feature
   ```
3. **Commit** yapın:
   ```bash
   git commit -m 'Add amazing feature'
   ```
4. **Push** yapın:
   ```bash
   git push origin feature/amazing-feature
   ```
5. **Pull Request** açın

### 📋 Commit Mesajları

İyi commit mesajları yazın:
- ✅ `feat: Yeni özellik eklendi`
- ✅ `fix: Bug düzeltildi`
- ✅ `docs: Dokümantasyon güncellendi`
- ✅ `refactor: Kod iyileştirmesi`

---

## 📊 İstatistikler

> 💡 Bu bölüm GitHub'da otomatik olarak güncellenir.

![GitHub stars](https://img.shields.io/github/stars/kullanici-adi/fuzzy_model?style=social)
![GitHub forks](https://img.shields.io/github/forks/kullanici-adi/fuzzy_model?style=social)
![GitHub issues](https://img.shields.io/github/issues/kullanici-adi/fuzzy_model)
![GitHub license](https://img.shields.io/github/license/kullanici-adi/fuzzy_model)

---

## 📚 Ek Kaynaklar

### 📖 Öğrenme Materyalleri

- [Fuzzy Logic Nedir?](https://en.wikipedia.org/wiki/Fuzzy_logic)
- [Random Forest Algoritması](https://scikit-learn.org/stable/modules/ensemble.html#forest)
- [FastAPI Dokümantasyonu](https://fastapi.tiangolo.com/)
- [scikit-fuzzy Kullanımı](https://pythonhosted.org/scikit-fuzzy/)

### 🔗 İlgili Projeler

- [scikit-fuzzy Examples](https://github.com/scikit-fuzzy/scikit-fuzzy)
- [FastAPI Examples](https://github.com/tiangolo/fastapi/tree/master/docs_src)

---

<div align="center">

### ⭐ Bu projeyi beğendiyseniz yıldız vermeyi unutmayın!

**Not**: Bu proje, Fuzzy Logic ve Machine Learning tekniklerini öğrenmek ve RESTful API geliştirme konusunda deneyim kazanmak için oluşturulmuştur. Lütfen sorumlu bir şekilde kullanın.

Made with ❤️ for educational purposes

[⬆ Başa Dön](#-emlak-fiyat-tahmini---fuzzy-logic--machine-learning)

</div>
