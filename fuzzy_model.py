"""
Emlak Fiyat Tahmini - Fuzzy Logic Model
Veri: emlakverileri.csv (2043 kayit)
"""

import numpy as np
import skfuzzy as fuzz
from skfuzzy import control as ctrl
import pandas as pd
import warnings
warnings.filterwarnings('ignore')


class EmlakFuzzyModel:
    """
    Fuzzy logic ile emlak fiyat tahmini
    """
    
    def __init__(self, df=None):
        self.df = df
        self.istatistikler = {}
        
        # Eger veri varsa isleyelim
        if df is not None:
            self._veriyi_isle()
            self._hesapla_istatistikler()
        
        # Fuzzy sistem kur
        self._olustur_fuzzy_degiskenler()
        self._olustur_kurallar()
        self._olustur_kontrol_sistemi()
    
    def _veriyi_isle(self):
        """String verileri sayiya cevir"""
        print("\nVeri isleniyor...")
        
        # Fiyat: "2.500.000 TL" -> 2500000
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
        
        # Isitma tipi skorlama (0-10 arasi)
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
        
        print("Veri donusumu tamam. Toplam kayit:", len(self.df))
    
    def _hesapla_istatistikler(self):
        """Veri istatistikleri"""
        # Metrekare basina fiyat
        self.df['Fiyat_Per_M2'] = self.df['Fiyat_Numeric'] / self.df['Metrekare_Numeric']
        
        # Temel istatistikler
        self.istatistikler = {
            'fiyat_min': self.df['Fiyat_Numeric'].quantile(0.05),
            'fiyat_p25': self.df['Fiyat_Numeric'].quantile(0.25),
            'fiyat_median': self.df['Fiyat_Numeric'].median(),
            'fiyat_p75': self.df['Fiyat_Numeric'].quantile(0.75),
            'fiyat_p90': self.df['Fiyat_Numeric'].quantile(0.90),
            'fiyat_max': self.df['Fiyat_Numeric'].quantile(0.95),
            'fiyat_mean': self.df['Fiyat_Numeric'].mean(),
            'metrekare_min': self.df['Metrekare_Numeric'].quantile(0.05),
            'metrekare_p25': self.df['Metrekare_Numeric'].quantile(0.25),
            'metrekare_median': self.df['Metrekare_Numeric'].median(),
            'metrekare_p75': self.df['Metrekare_Numeric'].quantile(0.75),
            'metrekare_max': self.df['Metrekare_Numeric'].quantile(0.95),
            'fiyat_per_m2_p25': self.df['Fiyat_Per_M2'].quantile(0.25),
            'fiyat_per_m2_median': self.df['Fiyat_Per_M2'].median(),
            'fiyat_per_m2_p75': self.df['Fiyat_Per_M2'].quantile(0.75),
            'fiyat_per_m2_p90': self.df['Fiyat_Per_M2'].quantile(0.90),
            'veri_sayisi': len(self.df)
        }
        
        print("\nVeri istatistikleri hesaplandi")
        print("Medyan fiyat:", f"{self.istatistikler['fiyat_median']:,.0f} TL")
        print("Medyan m2:", f"{self.istatistikler['metrekare_median']:.0f} m2")
    
    def _olustur_fuzzy_degiskenler(self):
        """Fuzzy degiskenler"""
        
        # Metrekare (40-350)
        self.metrekare = ctrl.Antecedent(np.arange(40, 350, 1), 'metrekare')
        self.metrekare['kucuk'] = fuzz.trimf(self.metrekare.universe, [40, 40, 90])
        self.metrekare['orta'] = fuzz.trimf(self.metrekare.universe, [70, 110, 160])
        self.metrekare['buyuk'] = fuzz.trimf(self.metrekare.universe, [140, 200, 350])
        
        # Oda sayisi (1-10)
        self.oda_sayisi = ctrl.Antecedent(np.arange(1, 10, 1), 'oda_sayisi')
        self.oda_sayisi['az'] = fuzz.trimf(self.oda_sayisi.universe, [1, 1, 3])
        self.oda_sayisi['orta'] = fuzz.trimf(self.oda_sayisi.universe, [2, 3, 5])
        self.oda_sayisi['cok'] = fuzz.trimf(self.oda_sayisi.universe, [4, 7, 10])
        
        # Bina yasi (0-60)
        self.bina_yasi = ctrl.Antecedent(np.arange(0, 60, 1), 'bina_yasi')
        self.bina_yasi['yeni'] = fuzz.trimf(self.bina_yasi.universe, [0, 0, 8])
        self.bina_yasi['orta'] = fuzz.trimf(self.bina_yasi.universe, [5, 15, 25])
        self.bina_yasi['eski'] = fuzz.trimf(self.bina_yasi.universe, [20, 60, 60])
        
        # Bulundugu kat (-1 ile 20 arasi)
        self.bulundugu_kat = ctrl.Antecedent(np.arange(-1, 20, 1), 'bulundugu_kat')
        self.bulundugu_kat['alt'] = fuzz.trimf(self.bulundugu_kat.universe, [-1, -1, 1])
        self.bulundugu_kat['orta'] = fuzz.trimf(self.bulundugu_kat.universe, [1, 3, 7])
        self.bulundugu_kat['yuksek'] = fuzz.trimf(self.bulundugu_kat.universe, [5, 12, 20])
        
        # Binanin kat sayisi
        self.bina_kat_sayisi = ctrl.Antecedent(np.arange(1, 25, 1), 'bina_kat_sayisi')
        self.bina_kat_sayisi['az_katli'] = fuzz.trimf(self.bina_kat_sayisi.universe, [1, 1, 5])
        self.bina_kat_sayisi['orta_katli'] = fuzz.trimf(self.bina_kat_sayisi.universe, [4, 7, 12])
        self.bina_kat_sayisi['cok_katli'] = fuzz.trimf(self.bina_kat_sayisi.universe, [10, 18, 25])
        
        # Isitma tipi (0-10 skor)
        self.isitma_tipi = ctrl.Antecedent(np.arange(0, 11, 1), 'isitma_tipi')
        self.isitma_tipi['zayif'] = fuzz.trimf(self.isitma_tipi.universe, [0, 0, 3])
        self.isitma_tipi['orta'] = fuzz.trimf(self.isitma_tipi.universe, [2, 5, 7])
        self.isitma_tipi['iyi'] = fuzz.trimf(self.isitma_tipi.universe, [6, 8, 11])
        
        # Cikti: Tahmini fiyat
        fmin = 500000
        fmax = 20000000
        
        self.tahmini_fiyat = ctrl.Consequent(np.arange(fmin, fmax, 100000), 'tahmini_fiyat')
        
        # fiyat segmenti
        self.tahmini_fiyat['cok_dusuk'] = fuzz.trimf(self.tahmini_fiyat.universe, [500000, 2000000, 2800000])
        self.tahmini_fiyat['dusuk'] = fuzz.trimf(self.tahmini_fiyat.universe, [2500000, 3200000, 4000000])
        self.tahmini_fiyat['orta'] = fuzz.trimf(self.tahmini_fiyat.universe, [3500000, 4500000, 5500000])
        self.tahmini_fiyat['yuksek'] = fuzz.trimf(self.tahmini_fiyat.universe, [5000000, 6500000, 8500000])
        self.tahmini_fiyat['cok_yuksek'] = fuzz.trimf(self.tahmini_fiyat.universe, [8000000, 12000000, 20000000])
    
    def _olustur_kurallar(self):
        """Fuzzy kurallari olustur"""
        
        self.kurallar = [
            # Cok yuksek fiyat kurallari
            ctrl.Rule(self.metrekare['buyuk'] & self.oda_sayisi['cok'] & 
                     self.bina_yasi['yeni'] & self.isitma_tipi['iyi'] & 
                     self.bulundugu_kat['yuksek'],
                     self.tahmini_fiyat['cok_yuksek']),
            
            ctrl.Rule(self.metrekare['buyuk'] & self.oda_sayisi['cok'] & 
                     self.bina_yasi['yeni'] & self.isitma_tipi['iyi'] & 
                     self.bina_kat_sayisi['cok_katli'],
                     self.tahmini_fiyat['cok_yuksek']),
            
            ctrl.Rule(self.metrekare['buyuk'] & self.oda_sayisi['cok'] & 
                     self.bulundugu_kat['yuksek'] & self.isitma_tipi['iyi'] &
                     self.bina_kat_sayisi['cok_katli'],
                     self.tahmini_fiyat['cok_yuksek']),
            
            ctrl.Rule(self.metrekare['buyuk'] & self.bina_yasi['yeni'] & 
                     self.bulundugu_kat['yuksek'] & self.isitma_tipi['iyi'] &
                     self.bina_kat_sayisi['cok_katli'],
                     self.tahmini_fiyat['cok_yuksek']),
            
            # Yuksek fiyat kurallari
            ctrl.Rule(self.metrekare['buyuk'] & self.oda_sayisi['orta'] & 
                     self.bina_yasi['yeni'] & self.isitma_tipi['iyi'],
                     self.tahmini_fiyat['yuksek']),
            
            ctrl.Rule(self.metrekare['buyuk'] & self.oda_sayisi['cok'] & 
                     self.bina_yasi['yeni'] & self.bulundugu_kat['orta'],
                     self.tahmini_fiyat['yuksek']),
            
            ctrl.Rule(self.metrekare['orta'] & self.oda_sayisi['cok'] & 
                     self.bina_yasi['yeni'] & self.bulundugu_kat['yuksek'],
                     self.tahmini_fiyat['yuksek']),
            
            ctrl.Rule(self.metrekare['buyuk'] & self.bulundugu_kat['yuksek'] & 
                     self.isitma_tipi['iyi'] & self.bina_kat_sayisi['cok_katli'],
                     self.tahmini_fiyat['yuksek']),
            
            ctrl.Rule(self.metrekare['buyuk'] & self.isitma_tipi['iyi'] & 
                     self.bina_yasi['yeni'] & self.bulundugu_kat['orta'],
                     self.tahmini_fiyat['yuksek']),
            
            ctrl.Rule(self.oda_sayisi['cok'] & self.bina_yasi['yeni'] & 
                     self.bulundugu_kat['yuksek'] & self.isitma_tipi['orta'],
                     self.tahmini_fiyat['yuksek']),
            
            # Orta fiyat kurallari
            ctrl.Rule(self.metrekare['orta'] & self.oda_sayisi['orta'] & 
                     self.bina_yasi['yeni'] & self.isitma_tipi['orta'],
                     self.tahmini_fiyat['orta']),
            
            ctrl.Rule(self.metrekare['orta'] & self.oda_sayisi['orta'] & 
                     self.bina_yasi['orta'] & self.isitma_tipi['orta'],
                     self.tahmini_fiyat['orta']),
            
            ctrl.Rule(self.metrekare['orta'] & self.oda_sayisi['cok'] & 
                     self.bulundugu_kat['orta'] & self.isitma_tipi['orta'],
                     self.tahmini_fiyat['orta']),
            
            # Buyuk metrekare ama eski - dengeli
            ctrl.Rule(self.metrekare['buyuk'] & self.bina_yasi['eski'] & 
                     self.bulundugu_kat['orta'] & self.isitma_tipi['orta'],
                     self.tahmini_fiyat['orta']),
            
            ctrl.Rule(self.metrekare['buyuk'] & self.bina_yasi['eski'] & 
                     self.bulundugu_kat['alt'] & self.isitma_tipi['orta'],
                     self.tahmini_fiyat['orta']),
            
            # Kucuk ama yeni ve iyi - dengeli
            ctrl.Rule(self.metrekare['kucuk'] & self.oda_sayisi['orta'] & 
                     self.bina_yasi['yeni'] & self.isitma_tipi['iyi'],
                     self.tahmini_fiyat['orta']),
            
            ctrl.Rule(self.metrekare['orta'] & self.bulundugu_kat['orta'] & 
                     self.isitma_tipi['iyi'] & self.bina_yasi['orta'],
                     self.tahmini_fiyat['orta']),
            
            ctrl.Rule(self.metrekare['orta'] & self.oda_sayisi['orta'] & 
                     self.bulundugu_kat['yuksek'] & self.bina_yasi['eski'],
                     self.tahmini_fiyat['orta']),
            
            ctrl.Rule(self.metrekare['buyuk'] & self.oda_sayisi['az'] & 
                     self.bina_yasi['orta'] & self.isitma_tipi['orta'],
                     self.tahmini_fiyat['orta']),
            
            # Dusuk fiyat kurallari
            ctrl.Rule(self.metrekare['kucuk'] & self.oda_sayisi['az'] & 
                     self.bulundugu_kat['alt'] & self.isitma_tipi['zayif'],
                     self.tahmini_fiyat['dusuk']),
            
            ctrl.Rule(self.metrekare['kucuk'] & self.bina_yasi['eski'] & 
                     self.isitma_tipi['zayif'] & self.bulundugu_kat['alt'],
                     self.tahmini_fiyat['dusuk']),
            
            ctrl.Rule(self.metrekare['orta'] & self.oda_sayisi['az'] & 
                     self.bina_yasi['eski'] & self.bina_kat_sayisi['az_katli'],
                     self.tahmini_fiyat['dusuk']),
            
            ctrl.Rule(self.metrekare['kucuk'] & self.bina_kat_sayisi['az_katli'] & 
                     self.isitma_tipi['zayif'] & self.bina_yasi['eski'],
                     self.tahmini_fiyat['dusuk']),
            
            ctrl.Rule(self.isitma_tipi['zayif'] & self.bulundugu_kat['alt'] &
                     self.bina_yasi['eski'] & self.oda_sayisi['az'],
                     self.tahmini_fiyat['dusuk']),
            
            ctrl.Rule(self.metrekare['kucuk'] & self.bulundugu_kat['alt'] &
                     self.bina_kat_sayisi['az_katli'] & self.bina_yasi['orta'],
                     self.tahmini_fiyat['dusuk']),
            
            ctrl.Rule(self.metrekare['orta'] & self.oda_sayisi['az'] &
                     self.isitma_tipi['zayif'] & self.bulundugu_kat['alt'],
                     self.tahmini_fiyat['dusuk']),
            
            ctrl.Rule(self.oda_sayisi['az'] & self.bina_yasi['eski'] &
                     self.isitma_tipi['zayif'] & self.bina_kat_sayisi['az_katli'],
                     self.tahmini_fiyat['dusuk']),
            
            # Cok dusuk fiyat kurallari
            ctrl.Rule(self.metrekare['kucuk'] & self.oda_sayisi['az'] & 
                     self.bina_yasi['eski'] & self.bulundugu_kat['alt'] &
                     self.isitma_tipi['zayif'],
                     self.tahmini_fiyat['cok_dusuk']),
            
            ctrl.Rule(self.metrekare['kucuk'] & self.bina_yasi['eski'] & 
                     self.isitma_tipi['zayif'] & self.bina_kat_sayisi['az_katli'] &
                     self.bulundugu_kat['alt'],
                     self.tahmini_fiyat['cok_dusuk']),
            
            ctrl.Rule(self.metrekare['kucuk'] & self.oda_sayisi['az'] & 
                     self.isitma_tipi['zayif'] & self.bulundugu_kat['alt'] &
                     self.bina_kat_sayisi['az_katli'],
                     self.tahmini_fiyat['cok_dusuk']),
            
            ctrl.Rule(self.oda_sayisi['az'] & self.bina_yasi['eski'] & 
                     self.isitma_tipi['zayif'] & self.bulundugu_kat['alt'] &
                     self.bina_kat_sayisi['az_katli'],
                     self.tahmini_fiyat['cok_dusuk']),
        ]
    
    def _olustur_kontrol_sistemi(self):
        """Kontrol sistemi kur"""
        self.kontrol_sistemi = ctrl.ControlSystem(self.kurallar)
        self.simulasyon = ctrl.ControlSystemSimulation(self.kontrol_sistemi)
    
    def predict(self, ozellikler):
        """Fiyat tahmini yap"""
        try:
            # Inputlari sinirla (clipping)
            metrekare = max(40, min(350, ozellikler['metrekare']))
            oda_sayisi = max(1, min(10, ozellikler['oda_sayisi']))
            bina_yasi = max(0, min(60, ozellikler['bina_yasi']))
            bulundugu_kat = max(-1, min(20, ozellikler['bulundugu_kat']))
            bina_kat_sayisi = max(1, min(25, ozellikler['bina_kat_sayisi']))
            isitma_tipi = max(0, min(10, ozellikler['isitma_tipi']))
            
            # Fuzzy sisteme inputlari ver
            self.simulasyon.input['metrekare'] = metrekare
            self.simulasyon.input['oda_sayisi'] = oda_sayisi
            self.simulasyon.input['bina_yasi'] = bina_yasi
            self.simulasyon.input['bulundugu_kat'] = bulundugu_kat
            self.simulasyon.input['bina_kat_sayisi'] = bina_kat_sayisi
            self.simulasyon.input['isitma_tipi'] = isitma_tipi
            
            # Hesapla
            self.simulasyon.compute()
            
            return self.simulasyon.output['tahmini_fiyat']
        
        except KeyError:
            # Fallback: basit m2 hesabi
            if self.istatistikler:
                m2_fiyat = self.istatistikler['fiyat_per_m2_median']
                base = ozellikler['metrekare'] * m2_fiyat
                yas_factor = 1.0 - (ozellikler['bina_yasi'] * 0.008)
                yas_factor = max(0.7, min(1.1, yas_factor))
                isitma_factor = 0.9 + (ozellikler['isitma_tipi'] * 0.02)
                return base * yas_factor * isitma_factor
            else:
                return None
        
        except Exception as e:
            print("Hata:", e)
            return None
    
    def predict_from_dataframe_row(self, row):
        """DataFrame satirindan tahmin yap"""
        ozellikler = {
            'metrekare': int(row['Metrekare_Numeric']),
            'oda_sayisi': int(row['Oda_Numeric']),
            'bina_yasi': int(row['Bina_Yasi_Numeric']),
            'bulundugu_kat': int(row['Bulundugu_Kat_Numeric']),
            'bina_kat_sayisi': int(row['Kat_Sayisi_Numeric']),
            'isitma_tipi': int(row['Isitma_Numeric'])
        }
        return self.predict(ozellikler)


def main():
    """Interaktif tahmin"""
    print("\n" + "="*60)
    print(" EMLAK FIYAT TAHMINI")
    print("="*60)
    print("\nModel yukleniyor...")
    
    # Veriyi yukle ve modeli olustur
    df = pd.read_csv('sehir_file/emlakverileri.csv')
    model = EmlakFuzzyModel(df=df)
    
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
            
            # Isitma (Tüm seçenekler)
            print("\nIsitma tipleri secenekleri:")
            print(" 0  : Isıtma Yok")
            print(" 1  : Soba")
            print(" 2  : Doğalgaz Sobası")
            print(" 4  : Kat Kaloriferi")
            print(" 5  : Kombi")
            print(" 6  : Merkezi / Merkezi (Pay Ölçer)")
            print(" 8  : Klima")
            print(" 9  : Yerden Isıtma")
            print("10  : Güneş Enerjisi")
            print("Enter: Belirtilmemiş/ortalama (varsayılan: 5 = Kombi/Merkezi)")
            inp = input("Isitma skoru veya yukaridaki tip numarasi: ").strip()
            if inp.lower() == 'q':
                break
            if inp == "":
                isitma_tipi = 5
            else:
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

