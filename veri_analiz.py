"""
Veri Analiz ve Temizleme
En ucuz ilanlari goster ve temizle
"""

import pandas as pd


def en_ucuz_ilanlari_goster(n=20):
    """En ucuz n ilani goster"""
    print("\nVeri yukleniyor...")
    df = pd.read_csv('sehir_file/emlakverileri.csv')
    
    # Fiyati sayiya cevir
    df['Fiyat_Numeric'] = df['Fiyat'].str.replace('.', '', regex=False).str.replace(' TL', '').astype(float)
    
    # En ucuz ilanlari sirala (ascending=True yaparak en düşükten en yükseğe sıralanır)
    # Bu kısım değişti: ascending=False -> ascending=True
    df_sorted = df.sort_values('Fiyat_Numeric', ascending=True) 
    
    # Başlık ve çıktıyı güncelledik
    print(f"\n{'='*100}")
    print(f" EN UCUZ {n} ILAN")
    print(f"{'='*100}\n")
    
    for i, (idx, row) in enumerate(df_sorted.head(n).iterrows(), 1):
        print(f"{i}. {row['Fiyat']} - {row['Brüt m2']} - {row['Oda Sayısı']} - {row['Bina Yaşı']}")
        print(f"   URL: {row['URL']}")
        print()
    
    print(f"{'='*100}\n")
    
    # İstatistikler (Değişmedi, ancak min/max değerleri en ucuz ilanlar bağlamında daha anlamlı hale geldi)
    print("ISTATISTIKLER:")
    print(f"Toplam ilan sayisi: {len(df)}")
    print(f"Ortalama fiyat: {df['Fiyat_Numeric'].mean():,.0f} TL")
    print(f"Medyan fiyat: {df['Fiyat_Numeric'].median():,.0f} TL")
    print(f"Min fiyat: {df['Fiyat_Numeric'].min():,.0f} TL")
    print(f"Max fiyat: {df['Fiyat_Numeric'].max():,.0f} TL")
    print(f"\nP75 (ust %25): {df['Fiyat_Numeric'].quantile(0.75):,.0f} TL")
    print(f"P90 (ust %10): {df['Fiyat_Numeric'].quantile(0.90):,.0f} TL")
    print(f"P95 (ust %5): {df['Fiyat_Numeric'].quantile(0.95):,.0f} TL")
    
    return df_sorted


def veriyi_temizle(ust_limit=None, alt_limit=None):
    """Belirlenen limitlerin disindaki ilanlari kaldir"""
    print("\n\nVeri temizleniyor...")
    df = pd.read_csv('sehir_file/emlakverileri.csv')
    
    # Fiyati sayiya cevir
    df['Fiyat_Numeric'] = df['Fiyat'].str.replace('.', '', regex=False).str.replace(' TL', '').astype(float)
    
    onceki_sayi = len(df)
    
    # Ust limit varsa filtrele
    if ust_limit:
        df = df[df['Fiyat_Numeric'] <= ust_limit]
    
    # Alt limit varsa filtrele
    if alt_limit:
        df = df[df['Fiyat_Numeric'] >= alt_limit]
    
    sonraki_sayi = len(df)
    silinen = onceki_sayi - sonraki_sayi
    
    # Fiyat_Numeric kolonunu kaldir
    df = df.drop('Fiyat_Numeric', axis=1)
    
    # Yeni dosyaya kaydet
    yeni_dosya = 'sehir_file/emlakverileri_temiz.csv'
    df.to_csv(yeni_dosya, index=False)
    
    print(f"\n{'='*80}")
    print(f"TEMIZLEME TAMAMLANDI")
    print(f"{'='*80}")
    print(f"Onceki ilan sayisi: {onceki_sayi}")
    print(f"Yeni ilan sayisi: {sonraki_sayi}")
    print(f"Silinen ilan sayisi: {silinen}")
    print(f"\nYeni dosya: {yeni_dosya}")
    print(f"{'='*80}\n")


def main():
    """Ana program"""
    print("\n" + "="*80)
    print(" VERI ANALIZ VE TEMIZLEME")
    print("="*80)
    
    # En ucuz ilanlari goster fonksiyonunu çağırdık
    df_sorted = en_ucuz_ilanlari_goster(n=20)
    
    # Kullaniciya sor
    print("\nVeriyi temizlemek istiyor musunuz? (e/h): ", end='')
    cevap = input().strip().lower()
    
    if cevap in ['e', 'evet']:
        print("\nOnerilen limitler:")
        df = pd.read_csv('sehir_file/emlakverileri.csv')
        df['Fiyat_Numeric'] = df['Fiyat'].str.replace('.', '', regex=False).str.replace(' TL', '').astype(float)
        
        # Temizleme için alt limit önerileri (Örneğin P05 ve P10)
        p05 = df['Fiyat_Numeric'].quantile(0.05)
        p10 = df['Fiyat_Numeric'].quantile(0.10)
        
        # Önerilen limit başlıkları en ucuz ilanlara göre güncellendi
        print(f"1) P05 alti ilanlar (alt %5): {p05:,.0f} TL alti")
        print(f"2) P10 alti ilanlar (alt %10): {p10:,.0f} TL alti")
        print(f"3) Ozel limit belirle")
        print(f"4) Iptal")
        
        secim = input("\nSeciminiz (1-4): ").strip()
        
        if secim == '1':
            # P05 altı temizleme: alt limit belirtmedik, üst limit P05'e kadar olacak şekilde temizlenmeli.
            # Ancak temizleme fonksiyonu "limitlerin dışındakileri kaldırma" mantığında olduğu için, 
            # alt limit belirterek (örneğin 1000 TL altını) veya üst limit belirterek (P05 üstünü) temizleyebiliriz.
            # Veri temizleme genellikle aykırı değerleri kaldırmak için üst ve alt limitlerle yapılır.
            
            # Burada, "alt %5'i sil" mantığı için alt limit belirtmeliyiz, yani P05'in altındaki tüm ilanları temizle.
            # veriyi_temizle(alt_limit=p05) yaparsak P05 ve üstünü tutarız.
            veriyi_temizle(alt_limit=p05) 
            
        elif secim == '2':
            veriyi_temizle(alt_limit=p10)
            
        elif secim == '3':
            try:
                # Kullanıcıdan alt limit alıp altını temizleyebiliriz (örn: 100000 TL altını sil)
                alt_limit = float(input("Alt limit (TL) - Bu limitin altı silinecek: ").strip().replace('.', '').replace(',', ''))
                veriyi_temizle(alt_limit=alt_limit)
            except:
                print("Gecersiz limit!")
        else:
            print("Iptal edildi.")
    else:
        print("\nTemizleme iptal edildi.")


if __name__ == "__main__":
    main()