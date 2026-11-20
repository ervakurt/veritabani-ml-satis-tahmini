
import pandas as pd
import numpy as np
import joblib
import psycopg2
from getpass import getpass

from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score

# PostgreSQL baglantisi
sifre = getpass("PostgreSQL sifresi: ")

baglanti = psycopg2.connect(
    host="localhost",
    port=5432,
    dbname="retail_ml_db",
    user="postgres",
    password=sifre
)

# Egitim ve test verilerini oku
print("Veriler yukleniyor...")

egitim = pd.read_sql_query(
    "SELECT * FROM yeni_ml_egitim_temiz", baglanti
)

test = pd.read_sql_query(
    "SELECT * FROM yeni_ml_test", baglanti
)

baglanti.close()

# Model ozellikleri
sutunlar = [
    "magaza_id",
    "tahmin_gunu",
    "haftanin_gunu",
    "ay",
    "gecmis_7_gun_ortalama",
    "gecmis_28_gun_ortalama",
    "gecmis_59_gun_ortalama"
]

x_egitim = pd.get_dummies(
    egitim[sutunlar], columns=["magaza_id"]
)

x_test = pd.get_dummies(
    test[sutunlar], columns=["magaza_id"]
)

x_test = x_test.reindex(
    columns=x_egitim.columns, fill_value=0
)

y_egitim = egitim["gercek_satis"]
y_test = test["gercek_satis"]

# Iyilestirilmis Random Forest
print("Yeni model egitiliyor...")

model = RandomForestRegressor(
    n_estimators=100,
    max_depth=20,
    min_samples_leaf=5,
    max_features=0.8,
    random_state=42,
    n_jobs=-1
)

model.fit(x_egitim, y_egitim)

# Tahminler
tahminler = np.maximum(model.predict(x_test), 0)

# Performans
mae = mean_absolute_error(y_test, tahminler)
rmse = np.sqrt(mean_squared_error(y_test, tahminler))
r2 = r2_score(y_test, tahminler)

print("\n--- YENI MODEL SONUCLARI ---")
print(f"MAE: {mae:.2f}")
print(f"RMSE: {rmse:.2f}")
print(f"R2: {r2:.3f}")

print("\n--- ESKI MODEL SONUCLARI ---")
print("MAE: 15.12")
print("RMSE: 32.54")
print("R2: 0.695")

# Magaza bazinda hata analizi
test["tahmini_satis"] = tahminler

for magaza in ["S0020", "S0026", "S0085"]:
    grup = test[test["magaza_id"] == magaza]

    magaza_mae = mean_absolute_error(
        grup["gercek_satis"], grup["tahmini_satis"]
    )

    print(f"{magaza} MAE: {magaza_mae:.2f}")

# Modeli farkli isimle kaydet
joblib.dump(
    {
        "model": model,
        "ozellikler": x_egitim.columns.tolist()
    },
    "models/iyilestirilmis_random_forest.pkl"
)

print("\nYeni model kaydedildi.")# Yeni modelin tahmin sapmasi analizi
print("\n--- YENI MODEL TAHMIN SAPMASI ---")

for magaza in ["S0020", "S0026", "S0085"]:
    grup = test[test["magaza_id"] == magaza]

    yuksek_tahmin_orani = (
        grup["tahmini_satis"] > grup["gercek_satis"]
    ).mean() * 100

    ortalama_fark = (
        grup["tahmini_satis"] - grup["gercek_satis"]
    ).mean()

    print(f"\nMagaza: {magaza}")
    print(f"Yuksek tahmin orani: %{yuksek_tahmin_orani:.2f}")
    print(f"Ortalama tahmin farki: {ortalama_fark:.2f}")
