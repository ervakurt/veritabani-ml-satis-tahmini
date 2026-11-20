
import pandas as pd
import numpy as np
import joblib
import psycopg2
from getpass import getpass

from sklearn.ensemble import HistGradientBoostingRegressor
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

print("Veriler yukleniyor...")

egitim = pd.read_sql_query(
    """
    SELECT magaza_id, tahmin_gunu, haftanin_gunu, ay,
           gecmis_7_gun_ortalama, gecmis_28_gun_ortalama,
           gecmis_59_gun_ortalama, gercek_satis
    FROM yeni_ml_egitim_temiz
    """,
    baglanti
)

test = pd.read_sql_query(
    """
    SELECT magaza_id, tahmin_gunu, haftanin_gunu, ay,
           gecmis_7_gun_ortalama, gecmis_28_gun_ortalama,
           gecmis_59_gun_ortalama, gercek_satis
    FROM yeni_ml_test
    """,
    baglanti
)

baglanti.close()

# Ozellikleri hazirla
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

# HistGradientBoosting modelini egit
print("HistGradientBoosting modeli egitiliyor...")

model = HistGradientBoostingRegressor(
    max_iter=200,
    max_depth=10,
    learning_rate=0.05,
    min_samples_leaf=20,
    random_state=42
)

model.fit(x_egitim, y_egitim)

# Test tahminleri
tahminler = np.maximum(model.predict(x_test), 0)

mae = mean_absolute_error(y_test, tahminler)
rmse = np.sqrt(mean_squared_error(y_test, tahminler))
r2 = r2_score(y_test, tahminler)

print("\n--- HISTGRADIENTBOOSTING SONUCLARI ---")
print(f"MAE: {mae:.2f}")
print(f"RMSE: {rmse:.2f}")
print(f"R2: {r2:.3f}")

print("\n--- IYILESTIRILMIS RANDOM FOREST ---")
print("MAE: 14.77")
print("RMSE: 31.18")
print("R2: 0.720")

# Magaza bazinda hata analizi
test["tahmini_satis"] = tahminler

for magaza in ["S0020", "S0026", "S0085"]:
    grup = test[test["magaza_id"] == magaza]

    magaza_mae = mean_absolute_error(
        grup["gercek_satis"],
        grup["tahmini_satis"]
    )

    print(f"{magaza} MAE: {magaza_mae:.2f}")

# Modeli kaydet
joblib.dump(
    {
        "model": model,
        "ozellikler": x_egitim.columns.tolist()
    },
    "models/hist_gradient_modeli.pkl"
)

print("\nHistGradientBoosting modeli kaydedildi.")
