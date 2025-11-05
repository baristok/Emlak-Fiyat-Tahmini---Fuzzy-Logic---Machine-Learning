"""
Emlak Fiyat Tahmini - Makine Ogrenmesi Model
Random Forest ile egitilmis model
Veri: emlakverileri.csv (2043 kayit)
"""

import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
import warnings
warnings.filterwarnings('ignore')


class EmlakMLModel:
    """
    Random Forest ile emlak fiyat tahmini
    """
    
    def __init__(self):
        self.model = None
        self.df = None
        self.df_processed = None
        
    def veriyi_yukle_ve_isle(self, csv_path='sehir_file/emlakverileri.csv'):
        """CSV verisini yukle ve isle"""
        print("\nVeri yukleniyor...")
        self.df = pd.read_csv(csv_path)
        
        # String verileri sayiya cevir
        self.df['Fiyat_Numeric'] = self.df['Fiyat'].str.replace('.', '', regex=False).str.replace(' TL', '').astype(float)
        
        # Oda sayisi: "2 + 1" -> 3
        self.df['Oda_Numeric'] = self.df['Oda Sayısı'].str.split('+').apply(
            lambda x: int(x[0].strip()) + int(x[1].strip()) if len(x) == 2 else int(x[0].strip())
        )
        
        # Metrekare: "80 m2" -> 80
        self.df['Metrekare_Numeric'] = self.df['Brüt m2'].str.replace(' m2', '').astype(float)
        
        # Kat sayisi: "6 Katlı" -> 6
        self.df['Kat_Sayisi_Numeric'] = self.df['Kat Sayısı'].str.replace(' Katlı', '').astype(int)
        
        # Bulundugu kat
        def kat_donustur(kat_str):
            if 'Bodrum' in kat_str or 'Bahçe' in kat_str:
                return -1
            elif 'Zemin' in kat_str or 'Giriş' in kat_str:
                return 0
            elif 'Yüksek' in kat_str:
                return 5
            elif 'Ara' in kat_str:
                return 2
            else:
                try:
                    return int(kat_str.split('.')[0])
                except:
                    return 1
        
        self.df['Bulundugu_Kat_Numeric'] = self.df['Bulunduğu Kat'].apply(kat_donustur)
        
        # Bina yasi: "11 Yaşında" -> 11
        def yas_donustur(yas_str):
            if 'Sıfır' in yas_str:
                return 0
            elif 'Yaşında' in yas_str:
                return int(yas_str.replace(' Yaşında', ''))
            else:
                return 10
        
        self.df['Bina_Yasi_Numeric'] = self.df['Bina Yaşı'].apply(yas_donustur)
        
        # Isitma tipi skorlama
        isitma_skorlari = {
            'Isıtma Yok': 0,
            'Soba': 1,
            'Doğalgaz Sobası': 2,
            'Kat Kaloriferi': 4,
            'Kombi': 5,
            'Merkezi': 6,
            'Merkezi (Pay Öl...': 6,
            'Klima': 8,
            'Yerden Isıtma': 9,
            'Güneş Enerjisi': 10,
            'Belirtilmemiş': 5
        }
        
        self.df['Isitma_Numeric'] = self.df['Isınma Tipi'].map(isitma_skorlari).fillna(5)
        
        # Temiz veriyi sakla
        self.df_processed = self.df.dropna(subset=['Fiyat_Numeric', 'Metrekare_Numeric', 'Oda_Numeric', 
                                                     'Bina_Yasi_Numeric', 'Bulundugu_Kat_Numeric', 
                                                     'Kat_Sayisi_Numeric', 'Isitma_Numeric'])
        
        print(f"Veri islendi. Toplam kayit: {len(self.df_processed)}")
        
    def model_egit(self):
        """Random Forest modelini egit"""
        print("\nModel egitiliyor...")
        
        # Feature'lari hazirla
        X = self.df_processed[['Metrekare_Numeric', 'Oda_Numeric', 'Bina_Yasi_Numeric', 
                                'Bulundugu_Kat_Numeric', 'Kat_Sayisi_Numeric', 'Isitma_Numeric']]
        y = self.df_processed['Fiyat_Numeric']
        
        # Train-test split
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
        
        # Random Forest modeli
        self.model = RandomForestRegressor(
            n_estimators=100,  # Agac sayisi
            max_depth=20,      # Maksimum derinlik
            min_samples_split=5,
            min_samples_leaf=2,
            random_state=42,
            n_jobs=-1
        )
        
        self.model.fit(X_train, y_train)
        
        # Test performansi
        y_pred = self.model.predict(X_test)
        
        mae = mean_absolute_error(y_test, y_pred)
        rmse = np.sqrt(mean_squared_error(y_test, y_pred))
        r2 = r2_score(y_test, y_pred)
        mape = np.mean(np.abs((y_test - y_pred) / y_test)) * 100
        
        print(f"\nModel egitildi!")
        print(f"Test seti performansi:")
        print(f"  MAE: {mae:,.0f} TL")
        print(f"  RMSE: {rmse:,.0f} TL")
        print(f"  R2: {r2:.4f}")
        print(f"  MAPE: {mape:.2f}%")
        
    def predict(self, ozellikler):
        """Fiyat tahmini yap"""
        if self.model is None:
            print("Hata: Model egitilmemis!")
            return None
        
        # Feature'lari hazirla
        X = pd.DataFrame([{
            'Metrekare_Numeric': ozellikler['metrekare'],
            'Oda_Numeric': ozellikler['oda_sayisi'],
            'Bina_Yasi_Numeric': ozellikler['bina_yasi'],
            'Bulundugu_Kat_Numeric': ozellikler['bulundugu_kat'],
            'Kat_Sayisi_Numeric': ozellikler['bina_kat_sayisi'],
            'Isitma_Numeric': ozellikler['isitma_tipi']
        }])
        
        tahmin = self.model.predict(X)[0]
        return tahmin
    
    def benzer_evler_bul(self, ozellikler, n=5):
        """Benzer evleri bul ve linklerini dondur"""
        if self.df_processed is None:
            return []
        
        # Benzer evleri filtrele (m2 ve oda sayisina gore)
        m2_min = ozellikler['metrekare'] - 20
        m2_max = ozellikler['metrekare'] + 20
        
        benzer = self.df_processed[
            (self.df_processed['Metrekare_Numeric'] >= m2_min) & 
            (self.df_processed['Metrekare_Numeric'] <= m2_max) &
            (self.df_processed['Oda_Numeric'] == ozellikler['oda_sayisi'])
        ]
        
        if len(benzer) == 0:
            # Sadece m2'ye gore ara
            benzer = self.df_processed[
                (self.df_processed['Metrekare_Numeric'] >= m2_min) & 
                (self.df_processed['Metrekare_Numeric'] <= m2_max)
            ]
        
        if len(benzer) > 0:
            # Rastgele n tane sec
            ornekler = benzer.sample(min(n, len(benzer)))
            
            sonuclar = []
            for idx, row in ornekler.iterrows():
                sonuclar.append({
                    'url': row['URL'],
                    'fiyat': row['Fiyat_Numeric'],
                    'metrekare': row['Metrekare_Numeric'],
                    'oda': row['Oda_Numeric'],
                    'yas': row['Bina_Yasi_Numeric']
                })
            
            return sonuclar
        
        return []


