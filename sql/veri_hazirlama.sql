-- Veri Hazirlama
-- Mevcut verilerden yeniden olusturulan SQL sorgusu.
-- 136150 kayit uzerinde dogrulandi.
-- Farkli kayit: 0, Eksik kayit: 0.
-- Bos magaza_gunluk tablosunda calistirilmalidir.

BEGIN;

LOCK TABLE magaza_gunluk IN SHARE ROW EXCLUSIVE MODE;

INSERT INTO magaza_gunluk (
    tarih,
    magaza_id,
    gunluk_satis,
    ortalama_fiyat,
    toplam_stok,
    urun_sayisi,
    promosyon1_sayisi,
    promosyon2_sayisi,
    magaza_tipi_id,
    magaza_boyutu,
    sehir_id
)
SELECT
    s.date,
    s.store_id,
    SUM(s.sales),
    AVG(s.price),
    SUM(s.stock),
    COUNT(DISTINCT s.product_id),
    COUNT(s.promo_bin_1),
    COUNT(s.promo_bin_2),
    m.storetype_id,
    m.store_size,
    m.city_id
FROM sales s
JOIN stores m ON s.store_id = m.store_id
WHERE s.date <= DATE '2019-10-31'
  AND NOT EXISTS (SELECT 1 FROM magaza_gunluk)
GROUP BY s.date, s.store_id,
         m.storetype_id, m.store_size, m.city_id;

COMMIT;
