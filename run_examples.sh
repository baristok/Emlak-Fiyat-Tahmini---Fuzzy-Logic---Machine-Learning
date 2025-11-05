#!/bin/bash

# Emlak Fiyat Tahmini - Calistirma Script

echo ""
echo "======================================================================"
echo " EMLAK FIYAT TAHMINI"
echo "======================================================================"
echo ""

# Virtual environment aktif et
source venv/bin/activate

# Hangi modeli calistirmak istediginizi soralim
echo "Hangi modeli calistirmak istiyorsunuz?"
echo ""
echo "1) Fuzzy Logic Model (Bulanik Mantik)"
echo "2) Machine Learning Model (Random Forest + Link Onerisi)"
echo "3) Karsilastirma (Her iki model)"
echo "4) Cikis"
echo ""
read -p "Seciminiz (1-4): " secim

case $secim in
    1)
        echo ""
        echo "Fuzzy model baslatiliyor..."
        echo ""
        python fuzzy_model.py
        ;;
    2)
        echo ""
        echo "ML model baslatiliyor..."
        echo ""
        python ml_model.py
        ;;
    3)
        echo ""
        echo "Karsilastirma baslatiliyor..."
        echo ""
        python karsilastir.py
        ;;
    4)
        echo ""
        echo "Cikis yapiliyor..."
        exit 0
        ;;
    *)
        echo ""
        echo "Gecersiz secim!"
        exit 1
        ;;
esac

echo ""
echo "======================================================================"
echo "Islem tamamlandi"
echo "======================================================================"
