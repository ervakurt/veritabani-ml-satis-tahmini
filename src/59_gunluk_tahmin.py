
import joblib

# Eğitilmiş modeli yükle
kayit = joblib.load("models/gelecek_random_forest.pkl")

model = kayit["model"]
ozellikler = kayit["ozellikler"]

print("Model başarıyla yüklendi!")
print("Modelin kullandığı özellik sayısı:", len(ozellikler))

import os
import pandas as pd
import psycopg2
from getpass import getpass

# PostgreSQL bağlantısı
sifre = os.getenv("PGPASSWORD") or getpass("PostgreSQL şifreni gir: ")

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
print("Mağaza sayısı:", gelecek["magaza_id"].nunique())
print("Tahmin günü sayısı:", gelecek["tahmin_gunu"].nunique())

# Modelin kullanacağı özellikler
ozellik_sutunlari = [
    "tahmin_gunu",
    "haftanin_gunu",
    "ay",
    "gecmis_7_gun_ortalama",
    "gecmis_28_gun_ortalama",
    "gecmis_59_gun_ortalama"
]

# Mağaza bilgilerini sayısal hale getir
x_gelecek = pd.get_dummies(
    gelecek[ozellik_sutunlari + ["magaza_id"]],
    columns=["magaza_id"]
)

# Sütunları eğitilmiş modele uygun sıraya getir
x_gelecek = x_gelecek.reindex(
    columns=ozellikler,
    fill_value=0
)

# Satış tahminlerini oluştur
gelecek["tahmini_satis"] = model.predict(x_gelecek)

# Negatif satış tahminlerini sıfıra eşitle
gelecek["tahmini_satis"] = gelecek["tahmini_satis"].clip(lower=0)

print("\nİlk 10 satış tahmini:")
print(
    gelecek[
        ["magaza_id", "tahmin_tarihi", "tahmini_satis"]
    ].head(10).to_string(index=False)
)

print("\nToplam tahmin sayısı:", len(gelecek))

# Tahmin sonuçlarını CSV dosyasına kaydet
os.makedirs("reports", exist_ok=True)

sonuclar = gelecek[
    ["magaza_id", "tahmin_tarihi", "tahmin_gunu", "tahmini_satis"]
].copy()

sonuclar = sonuclar.sort_values(
    ["magaza_id", "tahmin_tarihi"]
)

sonuclar.to_csv(
    "reports/csv/59_gunluk_satis_tahminleri.csv",
    index=False,
    encoding="utf-8-sig"
)

print("Tahminler CSV dosyasına kaydedildi!")
print("Kaydedilen kayıt sayısı:", len(sonuclar))
