"""
Fuzzy vs Makine Ogrenmesi Karsilastirma
Ayni input ile iki modeli de test eder
"""

import pandas as pd
from fuzzy_model import EmlakFuzzyModel
from ml_model import EmlakMLModel
import warnings
warnings.filterwarnings('ignore')


def main():
    """Iki modeli karsilastir"""
    print("\n" + "="*70)
    print(" FUZZY vs MAKINE OGRENMESI KARSILASTIRMA")
    print("="*70)
    
    # Veriyi yukle
    print("\nVeri yukleniyor...")
    df = pd.read_csv('sehir_file/emlakverileri.csv')
    
    # Fuzzy model
    print("\nFuzzy model olusturuluyor...")
    fuzzy_model = EmlakFuzzyModel(df=df)
    
    # ML model
    print("\nML model egitiliyor...")
    ml_model = EmlakMLModel()
    ml_model.veriyi_yukle_ve_isle()
    ml_model.model_egit()
    
    print("\n" + "="*70)
    print("Her iki model hazir! (Cikmak icin 'q' yazin)")
    print("="*70)
    
    tahmin_sayisi = 0
    
    # Ana dongu
    while True:
        print(f"\n\n{'='*70}")
        print(f" TAHMIN #{tahmin_sayisi + 1}")
        print("="*70 + "\n")
        
        try:
            # Inputlari al
            inp = input("Metrekare: ").strip()
            if inp.lower() == 'q':
                break
            metrekare = int(inp)
            
            print("(1: Studyo, 2: 1+1, 3: 2+1, 4: 3+1, ...)")
            inp = input("Oda sayisi: ").strip()
            if inp.lower() == 'q':
                break
            oda_sayisi = int(inp)
            
            print("(0: Sifir, 5: 5 yil, 10: 10 yil, ...)")
            inp = input("Bina yasi: ").strip()
            if inp.lower() == 'q':
                break
            bina_yasi = int(inp)
            
            print("(-1: Bodrum, 0: Zemin, 3: 3.kat, ...)")
            inp = input("Bulundugu kat: ").strip()
            if inp.lower() == 'q':
                break
            bulundugu_kat = int(inp)
            
            inp = input("Bina kat sayisi: ").strip()
            if inp.lower() == 'q':
                break
            bina_kat_sayisi = int(inp)
            
            print("(0: Yok, 5: Kombi, 8: Klima, 9: Yerden)")
            inp = input("Isitma skoru: ").strip()
            if inp.lower() == 'q':
                break
            isitma_tipi = int(inp)
            
            # Ozellikler
            ozellikler = {
                'metrekare': metrekare,
                'oda_sayisi': oda_sayisi,
                'bina_yasi': bina_yasi,
                'bulundugu_kat': bulundugu_kat,
                'bina_kat_sayisi': bina_kat_sayisi,
                'isitma_tipi': isitma_tipi
            }
            
            # Fuzzy tahmin
            fuzzy_tahmin = fuzzy_model.predict(ozellikler)
            
            # ML tahmin
            ml_tahmin = ml_model.predict(ozellikler)
            
            # Benzer evler
            benzer_evler = ml_model.benzer_evler_bul(ozellikler, n=3)
            
            # Sonuclari goster
            print("\n" + "="*70)
            print(" SONUCLAR")
            print("="*70)
            
            print(f"\nFuzzy Model:     {fuzzy_tahmin:,.0f} TL")
            print(f"ML Model:        {ml_tahmin:,.0f} TL")
            
            fark = abs(fuzzy_tahmin - ml_tahmin)
            yuzde_fark = (fark / fuzzy_tahmin) * 100
            print(f"\nFark:            {fark:,.0f} TL ({yuzde_fark:.1f}%)")
            
            ortalama = (fuzzy_tahmin + ml_tahmin) / 2
            print(f"Ortalama:        {ortalama:,.0f} TL")
            
            # Benzer evler
            if benzer_evler:
                print(f"\n{'-'*70}")
                print("BENZER EVLER:")
                for i, ev in enumerate(benzer_evler, 1):
                    print(f"\n{i}. {ev['metrekare']:.0f}m2, {ev['oda']:.0f} oda, {ev['yas']:.0f} yil")
                    print(f"   Fiyat: {ev['fiyat']:,.0f} TL")
                    print(f"   Link: {ev['url']}")
            
            print("="*70)
            tahmin_sayisi += 1
        
        except ValueError:
            print("\nHATA: Gecerli sayi girin!")
            continue
        except KeyboardInterrupt:
            break
    
    print(f"\n{tahmin_sayisi} tahmin yapildi. Gorusmek uzere!\n")


if __name__ == "__main__":
    main()

