-- Egitim ve Test Verilerinin Hazirlanmasi

-- 1. Tahmin donemlerinin olusturulmasi
-- Yeniden olusturulan sorgu 123 kayit uzerinde dogrulandi.
-- Farkli kayit: 0, Eksik kayit: 0.

BEGIN;

LOCK TABLE tahmin_donemleri IN SHARE ROW EXCLUSIVE MODE;

INSERT INTO tahmin_donemleri (baslangic_tarihi)
SELECT generate_series(
    DATE '2017-05-01',
    DATE '2019-09-02',
    INTERVAL '7 days'
)::date
WHERE NOT EXISTS (
    SELECT 1 FROM tahmin_donemleri
);

COMMIT;

-- 2. Donem gecmis satis ortalamalarinin hesaplanmasi
-- Yeniden olusturulan sorgu 16448 kayit uzerinde dogrulandi.
-- Farkli kayit: 0, Eksik kayit: 0.

BEGIN;

LOCK TABLE donem_gecmis_ozet IN SHARE ROW EXCLUSIVE MODE;

INSERT INTO donem_gecmis_ozet (
    baslangic_tarihi,
    magaza_id,
    gecmis_7_gun_ortalama,
    gecmis_28_gun_ortalama,
    gecmis_59_gun_ortalama,
    gecmis_kayit_sayisi
)
SELECT
    d.baslangic_tarihi,
    m.magaza_id,
    AVG(m.gunluk_satis) FILTER (
        WHERE m.tarih >= d.baslangic_tarihi - 7
    ),
    AVG(m.gunluk_satis) FILTER (
        WHERE m.tarih >= d.baslangic_tarihi - 28
    ),
    AVG(m.gunluk_satis),
    COUNT(*)
FROM tahmin_donemleri d
JOIN magaza_gunluk m
    ON m.tarih >= d.baslangic_tarihi - 59
    AND m.tarih < d.baslangic_tarihi
WHERE NOT EXISTS (
    SELECT 1 FROM donem_gecmis_ozet
)
GROUP BY d.baslangic_tarihi, m.magaza_id;

COMMIT;

-- 3. Eksik gecmis kayitlarinin elenmesi
-- 16076 kayit uzerinde dogrulandi.
-- Farkli kayit: 0, Eksik kayit: 0.

BEGIN;

LOCK TABLE donem_gecmis_temiz IN SHARE ROW EXCLUSIVE MODE;

INSERT INTO donem_gecmis_temiz
SELECT *
FROM donem_gecmis_ozet
WHERE gecmis_kayit_sayisi = 59
  AND NOT EXISTS (
      SELECT 1 FROM donem_gecmis_temiz
  );

COMMIT;

-- 4. Makine ogrenmesi veri setinin hazirlanmasi
-- 945746 kayit uzerinde dogrulandi.
-- Farkli kayit: 0, Eksik kayit: 0.

BEGIN;

LOCK TABLE yeni_ml_egitim IN SHARE ROW EXCLUSIVE MODE;

INSERT INTO yeni_ml_egitim
SELECT
    d.magaza_id,
    d.baslangic_tarihi,
    m.tarih AS tahmin_tarihi,
    (m.tarih - d.baslangic_tarihi + 1),
    EXTRACT(DOW FROM m.tarih),
    EXTRACT(MONTH FROM m.tarih),
    d.gecmis_7_gun_ortalama,
    d.gecmis_28_gun_ortalama,
    d.gecmis_59_gun_ortalama,
    m.gunluk_satis
FROM donem_gecmis_temiz d
JOIN magaza_gunluk m
    ON d.magaza_id = m.magaza_id
    AND m.tarih >= d.baslangic_tarihi
    AND m.tarih < d.baslangic_tarihi + 59
WHERE NOT EXISTS (
    SELECT 1 FROM yeni_ml_egitim
);

COMMIT;

-- 5. Egitim veri setinin olusturulmasi
-- 622454 kayit uzerinde dogrulandi.
-- Farkli kayit: 0, Eksik kayit: 0.

BEGIN;

LOCK TABLE yeni_ml_egitim_temiz IN SHARE ROW EXCLUSIVE MODE;

INSERT INTO yeni_ml_egitim_temiz
SELECT *
FROM yeni_ml_egitim
WHERE tahmin_tarihi <= DATE '2018-12-31'
  AND NOT EXISTS (
      SELECT 1 FROM yeni_ml_egitim_temiz
  );

COMMIT;

-- 6. Test veri setinin olusturulmasi
-- 286304 kayit uzerinde dogrulandi.
-- Farkli kayit: 0, Eksik kayit: 0.

BEGIN;

LOCK TABLE yeni_ml_test IN SHARE ROW EXCLUSIVE MODE;

INSERT INTO yeni_ml_test
SELECT *
FROM yeni_ml_egitim
WHERE baslangic_tarihi >= DATE '2019-01-07'
  AND NOT EXISTS (
      SELECT 1 FROM yeni_ml_test
  );

COMMIT;
