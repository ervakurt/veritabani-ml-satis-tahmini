
import os
import pandas as pd
import psycopg2
from getpass import getpass
from psycopg2.extras import execute_values


dosya_yolu = "reports/csv/iyilestirilmis_rf_59_gunluk_tahmin.csv"

veri = pd.read_csv(
    dosya_yolu,
    parse_dates=["tahmin_tarihi"]
)

print("CSV dosyasi okundu.")
print("Toplam kayit:", len(veri))
gerekli_sutunlar = [
    "magaza_id",
    "tahmin_tarihi",
    "tahmin_gunu",
    "tahmini_satis"
]

eksik = set(gerekli_sutunlar) - set(veri.columns)

if eksik:
    raise ValueError(f"Eksik sutunlar: {eksik}")

if veri[gerekli_sutunlar].isnull().any().any():
    raise ValueError("Tahmin verilerinde bos deger var.")

if veri.duplicated(
    ["magaza_id", "tahmin_tarihi"]
).any():
    raise ValueError("Tekrar eden magaza-tarih kayitlari var.")


kayitlar = [
    (
        str(satir.magaza_id),
        satir.tahmin_tarihi.date(),
        int(satir.tahmin_gunu),
        float(satir.tahmini_satis)
    )
    for satir in veri.itertuples(index=False)
]


sifre = os.getenv("PGPASSWORD") or getpass(
    "PostgreSQL sifresi: "
)

baglanti = psycopg2.connect(
    host="localhost",
    port=5432,
    dbname="retail_ml_db",
    user="postgres",
    password=sifre
)

try:
    with baglanti:
        with baglanti.cursor() as cursor:
            # Tahminleri yeni tabloya kaydet
            execute_values(
                cursor,
                """
                INSERT INTO satis_tahminleri_rf_iyilestirilmis
                (magaza_id, tahmin_tarihi, tahmin_gunu, tahmini_satis)
                VALUES %s
                ON CONFLICT (magaza_id, tahmin_tarihi)
                DO UPDATE SET
                    tahmin_gunu = EXCLUDED.tahmin_gunu,
                    tahmini_satis = EXCLUDED.tahmini_satis
                """,
                kayitlar
            )

           
            cursor.execute(
                """
                SELECT
                    COUNT(*),
                    COUNT(DISTINCT magaza_id),
                    ROUND(SUM(tahmini_satis), 2)
                FROM satis_tahminleri_rf_iyilestirilmis
                """
            )

            sonuc = cursor.fetchone()

    print("\n--- POSTGRESQL KAYIT SONUCLARI ---")
    print("Toplam tahmin:", sonuc[0])
    print("Magaza sayisi:", sonuc[1])
    print("Toplam tahmini satis:", sonuc[2])
    print("\nTahminler PostgreSQL'e kaydedildi.")

finally:
    baglanti.close()
