
import pandas as pd
import psycopg2


baglanti = psycopg2.connect(
    host="localhost",
    port=5432,
    dbname="retail_ml_db",
    user="postgres",
    password=input("PostgreSQL şifrenizi girin: ")
)

sorgu = "SELECT * FROM ml_egitim ORDER BY tarih"

veriler = pd.read_sql_query(sorgu, baglanti)

baglanti.close()


print("Toplam kayıt sayısı:", len(veriler))
print("Sütunlar:")
print(veriler.columns.tolist())

print("\nİlk 5 kayıt:")
print(veriler.head())

veriler["tarih"] = pd.to_datetime(veriler["tarih"])
egitim = veriler[veriler["tarih"] < "2019-09-01"].copy()
dogrulama = veriler[veriler["tarih"] >= "2019-09-01"].copy()

print("\nEğitim kayıt sayısı:", len(egitim))
print("Doğrulama kayıt sayısı:", len(dogrulama))


hedef = "gunluk_satis"


ozellikler = [
    "ortalama_fiyat",
    "toplam_stok",
    "urun_sayisi",
    "promosyon1_sayisi",
    "promosyon2_sayisi",
    "magaza_tipi_id",
    "magaza_boyutu",
    "sehir_id",
    "gecmis_1_gun",
    "gecmis_7_gun",
    "gecmis_14_gun",
    "gecmis_28_gun",
    "haftanin_gunu",
    "ay"
]


X_egitim = egitim[ozellikler]
y_egitim = egitim[hedef]

X_dogrulama = dogrulama[ozellikler]
y_dogrulama = dogrulama[hedef]

print("Eğitim özellikleri:", X_egitim.shape)
print("Doğrulama özellikleri:", X_dogrulama.shape)

print("\nÖzelliklerin veri türleri:")
print(X_egitim.dtypes)


print("\nEğitim verisindeki eksik değerler:")
print(X_egitim.isnull().sum())

print("\nDoğrulama verisindeki eksik değerler:")
print(X_dogrulama.isnull().sum())

kategorik_sutunlar = ["magaza_tipi_id", "sehir_id"]

X_egitim = pd.get_dummies(
    X_egitim,
    columns=kategorik_sutunlar,
    dtype=int
)

X_dogrulama = pd.get_dummies(
    X_dogrulama,
    columns=kategorik_sutunlar,
    dtype=int
)

X_dogrulama = X_dogrulama.reindex(
    columns=X_egitim.columns,
    fill_value=0
)

print("\nDönüştürme tamamlandı!")
print("Eğitim özellikleri:", X_egitim.shape)
print("Doğrulama özellikleri:", X_dogrulama.shape)

print("\nMetin türünde sütun kaldı mı?")
print(X_egitim.select_dtypes(include=["object", "str"]).columns.tolist())

from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
import numpy as np

# Random Forest modelini oluştur
model = RandomForestRegressor(
    n_estimators=50,
    max_depth=15,
    random_state=42,
    n_jobs=-1
)

print("\nModel eğitiliyor...")

# Modeli eğit
model.fit(X_egitim, y_egitim)

print("Model eğitimi tamamlandı!")

# Doğrulama verileriyle tahmin yap
tahminler = model.predict(X_dogrulama)

# Başarı metriklerini hesapla
mae = mean_absolute_error(y_dogrulama, tahminler)
rmse = np.sqrt(mean_squared_error(y_dogrulama, tahminler))
r2 = r2_score(y_dogrulama, tahminler)

print("\nMODEL SONUÇLARI")
print("MAE:", round(mae, 3))
print("RMSE:", round(rmse, 3))
print("R²:", round(r2, 3))

print("\nİlk 5 tahmin:")
for gercek, tahmin in zip(y_dogrulama.iloc[:5], tahminler[:5]):
    print("Gerçek:", round(gercek, 2),
          "| Tahmin:", round(tahmin, 2))

# Basit tahmin yöntemi: Dünkü satış = Bugünkü tahmin
basit_tahminler = dogrulama["gecmis_1_gun"]

# Basit yöntemin hata değerleri
basit_mae = mean_absolute_error(y_dogrulama, basit_tahminler)
basit_rmse = np.sqrt(
    mean_squared_error(y_dogrulama, basit_tahminler)
)
basit_r2 = r2_score(y_dogrulama, basit_tahminler)

print("\nMODEL KARŞILAŞTIRMASI")
print("Random Forest MAE:", round(mae, 3))
print("Basit yöntem MAE:", round(basit_mae, 3))

print("Random Forest RMSE:", round(rmse, 3))
print("Basit yöntem RMSE:", round(basit_rmse, 3))

print("Random Forest R²:", round(r2, 3))
print("Basit yöntem R²:", round(basit_r2, 3))

import joblib
import os

# Model klasörünü oluştur
os.makedirs("models", exist_ok=True)

# Modeli ve özellik isimlerini kaydet
joblib.dump(
    {
        "model": model,
        "ozellikler": X_egitim.columns.tolist()
    },
    "models/ilk_random_forest.pkl"
)

print("\nModel başarıyla kaydedildi!")

import matplotlib.pyplot as plt

# İlk 30 kaydı karşılaştır
plt.figure(figsize=(12, 5))

plt.plot(
    range(30),
    y_dogrulama.iloc[:30],
    label="Gerçek Satış",
    marker="o"
)

plt.plot(
    range(30),
    tahminler[:30],
    label="Tahmin Edilen Satış",
    marker="x"
)

plt.title("Gerçek ve Tahmin Edilen Satışlar")
plt.xlabel("Doğrulama Kaydı")
plt.ylabel("Günlük Satış")
plt.legend()
plt.grid(True)

plt.tight_layout()
plt.savefig("reports/gercek_tahmin_grafigi.png", dpi=300)
plt.show()

print("Grafik başarıyla kaydedildi!")

# Modelin özellik önemlerini hesapla
onemler = pd.Series(
    model.feature_importances_,
    index=X_egitim.columns
)

# En önemli 10 özelliği seç
en_onemli = onemler.nlargest(10).sort_values()

# Grafik oluştur
plt.figure(figsize=(10, 6))

en_onemli.plot(kind="barh")

plt.title("Satış Tahmininde En Önemli 10 Özellik")
plt.xlabel("Özellik Önem Derecesi")
plt.ylabel("Özellikler")

plt.tight_layout()
plt.savefig("reports/ozellik_onem_grafigi.png", dpi=300)
plt.show()

print("\nÖzellik önem grafiği kaydedildi!")

