
import os
import joblib
import pandas as pd
import psycopg2
from getpass import getpass

# Iyilestirilmis Random Forest modelini yukle
kayit = joblib.load(
    "models/iyilestirilmis_random_forest.pkl"
)

model = kayit["model"]
ozellikler = kayit["ozellikler"]

print("Iyilestirilmis Random Forest modeli yuklendi.")

# PostgreSQL baglantisi
sifre = getpass("PostgreSQL sifresi: ")

baglanti = psycopg2.connect(
    host="localhost",
    port=5432,
    dbname="retail_ml_db",
    user="postgres",
    password=sifre
)

# Gelecek tahmin verilerini oku
gelecek = pd.read_sql_query(
    "SELECT * FROM gelecek_tahmin_verisi",
    baglanti
)

baglanti.close()

print("Tahmin verisi:", gelecek.shape)
print("Magaza sayisi:", gelecek["magaza_id"].nunique())
print("Tahmin gunu sayisi:", gelecek["tahmin_gunu"].nunique())

# Model ozelliklerini hazirla
ozellik_sutunlari = [
    "tahmin_gunu",
    "haftanin_gunu",
    "ay",
    "gecmis_7_gun_ortalama",
    "gecmis_28_gun_ortalama",
    "gecmis_59_gun_ortalama"
]

x_gelecek = pd.get_dummies(
    gelecek[ozellik_sutunlari + ["magaza_id"]],
    columns=["magaza_id"]
)

x_gelecek = x_gelecek.reindex(
    columns=ozellikler,
    fill_value=0
)

# Satis tahminlerini hesapla
gelecek["tahmini_satis"] = model.predict(x_gelecek)

# Negatif tahminleri sifira esitle
gelecek["tahmini_satis"] = gelecek["tahmini_satis"].clip(
    lower=0
)

# Sonuclari hazirla
sonuclar = gelecek[
    ["magaza_id", "tahmin_tarihi", "tahmin_gunu", "tahmini_satis"]
].copy()

sonuclar = sonuclar.sort_values(
    ["magaza_id", "tahmin_tarihi"]
)

# Yeni CSV dosyasina kaydet
os.makedirs("reports/csv", exist_ok=True)

sonuclar.to_csv(
   "reports/csv/iyilestirilmis_rf_59_gunluk_tahmin.csv",
    index=False,
    encoding="utf-8-sig"
)

print("\n--- TAHMIN SONUCLARI ---")
print("Toplam tahmin:", len(sonuclar))
print("Magaza sayisi:", sonuclar["magaza_id"].nunique())
print("Toplam tahmini satis:", round(
    sonuclar["tahmini_satis"].sum(), 2
))

print("\nIlk 5 tahmin:")
print(sonuclar.head(5).to_string(index=False))

print("\nCSV dosyasi kaydedildi.")
