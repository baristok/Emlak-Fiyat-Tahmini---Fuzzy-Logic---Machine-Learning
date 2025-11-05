#!/bin/bash

# Emlak Fiyat Tahmini API Başlatma Scripti

echo "=========================================="
echo " EMLAK FİYAT TAHMİNİ API BAŞLATILIYOR"
echo "=========================================="

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "📦 Sanal ortam bulunamadı. Oluşturuluyor..."
    python3 -m venv venv
fi

# Activate virtual environment
echo "🔧 Sanal ortam aktifleştiriliyor..."
source venv/bin/activate

# Install dependencies
echo "📥 Bağımlılıklar yükleniyor..."
pip install -r requirements_api.txt

# Check if CSV file exists
if [ ! -f "sehir_file/emlakverileri.csv" ]; then
    echo "❌ HATA: emlakverileri.csv dosyası bulunamadı!"
    echo "Lütfen sehir_file/ dizininde emlakverileri.csv dosyasının olduğundan emin olun."
    exit 1
fi

echo ""
echo "=========================================="
echo "✅ Hazırlık tamamlandı!"
echo "🚀 API sunucusu başlatılıyor..."
echo ""
echo "📖 API Dokümantasyonu:"
echo "   http://localhost:8000/docs"
echo ""
echo "⏹️  Durdurmak için: CTRL+C"
echo "=========================================="
echo ""

# Start the API server
python api_server.py

