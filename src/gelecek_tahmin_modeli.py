
import os
import psycopg2
import pandas as pd
from getpass import getpass

# Veritabanı bağlantısı
sifre = os.getenv("PGPASSWORD") or getpass("PostgreSQL şifreni gir: ")

baglanti = psycopg2.connect(
    host="localhost",
    port=5432,
    dbname="retail_ml_db",
    user="postgres",
    password=sifre
)

# Eğitim verilerini al
egitim = pd.read_sql_query(
    "SELECT * FROM yeni_ml_egitim_temiz",
    baglanti
)

# Test verilerini al
test = pd.read_sql_query(
    "SELECT * FROM yeni_ml_test",
    baglanti
)

baglanti.close()

print("Eğitim verisi:", egitim.shape)
print("Test verisi:", test.shape)
print("Veriler başarıyla yüklendi!")

from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
import numpy as np

# Modelde kullanılacak özellikler
ozellikler = [
    "tahmin_gunu",
    "haftanin_gunu",
    "ay",
    "gecmis_7_gun_ortalama",
    "gecmis_28_gun_ortalama",
    "gecmis_59_gun_ortalama"
]

# Mağaza bilgisini sayısal sütunlara dönüştür
x_egitim = pd.get_dummies(
    egitim[ozellikler + ["magaza_id"]],
    columns=["magaza_id"]
)

x_test = pd.get_dummies(
    test[ozellikler + ["magaza_id"]],
    columns=["magaza_id"]
)

x_test = x_test.reindex(columns=x_egitim.columns, fill_value=0)

y_egitim = egitim["gercek_satis"]
y_test = test["gercek_satis"]

# Random Forest modelini oluştur
model = RandomForestRegressor(
    n_estimators=50,
    max_depth=15,
    random_state=42,
    n_jobs=-1
)

print("Model eğitiliyor...")
model.fit(x_egitim, y_egitim)

# Test tahminleri
tahminler = model.predict(x_test)

print("MAE:", round(mean_absolute_error(y_test, tahminler), 2))
print("RMSE:", round(np.sqrt(mean_squared_error(y_test, tahminler)), 2))
print("R2:", round(r2_score(y_test, tahminler), 3))

# Basit tahmin yöntemi
basit_tahmin = test["gecmis_7_gun_ortalama"]

# Basit yöntemin hata değerleri
basit_mae = mean_absolute_error(y_test, basit_tahmin)
basit_rmse = np.sqrt(mean_squared_error(y_test, basit_tahmin))
basit_r2 = r2_score(y_test, basit_tahmin)

print("\nBasit Tahmin Sonuçları")
print("MAE:", round(basit_mae, 2))
print("RMSE:", round(basit_rmse, 2))
print("R2:", round(basit_r2, 3))

import joblib

# Modeli ve kullanılan özellikleri kaydet
os.makedirs("models", exist_ok=True)

joblib.dump(
    {
        "model": model,
        "ozellikler": x_egitim.columns.tolist()
    },
    "models/gelecek_random_forest.pkl"
)

print("Model başarıyla kaydedildi!")
