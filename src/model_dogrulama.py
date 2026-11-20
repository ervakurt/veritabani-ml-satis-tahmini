
import psycopg2
from getpass import getpass

sifre = getpass("PostgreSQL sifresi: ")

baglanti = psycopg2.connect(
    host="localhost",
    port=5432,
    dbname="retail_ml_db",
    user="postgres",
    password=sifre
)

cursor = baglanti.cursor()

tablolar = [
    "yeni_ml_egitim_temiz",
    "yeni_ml_test"
]

for tablo in tablolar:
    cursor.execute(f"""
        SELECT
            COUNT(*),
            MIN(baslangic_tarihi),
            MAX(baslangic_tarihi),
            MIN(tahmin_tarihi),
            MAX(tahmin_tarihi)
        FROM {tablo}
    """)

    sonuc = cursor.fetchone()

    print(f"\n--- {tablo} ---")
    print("Kayit sayisi:", sonuc[0])
    print("Ilk baslangic tarihi:", sonuc[1])
    print("Son baslangic tarihi:", sonuc[2])
    print("Ilk tahmin tarihi:", sonuc[3])
    print("Son tahmin tarihi:", sonuc[4])

cursor.close()
baglanti.close()

print("\nTarih kontrolleri tamamlandi.")

# Test verilerindeki tekrar eden hedefleri kontrol et
baglanti = psycopg2.connect(
    host="localhost",
    port=5432,
    dbname="retail_ml_db",
    user="postgres",
    password=sifre
)

cursor = baglanti.cursor()

cursor.execute("""
    SELECT
        COUNT(*) AS toplam_kayit,
        COUNT(DISTINCT (magaza_id, tahmin_tarihi))
            AS benzersiz_hedef,
        COUNT(DISTINCT (magaza_id, baslangic_tarihi))
            AS benzersiz_baslangic
    FROM yeni_ml_test
""")

toplam, hedef, baslangic = cursor.fetchone()

print("\n--- TEST VERISI TEKRAR KONTROLU ---")
print("Toplam kayit:", toplam)
print("Benzersiz magaza-tahmin tarihi:", hedef)
print("Benzersiz magaza-baslangic tarihi:", baslangic)
print("Tekrarlanan hedef kayit sayisi:", toplam - hedef)

cursor.close()
baglanti.close()

# Tahmin başlangıçları ile hedef tarihleri kontrol et
cursor = baglanti.cursor() if not baglanti.closed else None

if cursor is None:
    baglanti = psycopg2.connect(
        host="localhost",
        port=5432,
        dbname="retail_ml_db",
        user="postgres",
        password=sifre
    )
    cursor = baglanti.cursor()

cursor.execute("""
    SELECT
        COUNT(*) FILTER (
            WHERE tahmin_tarihi < baslangic_tarihi
        ) AS gecmis_hedefler,
        COUNT(*) FILTER (
            WHERE tahmin_tarihi = baslangic_tarihi
        ) AS ayni_gun_hedefleri,
        COUNT(*) FILTER (
            WHERE tahmin_tarihi > baslangic_tarihi
        ) AS gelecek_hedefler,
        MIN(tahmin_gunu),
        MAX(tahmin_gunu)
    FROM yeni_ml_test
""")

sonuc = cursor.fetchone()

print("\n--- TAHMIN TARIHI KONTROLU ---")
print("Baslangictan onceki hedefler:", sonuc[0])
print("Baslangicla ayni gun hedefleri:", sonuc[1])
print("Baslangictan sonraki hedefler:", sonuc[2])
print("En kucuk tahmin gunu:", sonuc[3])
print("En buyuk tahmin gunu:", sonuc[4])

cursor.close()
baglanti.close()

baglanti = psycopg2.connect(
    host="localhost",
    port=5432,
    dbname="retail_ml_db",
    user="postgres",
    password=sifre
)

cursor = baglanti.cursor()

cursor.execute("""
    SELECT
        tahmin_gunu,
        tahmin_tarihi - baslangic_tarihi AS gun_farki,
        COUNT(*) AS kayit_sayisi
    FROM yeni_ml_test
    GROUP BY tahmin_gunu, gun_farki
    ORDER BY tahmin_gunu, gun_farki
    LIMIT 10
""")

print("\n--- TAHMIN GUNU HESAPLAMA KONTROLU ---")

for tahmin_gunu, gun_farki, kayit_sayisi in cursor.fetchall():
    print(
        f"Tahmin gunu: {tahmin_gunu}, "
        f"Tarih farki: {gun_farki}, "
        f"Kayit: {kayit_sayisi}"
    )

cursor.close()
baglanti.close()

# Gecmis ortalamalarin ayni baslangic tarihinde
# sabit kalip kalmadigini kontrol et

baglanti = psycopg2.connect(
    host="localhost",
    port=5432,
    dbname="retail_ml_db",
    user="postgres",
    password=sifre
)

cursor = baglanti.cursor()

cursor.execute("""
    SELECT
        COUNT(*) AS grup_sayisi,
        COUNT(*) FILTER (
            WHERE farkli_7 > 1
               OR farkli_28 > 1
               OR farkli_59 > 1
        ) AS degisen_grup_sayisi
    FROM (
        SELECT
            magaza_id,
            baslangic_tarihi,
            COUNT(DISTINCT gecmis_7_gun_ortalama) AS farkli_7,
            COUNT(DISTINCT gecmis_28_gun_ortalama) AS farkli_28,
            COUNT(DISTINCT gecmis_59_gun_ortalama) AS farkli_59
        FROM yeni_ml_test
        GROUP BY magaza_id, baslangic_tarihi
    ) AS kontrol
""")

sonuc = cursor.fetchone()

print("\n--- GECMIS ORTALAMA KONTROLU ---")
print("Toplam magaza-baslangic grubu:", sonuc[0])
print("Ortalamasi degisen grup sayisi:", sonuc[1])

cursor.close()
baglanti.close()

# Gecmis ozet tablosunun sutunlarini incele

baglanti = psycopg2.connect(
    host="localhost",
    port=5432,
    dbname="retail_ml_db",
    user="postgres",
    password=sifre
)

cursor = baglanti.cursor()

cursor.execute("""
    SELECT column_name, data_type
    FROM information_schema.columns
    WHERE table_schema = 'public'
      AND table_name = 'donem_gecmis_temiz'
    ORDER BY ordinal_position
""")

print("\n--- DONEM GECMIS TEMIZ TABLOSU ---")

for sutun, veri_tipi in cursor.fetchall():
    print(f"{sutun}: {veri_tipi}")

cursor.close()
baglanti.close()

# Gunluk satis tablosunun sutunlarini kontrol et

baglanti = psycopg2.connect(
    host="localhost",
    port=5432,
    dbname="retail_ml_db",
    user="postgres",
    password=sifre
)

cursor = baglanti.cursor()

cursor.execute("""
    SELECT column_name, data_type
    FROM information_schema.columns
    WHERE table_schema = 'public'
      AND table_name = 'magaza_gunluk'
    ORDER BY ordinal_position
""")

print("\n--- MAGAZA GUNLUK TABLOSU ---")

for sutun, veri_tipi in cursor.fetchall():
    print(f"{sutun}: {veri_tipi}")

cursor.close()
baglanti.close()

# 7 gunluk gecmis ortalamayi kaynak verilerle karsilastir

baglanti = psycopg2.connect(
    host="localhost",
    port=5432,
    dbname="retail_ml_db",
    user="postgres",
    password=sifre
)

cursor = baglanti.cursor()

cursor.execute("""
    SELECT
        d.magaza_id,
        d.baslangic_tarihi,
        d.gecmis_7_gun_ortalama,
        (
            SELECT AVG(g.gunluk_satis)
            FROM magaza_gunluk g
            WHERE g.magaza_id = d.magaza_id
              AND g.tarih >= d.baslangic_tarihi - INTERVAL '7 days'
              AND g.tarih < d.baslangic_tarihi
        ) AS hesaplanan_ortalama
    FROM donem_gecmis_temiz d
    WHERE EXISTS (
        SELECT 1
        FROM yeni_ml_test t
        WHERE t.magaza_id = d.magaza_id
          AND t.baslangic_tarihi = d.baslangic_tarihi
    )
    ORDER BY d.baslangic_tarihi, d.magaza_id
    LIMIT 5
""")

print("\n--- 7 GUNLUK ORTALAMA DOGRULAMA ---")

for magaza, tarih, kayitli, hesaplanan in cursor.fetchall():
    print(f"\nMagaza: {magaza}")
    print(f"Baslangic tarihi: {tarih}")
    print(f"Veritabanindaki ortalama: {kayitli}")
    print(f"Yeniden hesaplanan ortalama: {hesaplanan}")

    if kayitli is not None and hesaplanan is not None:
        print(f"Mutlak fark: {abs(kayitli - hesaplanan)}")

cursor.close()
baglanti.close()

# Tum test baslangiclarinda gecmis ortalamalari dogrula

baglanti = psycopg2.connect(
    host="localhost",
    port=5432,
    dbname="retail_ml_db",
    user="postgres",
    password=sifre
)

cursor = baglanti.cursor()

cursor.execute("""
    WITH test_baslangiclari AS (
        SELECT DISTINCT magaza_id, baslangic_tarihi
        FROM yeni_ml_test
    ),
    kontrol AS (
        SELECT
            t.magaza_id,
            t.baslangic_tarihi,
            d.gecmis_7_gun_ortalama AS kayitli_7,
            d.gecmis_28_gun_ortalama AS kayitli_28,
            d.gecmis_59_gun_ortalama AS kayitli_59,
            AVG(g.gunluk_satis) FILTER (
                WHERE g.tarih >= t.baslangic_tarihi - 7
            ) AS hesaplanan_7,
            AVG(g.gunluk_satis) FILTER (
                WHERE g.tarih >= t.baslangic_tarihi - 28
            ) AS hesaplanan_28,
            AVG(g.gunluk_satis) AS hesaplanan_59
        FROM test_baslangiclari t
        LEFT JOIN donem_gecmis_temiz d
            ON d.magaza_id = t.magaza_id
           AND d.baslangic_tarihi = t.baslangic_tarihi
        LEFT JOIN magaza_gunluk g
            ON g.magaza_id = t.magaza_id
           AND g.tarih >= t.baslangic_tarihi - 59
           AND g.tarih < t.baslangic_tarihi
        GROUP BY
            t.magaza_id,
            t.baslangic_tarihi,
            d.gecmis_7_gun_ortalama,
            d.gecmis_28_gun_ortalama,
            d.gecmis_59_gun_ortalama
    )
    SELECT
        COUNT(*) AS toplam,
        COUNT(*) FILTER (
            WHERE kayitli_7 IS DISTINCT FROM hesaplanan_7
        ) AS farkli_7,
        COUNT(*) FILTER (
            WHERE kayitli_28 IS DISTINCT FROM hesaplanan_28
        ) AS farkli_28,
        COUNT(*) FILTER (
            WHERE kayitli_59 IS DISTINCT FROM hesaplanan_59
        ) AS farkli_59
    FROM kontrol
""")

sonuc = cursor.fetchone()

print("\n--- TUM GECMIS ORTALAMALARIN DOGRULANMASI ---")
print("Kontrol edilen grup:", sonuc[0])
print("7 gunluk farkli grup:", sonuc[1])
print("28 gunluk farkli grup:", sonuc[2])
print("59 gunluk farkli grup:", sonuc[3])

cursor.close()
baglanti.close()
