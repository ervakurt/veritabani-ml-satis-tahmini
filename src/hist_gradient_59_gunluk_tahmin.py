
import pandas as pd
import numpy as np
import joblib
import psycopg2
from getpass import getpass

# Kaydedilen modeli yukle
print("HistGradientBoosting modeli yukleniyor...")

kayit = joblib.load("models/hist_gradient_modeli.pkl")
model = kayit["model"]
ozellikler = kayit["ozellikler"]

# PostgreSQL baglantisi
sifre = getpass("PostgreSQL sifresi: ")

baglanti = psycopg2.connect(
    host="localhost",
    port=5432,
    dbname="retail_ml_db",
    user="postgres",
    password=sifre
)

print("Gelecek tahmin verileri yukleniyor...")

veri = pd.read_sql_query("""
    SELECT magaza_id, tahmin_tarihi, tahmin_gunu,
           haftanin_gunu, ay,
           gecmis_7_gun_ortalama,
           gecmis_28_gun_ortalama,
           gecmis_59_gun_ortalama
    FROM gelecek_tahmin_verisi
    ORDER BY magaza_id, tahmin_tarihi
""", baglanti)

baglanti.close()

print(f"Toplam tahmin satiri: {len(veri)}")
print(f"Magaza sayisi: {veri['magaza_id'].nunique()}")

# Modelin kullanacagi ozellikler
x = veri.drop(columns=["tahmin_tarihi"])

x = pd.get_dummies(
    x,
    columns=["magaza_id"]
)

# Egitimdeki sutun sirasi ile ayni hale getir
x = x.reindex(
    columns=ozellikler,
    fill_value=0
)

# Tahmin yap
print("59 gunluk satis tahminleri hesaplaniyor...")

veri["tahmini_satis"] = np.maximum(
    model.predict(x), 0
)

# Sonuclari hazirla
sonuc = veri[
    ["magaza_id", "tahmin_tarihi",
     "tahmin_gunu", "tahmini_satis"]
].copy()

# Yeni CSV dosyasina kaydet
dosya = "reports/csv/hist_gradient_59_gunluk_tahmin.csv"

sonuc.to_csv(
    dosya,
    index=False,
    encoding="utf-8-sig"
)

# Genel sonuclari yazdir
print("\n--- HISTGRADIENTBOOSTING TAHMINLERI ---")
print(f"Toplam tahmin: {len(sonuc)}")
print(f"Magaza sayisi: {sonuc['magaza_id'].nunique()}")
print(f"Toplam tahmini satis: {sonuc['tahmini_satis'].sum():.2f}")

print("\nAylik tahminler:")

sonuc["ay"] = pd.to_datetime(
    sonuc["tahmin_tarihi"]
).dt.to_period("M")

print(
    sonuc.groupby("ay")["tahmini_satis"]
    .sum()
    .round(2)
)

print(f"\nTahminler kaydedildi: {dosya}")