def main():
    """Interaktif tahmin programi"""
    print("\n" + "="*60)
    print(" EMLAK FIYAT TAHMINI - MAKINE OGRENMESI")
    print("="*60)
    
    # Model olustur ve egit
    model = EmlakMLModel()
    model.veriyi_yukle_ve_isle()
    model.model_egit()
    
    print("\nHazir! (Cikmak icin 'q' yazin)\n")
    print("="*60)
    
    tahmin_sayisi = 0
    
    # Ana dongu
    while True:
        print(f"\n--- TAHMIN #{tahmin_sayisi + 1} ---\n")
        
        try:
            # Metrekare
            inp = input("Metrekare: ").strip()
            if inp.lower() == 'q':
                break
            metrekare = int(inp)
            
            # Oda sayisi
            print("(1: Studyo, 2: 1+1, 3: 2+1, 4: 3+1, ...)")
            inp = input("Oda sayisi: ").strip()
            if inp.lower() == 'q':
                break
            oda_sayisi = int(inp)
            
            # Bina yasi
            print("(0: Sifir, 5: 5 yil, 10: 10 yil, ...)")
            inp = input("Bina yasi: ").strip()
            if inp.lower() == 'q':
                break
            bina_yasi = int(inp)
            
            # Bulundugu kat
            print("(-1: Bodrum, 0: Zemin, 3: 3.kat, ...)")
            inp = input("Bulundugu kat: ").strip()
            if inp.lower() == 'q':
                break
            bulundugu_kat = int(inp)
            
            # Kat sayisi
            inp = input("Bina kat sayisi: ").strip()
            if inp.lower() == 'q':
                break
            bina_kat_sayisi = int(inp)
            
            # Isitma
            print("(0: Yok, 5: Kombi, 8: Klima, 9: Yerden)")
            inp = input("Isitma skoru: ").strip()
            if inp.lower() == 'q':
                break
            isitma_tipi = int(inp)
            
            # Tahmin yap
            ozellikler = {
                'metrekare': metrekare,
                'oda_sayisi': oda_sayisi,
                'bina_yasi': bina_yasi,
                'bulundugu_kat': bulundugu_kat,
                'bina_kat_sayisi': bina_kat_sayisi,
                'isitma_tipi': isitma_tipi
            }
            
            tahmin = model.predict(ozellikler)
            
            if tahmin:
                print("\n" + "-"*60)
                print(f"TAHMIN: {tahmin:,.0f} TL")
                print(f"M2 basina: {tahmin/metrekare:,.0f} TL/m2")
                print("-"*60)
                
                # Benzer evleri goster
                print("\nBENZER EVLER:")
                benzer_evler = model.benzer_evler_bul(ozellikler, n=5)
                
                if benzer_evler:
                    for i, ev in enumerate(benzer_evler, 1):
                        print(f"\n{i}. {ev['metrekare']:.0f}m2, {ev['oda']:.0f} oda, {ev['yas']:.0f} yil")
                        print(f"   Fiyat: {ev['fiyat']:,.0f} TL")
                        print(f"   Link: {ev['url']}")
                else:
                    print("Benzer ev bulunamadi")
                
                print("-"*60)
                tahmin_sayisi += 1
            else:
                print("\nTahmin yapilamadi!")
        
        except ValueError:
            print("\nHATA: Gecerli sayi girin!")
            continue
        except KeyboardInterrupt:
            break
    
    print(f"\n{tahmin_sayisi} tahmin yapildi. Gorusmek uzere!\n")


if __name__ == "__main__":
    main()

