"""
Emlak Fiyat Tahmini API
FastAPI ile RESTful API servisi
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from typing import Optional, List, Dict
import pandas as pd
import uvicorn
from fuzzy_model import EmlakFuzzyModel
from ml_model import EmlakMLModel
import warnings
warnings.filterwarnings('ignore')

# FastAPI app
app = FastAPI(
    title="Emlak Fiyat Tahmini API",
    description="Fuzzy Logic ve Machine Learning ile emlak fiyat tahmini servisi",
    version="1.0.0"
)

# CORS ayarları
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Production'da spesifik domain'ler ekleyin
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Global model instancelari
fuzzy_model = None
ml_model = None
df = None


# Request/Response modelleri
class EmlakOzellikleri(BaseModel):
    """Emlak özellikleri girdi modeli"""
    metrekare: int = Field(..., ge=40, le=350, description="Metrekare (40-350 arası)")
    oda_sayisi: int = Field(..., ge=1, le=10, description="Toplam oda sayısı (1-10)")
    bina_yasi: int = Field(..., ge=0, le=60, description="Bina yaşı (0-60)")
    bulundugu_kat: int = Field(..., ge=-1, le=20, description="Bulunduğu kat (-1:bodrum, 0:zemin, ...)")
    bina_kat_sayisi: int = Field(..., ge=1, le=25, description="Binanın toplam kat sayısı")
    isitma_tipi: int = Field(..., ge=0, le=10, description="Isıtma tipi skoru (0:yok, 5:kombi, 9:yerden)")
    
    class Config:
        schema_extra = {
            "example": {
                "metrekare": 120,
                "oda_sayisi": 3,
                "bina_yasi": 5,
                "bulundugu_kat": 3,
                "bina_kat_sayisi": 8,
                "isitma_tipi": 5
            }
        }


class BenzerEv(BaseModel):
    """Benzer ev modeli"""
    url: str
    fiyat: float
    metrekare: float
    oda: int
    yas: int


class TahminSonucu(BaseModel):
    """Tahmin sonucu response modeli"""
    fuzzy_tahmin: float
    ml_tahmin: float
    ortalama_tahmin: float
    fark: float
    fark_yuzde: float
    m2_basina_fiyat: float
    benzer_evler: Optional[List[BenzerEv]] = []


class ModelIstatistik(BaseModel):
    """Model istatistikleri"""
    veri_sayisi: int
    medyan_fiyat: float
    medyan_m2: float
    fiyat_min: float
    fiyat_max: float


class HealthCheck(BaseModel):
    """Health check response"""
    status: str
    fuzzy_model_ready: bool
    ml_model_ready: bool
    data_loaded: bool


@app.on_event("startup")
async def startup_event():
    """Uygulama başlatıldığında modelleri yükle"""
    global fuzzy_model, ml_model, df
    
    print("🚀 API başlatılıyor...")
    print("📊 Veri yükleniyor...")
    
    try:
        # Veriyi yükle
        df = pd.read_csv('sehir_file/emlakverileri.csv')
        
        # Fuzzy model
        print("🔮 Fuzzy model oluşturuluyor...")
        fuzzy_model = EmlakFuzzyModel(df=df)
        
        # ML model
        print("🤖 ML model eğitiliyor...")
        ml_model = EmlakMLModel()
        ml_model.veriyi_yukle_ve_isle('sehir_file/emlakverileri.csv')
        ml_model.model_egit()
        
        print("✅ Tüm modeller hazır!")
        
    except Exception as e:
        print(f"❌ Model yükleme hatası: {e}")
        raise


@app.get("/", tags=["Genel"])
async def root():
    """API ana sayfa"""
    return {
        "message": "Emlak Fiyat Tahmini API",
        "version": "1.0.0",
        "docs": "/docs",
        "endpoints": {
            "health": "/health",
            "predict": "/predict",
            "predict_fuzzy": "/predict/fuzzy",
            "predict_ml": "/predict/ml",
            "stats": "/stats"
        }
    }


@app.get("/health", response_model=HealthCheck, tags=["Genel"])
async def health_check():
    """Sistem sağlık kontrolü"""
    return HealthCheck(
        status="healthy" if (fuzzy_model and ml_model and df is not None) else "unhealthy",
        fuzzy_model_ready=fuzzy_model is not None,
        ml_model_ready=ml_model is not None,
        data_loaded=df is not None
    )


@app.post("/predict", response_model=TahminSonucu, tags=["Tahmin"])
async def predict_combined(ozellikler: EmlakOzellikleri):
    """
    Her iki modelle tahmin yap (Fuzzy + ML)
    
    Bu endpoint hem Fuzzy Logic hem de Machine Learning modelini kullanarak
    fiyat tahmini yapar ve karşılaştırmalı sonuç döner.
    """
    if not fuzzy_model or not ml_model:
        raise HTTPException(status_code=503, detail="Modeller henüz yüklenmedi")
    
    try:
        # Özellikleri dict'e çevir
        oz_dict = ozellikler.dict()
        
        # Fuzzy tahmin
        fuzzy_tahmin = fuzzy_model.predict(oz_dict)
        
        # ML tahmin
        ml_tahmin = ml_model.predict(oz_dict)
        
        # Benzer evler
        benzer_evler = ml_model.benzer_evler_bul(oz_dict, n=5)
        benzer_evler_list = [BenzerEv(**ev) for ev in benzer_evler]
        
        # Hesaplamalar
        ortalama = (fuzzy_tahmin + ml_tahmin) / 2
        fark = abs(fuzzy_tahmin - ml_tahmin)
        fark_yuzde = (fark / fuzzy_tahmin) * 100 if fuzzy_tahmin > 0 else 0
        m2_fiyat = ortalama / ozellikler.metrekare
        
        return TahminSonucu(
            fuzzy_tahmin=round(fuzzy_tahmin, 2),
            ml_tahmin=round(ml_tahmin, 2),
            ortalama_tahmin=round(ortalama, 2),
            fark=round(fark, 2),
            fark_yuzde=round(fark_yuzde, 2),
            m2_basina_fiyat=round(m2_fiyat, 2),
            benzer_evler=benzer_evler_list
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Tahmin hatası: {str(e)}")


@app.post("/predict/fuzzy", tags=["Tahmin"])
async def predict_fuzzy_only(ozellikler: EmlakOzellikleri):
    """
    Sadece Fuzzy Logic modeli ile tahmin yap
    """
    if not fuzzy_model:
        raise HTTPException(status_code=503, detail="Fuzzy model henüz yüklenmedi")
    
    try:
        oz_dict = ozellikler.dict()
        tahmin = fuzzy_model.predict(oz_dict)
        
        return {
            "model": "Fuzzy Logic",
            "tahmin": round(tahmin, 2),
            "m2_basina_fiyat": round(tahmin / ozellikler.metrekare, 2),
            "ozellikler": oz_dict
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Fuzzy tahmin hatası: {str(e)}")


@app.post("/predict/ml", tags=["Tahmin"])
async def predict_ml_only(ozellikler: EmlakOzellikleri):
    """
    Sadece Machine Learning modeli ile tahmin yap
    """
    if not ml_model:
        raise HTTPException(status_code=503, detail="ML model henüz yüklenmedi")
    
    try:
        oz_dict = ozellikler.dict()
        tahmin = ml_model.predict(oz_dict)
        benzer_evler = ml_model.benzer_evler_bul(oz_dict, n=5)
        
        return {
            "model": "Random Forest (ML)",
            "tahmin": round(tahmin, 2),
            "m2_basina_fiyat": round(tahmin / ozellikler.metrekare, 2),
            "ozellikler": oz_dict,
            "benzer_evler": benzer_evler
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"ML tahmin hatası: {str(e)}")


@app.get("/stats", response_model=ModelIstatistik, tags=["İstatistik"])
async def get_statistics():
    """
    Veri seti istatistiklerini getir
    """
    if not fuzzy_model or not fuzzy_model.istatistikler:
        raise HTTPException(status_code=503, detail="İstatistikler henüz hazır değil")
    
    stats = fuzzy_model.istatistikler
    
    return ModelIstatistik(
        veri_sayisi=stats['veri_sayisi'],
        medyan_fiyat=round(stats['fiyat_median'], 2),
        medyan_m2=round(stats['metrekare_median'], 2),
        fiyat_min=round(stats['fiyat_min'], 2),
        fiyat_max=round(stats['fiyat_max'], 2)
    )


@app.get("/isitma-tipleri", tags=["Yardımcı"])
async def get_isitma_tipleri():
    """
    Isıtma tipi skorlarını getir
    """
    return {
        "isitma_tipleri": {
            "0": "Isıtma Yok",
            "1": "Soba",
            "2": "Doğalgaz Sobası",
            "4": "Kat Kaloriferi",
            "5": "Kombi",
            "6": "Merkezi / Merkezi (Pay Ölçer)",
            "8": "Klima",
            "9": "Yerden Isıtma",
            "10": "Güneş Enerjisi"
        }
    }

@app.post("/ping")
async def keep_alive():
    # Basit bir yanıt döner, bu endpoint API'nin boşa düşmemesi için çağrılır.
    return {"message": "API is alive"}


if __name__ == "__main__":
    print("\n" + "="*60)
    print(" EMLAK FİYAT TAHMİNİ API")
    print("="*60)
    print("\n🌐 API sunucusu başlatılıyor...")
    print("📖 Dokümantasyon: http://localhost:8000/docs")
    print("🔍 ReDoc: http://localhost:8000/redoc")
    print("\n" + "="*60 + "\n")
    
    uvicorn.run(
        "api_server:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )

