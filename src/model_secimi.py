
import joblib
import pandas as pd
import numpy as np
import psycopg2
from getpass import getpass
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score

# Veritabanina baglan
sifre = getpass("PostgreSQL sifresi: ")

baglanti = psycopg2.connect(
    host="localhost",
    port=5432,
    dbname="retail_ml_db",
    user="postgres",
    password=sifre
)

print("Test verileri yukleniyor...")

test = pd.read_sql_query("""
    SELECT magaza_id, baslangic_tarihi, tahmin_tarihi,
           tahmin_gunu, haftanin_gunu, ay,
           gecmis_7_gun_ortalama, gecmis_28_gun_ortalama,
           gecmis_59_gun_ortalama, gercek_satis
    FROM yeni_ml_test
""", baglanti)


baglanti.close()

# Kaydedilen modeller
modeller = {
    "Random Forest": "models/iyilestirilmis_random_forest.pkl",
    "HistGradientBoosting": "models/hist_gradient_modeli.pkl"
}

sonuclar = []
benzersiz_sonuclar = []


for isim, dosya in modeller.items():
    print(f"\n{isim} degerlendiriliyor...")

    kayit = joblib.load(dosya)
    model = kayit["model"]
    ozellikler = kayit["ozellikler"]

   
    x_test = pd.get_dummies(
        test.drop(columns=[
            "gercek_satis",
            "baslangic_tarihi",
            "tahmin_tarihi"
        ]),
        columns=["magaza_id"]
    )

    x_test = x_test.reindex(
        columns=ozellikler, fill_value=0
    )

    gercek = test["gercek_satis"]
    tahmin = np.maximum(model.predict(x_test), 0)


    mae = mean_absolute_error(gercek, tahmin)
    rmse = np.sqrt(mean_squared_error(gercek, tahmin))
    r2 = r2_score(gercek, tahmin)
    sapma = np.mean(tahmin - gercek)

    # Ayni magaza ve hedef tarihe ait tahminleri birlestir
    tahmin_detay = pd.DataFrame({
        "magaza_id": test["magaza_id"],
        "tahmin_tarihi": test["tahmin_tarihi"],
        "gercek_satis": gercek,
        "tahmin": tahmin
    })

    benzersiz = tahmin_detay.groupby(
        ["magaza_id", "tahmin_tarihi"],
        as_index=False
    ).agg(
        gercek_satis=("gercek_satis", "mean"),
        tahmin=("tahmin", "mean")
    )

    yeni_mae = mean_absolute_error(
        benzersiz["gercek_satis"],
        benzersiz["tahmin"]
    )

    yeni_rmse = np.sqrt(mean_squared_error(
        benzersiz["gercek_satis"],
        benzersiz["tahmin"]
    ))

    yeni_r2 = r2_score(
        benzersiz["gercek_satis"],
        benzersiz["tahmin"]
    )

    benzersiz_sonuclar.append({
        "Model": isim,
        "MAE": round(yeni_mae, 2),
        "RMSE": round(yeni_rmse, 2),
        "R2": round(yeni_r2, 3)
    })


    sonuclar.append({
        "Model": isim,
        "MAE": round(mae, 2),
        "RMSE": round(rmse, 2),
        "R2": round(r2, 3),
        "Ortalama Sapma": round(sapma, 2)
    })

    print(f"MAE: {mae:.2f}")
    print(f"RMSE: {rmse:.2f}")
    print(f"R2: {r2:.3f}")
    print(f"Ortalama sapma: {sapma:.2f}")

sonuc_tablosu = pd.DataFrame(sonuclar)

print("\n--- MODEL KARSILASTIRMASI ---")
print(sonuc_tablosu.to_string(index=False))

sonuc_tablosu.to_csv(
    "reports/csv/dogrulama_model_karsilastirmasi.csv",
    index=False
)

print("\nKarsilastirma raporu kaydedildi.")

# Benzersiz magaza-tarih bazinda model karsilastirmasi

benzersiz_tablo = pd.DataFrame(benzersiz_sonuclar)

print("\n--- BENZERSIZ HEDEF MODEL KARSILASTIRMASI ---")
print(benzersiz_tablo.to_string(index=False))

benzersiz_tablo.to_csv(
    "reports/csv/benzersiz_hedef_karsilastirmasi.csv",
    index=False
)

print("\nBenzersiz hedef karsilastirma raporu kaydedildi.")

# Son test baslangic tarihindeki tahminleri karsilastir

son_tarih = test["baslangic_tarihi"].max()
son_test = test[
    test["baslangic_tarihi"] == son_tarih
].copy()

print("\n--- TEK BASLANGIC TARIHI MODEL KARSILASTIRMASI ---")
print("Baslangic tarihi:", son_tarih)
print("Test kayit sayisi:", len(son_test))

tek_tarih_sonuclar = []

for isim, dosya in modeller.items():
    kayit = joblib.load(dosya)
    model = kayit["model"]
    ozellikler = kayit["ozellikler"]

    x_son = pd.get_dummies(
        son_test.drop(columns=[
            "gercek_satis",
            "baslangic_tarihi",
            "tahmin_tarihi"
        ]),
        columns=["magaza_id"]
    )

    x_son = x_son.reindex(
        columns=ozellikler,
        fill_value=0
    )

    gercek = son_test["gercek_satis"]
    tahmin = np.maximum(model.predict(x_son), 0)

    tek_tarih_sonuclar.append({
        "Model": isim,
        "MAE": round(mean_absolute_error(gercek, tahmin), 2),
        "RMSE": round(np.sqrt(mean_squared_error(gercek, tahmin)), 2),
        "R2": round(r2_score(gercek, tahmin), 3)
    })

son_tablo = pd.DataFrame(tek_tarih_sonuclar)

print(son_tablo.to_string(index=False))

son_tablo.to_csv(
    "reports/csv/tek_baslangic_karsilastirmasi.csv",
    index=False
)

print("\nTek baslangic tarihi raporu kaydedildi.")
