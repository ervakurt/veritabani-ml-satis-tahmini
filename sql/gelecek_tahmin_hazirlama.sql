-- Gelecek Tahmin Verilerinin Hazirlanmasi

-- 1. Magazalarin son satis ortalamalarinin hesaplanmasi
-- 144 kayit uzerinde dogrulandi.
-- Farkli kayit: 0, Eksik kayit: 0.

BEGIN;

LOCK TABLE magaza_gecmis_ozet IN SHARE ROW EXCLUSIVE MODE;

INSERT INTO magaza_gecmis_ozet
SELECT
    magaza_id,
    AVG(gunluk_satis) FILTER (
        WHERE tarih >= DATE '2019-11-01' - 7
    ),
    AVG(gunluk_satis) FILTER (
        WHERE tarih >= DATE '2019-11-01' - 28
    ),
    AVG(gunluk_satis)
FROM magaza_gunluk
WHERE tarih >= DATE '2019-11-01' - 59
  AND tarih < DATE '2019-11-01'
  AND NOT EXISTS (
      SELECT 1 FROM magaza_gecmis_ozet
  )
GROUP BY magaza_id;

COMMIT;

-- 2. 59 gunluk gelecek tahmin verisinin hazirlanmasi
-- 139 magaza, 59 gun, toplam 8201 kayit.
-- Farkli kayit: 0, Eksik kayit: 0.
-- Son 7 gunluk satis ortalamasi pozitif olan magazalar secilir.

BEGIN;

LOCK TABLE gelecek_tahmin_verisi IN SHARE ROW EXCLUSIVE MODE;

INSERT INTO gelecek_tahmin_verisi
SELECT
    m.magaza_id,
    DATE '2019-11-01' + g.gun,
    g.gun + 1,
    EXTRACT(DOW FROM DATE '2019-11-01' + g.gun),
    EXTRACT(MONTH FROM DATE '2019-11-01' + g.gun),
    m.son_7_gun_ortalama,
    m.son_28_gun_ortalama,
    m.son_59_gun_ortalama
FROM magaza_gecmis_ozet m
CROSS JOIN generate_series(0, 58) AS g(gun)
WHERE m.son_7_gun_ortalama > 0
  AND NOT EXISTS (
      SELECT 1 FROM gelecek_tahmin_verisi
  );

COMMIT;
