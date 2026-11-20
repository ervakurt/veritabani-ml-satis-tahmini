import pandas as pd
import numpy as np
import joblib
import psycopg2
from sklearn.metrics import mean_absolute_error, mean_squared_error

kayit = joblib.load("models/gelecek_random_forest.pkl")
model = kayit["model"]
ozellikler = kayit["ozellikler"]

sifre = input("PostgreSQL sifrenizi girin: ")

baglanti = psycopg2.connect(
    host="localhost",
    port=5432,
    dbname="retail_ml_db",
    user="postgres",
    password=sifre
)

sorgu = """
SELECT *
FROM yeni_ml_test
"""
veriler = pd.read_sql_query(sorgu, baglanti)
baglanti.close()

sutunlar = [
    "magaza_id",
    "tahmin_gunu",
    "haftanin_gunu",
    "ay",
    "gecmis_7_gun_ortalama",
    "gecmis_28_gun_ortalama",
    "gecmis_59_gun_ortalama"
]

x = pd.get_dummies(veriler[sutunlar], columns=["magaza_id"])
x = x.reindex(columns=ozellikler, fill_value=0)

veriler["tahmini_satis"] = np.maximum(model.predict(x), 0)

for magaza, grup in veriler.groupby("magaza_id"):
    mae = mean_absolute_error(
        grup["gercek_satis"], grup["tahmini_satis"]
    )

    rmse = np.sqrt(mean_squared_error(
        grup["gercek_satis"], grup["tahmini_satis"]
    ))

    print(f"\nMagaza: {magaza}")
    print(f"Test kaydi: {len(grup)}")
    print(f"MAE: {mae:.2f}")
    print(f"RMSE: {rmse:.2f}")
    print(f"Gercek satis ortalamasi: {grup['gercek_satis'].mean():.2f}")
    print(f"Tahmini satis ortalamasi: {grup['tahmini_satis'].mean():.2f}")# Tahminlerin gerçek satışlardan yüksek olma oranı
print("\n--- Tahmin Sapmasi Analizi ---")

for magaza, grup in veriler.groupby("magaza_id"):
    yuksek_tahmin = (
        grup["tahmini_satis"] > grup["gercek_satis"]
    ).mean() * 100

    ortalama_fark = (
        grup["tahmini_satis"] - grup["gercek_satis"]
    ).mean()

    print(f"\nMagaza: {magaza}")
    print(f"Yuksek tahmin orani: %{yuksek_tahmin:.2f}")
    print(f"Ortalama tahmin farki: {ortalama_fark:.2f}")# Tum test verilerinin genel hata analizi
genel_mae = mean_absolute_error(
    veriler["gercek_satis"],
    veriler["tahmini_satis"]
)

genel_rmse = np.sqrt(mean_squared_error(
    veriler["gercek_satis"],
    veriler["tahmini_satis"]
))

print("\n--- GENEL MODEL SONUCLARI ---")
print(f"Toplam test kaydi: {len(veriler)}")
print(f"Genel MAE: {genel_mae:.2f}")
print(f"Genel RMSE: {genel_rmse:.2f}")
print(f"Gercek satis ortalamasi: {veriler['gercek_satis'].mean():.2f}")
print(f"Tahmini satis ortalamasi: {veriler['tahmini_satis'].mean():.2f}")