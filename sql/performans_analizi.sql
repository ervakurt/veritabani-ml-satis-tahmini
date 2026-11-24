-- Veritabani Performans Analizi
-- Olcum tarihi: 24.11.2026
-- Tablo: magaza_gunluk
-- Toplam kayit: 136150
-- Sorgu sonucu: 61 kayit

-- 1. Mevcut indeksin kontrol edilmesi

SELECT tablename, indexname, indexdef
FROM pg_indexes
WHERE schemaname = 'public'
  AND tablename = 'magaza_gunluk';

-- 2. Indeksli performans olcumu

EXPLAIN (ANALYZE, BUFFERS)
SELECT *
FROM magaza_gunluk
WHERE magaza_id = 'S0001'
  AND tarih BETWEEN '2019-09-01' AND '2019-10-31';

-- 3. Indeks kullanimini gecici olarak kapatma

BEGIN;

SET LOCAL enable_indexscan = off;
SET LOCAL enable_bitmapscan = off;
SET LOCAL enable_indexonlyscan = off;

-- 4. Indekssiz performans olcumu

EXPLAIN (ANALYZE, BUFFERS)
SELECT *
FROM magaza_gunluk
WHERE magaza_id = 'S0001'
  AND tarih BETWEEN '2019-09-01' AND '2019-10-31';

-- 5. Gecici ayarlarin geri alinmasi

ROLLBACK;

-- OLCUM SONUCLARI (Execution Time)
-- Indeksli: 0.194, 0.196, 0.201 ms
-- Indekssiz: 285.761, 259.638, 236.247 ms
-- Ortalama indeksli: 0.197 ms
-- Ortalama indekssiz: 260.549 ms
-- Hizlanma: yaklasik 1323 kat
-- Sure azalmasi: %99.92
-- Indeksli blok erisimi: 64
-- Indekssiz blok erisimi: 3310
-- Blok erisimi azalmasi: %98.07
-- Sonuclar secilen sorguya ve test ortamina ozeldir.
-- pgAdmin'de olcum adimlari ayri ayri calistirilmalidir.
