-- Satis Tahmin Sistemi - Analiz Sorgulari

-- pgAdmin sorgu gecmisinden kurtarilmistir.

-- Sorgu 2
SELECT
    magaza_id,
    tahmin_tarihi,
    tahmin_gunu,
    tahmini_satis
FROM satis_tahminleri_rf_iyilestirilmis
ORDER BY magaza_id, tahmin_tarihi
LIMIT 10;

-- Sorgu 3
SELECT
    COUNT(*) AS toplam_tahmin,
    COUNT(DISTINCT magaza_id) AS magaza_sayisi,
    MIN(tahmin_tarihi) AS ilk_tarih,
    MAX(tahmin_tarihi) AS son_tarih,
    ROUND(SUM(tahmini_satis), 2) AS toplam_satis
FROM satis_tahminleri_rf_iyilestirilmis;

-- Sorgu 4
SELECT table_name
FROM information_schema.tables
WHERE table_schema = 'public'
  AND table_name ILIKE '%tahmin%'
ORDER BY table_name;

-- Sorgu 7
SELECT
    'Ilk Random Forest' AS model,
    COUNT(*) AS tahmin_sayisi,
    ROUND(SUM(tahmini_satis)::NUMERIC, 2)
        AS toplam_tahmini_satis
FROM satis_tahminleri

UNION ALL

SELECT
    'Iyilestirilmis Random Forest',
    COUNT(*),
    ROUND(SUM(tahmini_satis)::NUMERIC, 2)
FROM satis_tahminleri_rf_iyilestirilmis

UNION ALL

SELECT
    'HistGradientBoosting',
    COUNT(*),
    ROUND(SUM(tahmini_satis)::NUMERIC, 2)
FROM satis_tahminleri_hist_gradient;

-- Sorgu 8
SELECT
    a.magaza_id,
    ROUND(SUM(a.tahmini_satis)::NUMERIC, 2)
        AS ilk_random_forest,
    ROUND(SUM(b.tahmini_satis)::NUMERIC, 2)
        AS iyilestirilmis_random_forest,
    ROUND(SUM(c.tahmini_satis)::NUMERIC, 2)
        AS hist_gradient
FROM satis_tahminleri a
JOIN satis_tahminleri_rf_iyilestirilmis b
    ON a.magaza_id = b.magaza_id
    AND a.tahmin_tarihi = b.tahmin_tarihi
JOIN satis_tahminleri_hist_gradient c
    ON a.magaza_id = c.magaza_id
    AND a.tahmin_tarihi = c.tahmin_tarihi
GROUP BY a.magaza_id
ORDER BY a.magaza_id;

-- Sorgu 9
SELECT
    a.magaza_id,
    ROUND(SUM(a.tahmini_satis)::NUMERIC, 2)
        AS iyilestirilmis_rf,
    ROUND(SUM(b.tahmini_satis)::NUMERIC, 2)
        AS hist_gradient,
    ROUND(
        ABS(
            SUM(a.tahmini_satis) -
            SUM(b.tahmini_satis)
        )::NUMERIC, 2
    ) AS mutlak_fark
FROM satis_tahminleri_rf_iyilestirilmis a
JOIN satis_tahminleri_hist_gradient b
    ON a.magaza_id = b.magaza_id
    AND a.tahmin_tarihi = b.tahmin_tarihi
GROUP BY a.magaza_id
ORDER BY mutlak_fark DESC
LIMIT 10;

-- Sorgu 10
SELECT
    a.magaza_id,

    ROUND(SUM(a.tahmini_satis)::NUMERIC, 2)
        AS iyilestirilmis_rf,

    ROUND(SUM(b.tahmini_satis)::NUMERIC, 2)
        AS hist_gradient,

    ROUND(
        (
            100.0 * ABS(
                SUM(a.tahmini_satis) -
                SUM(b.tahmini_satis)
            ) / NULLIF(SUM(b.tahmini_satis), 0)
        )::NUMERIC,
        2
    ) AS yuzde_fark

FROM satis_tahminleri_rf_iyilestirilmis a

JOIN satis_tahminleri_hist_gradient b
    ON a.magaza_id = b.magaza_id
    AND a.tahmin_tarihi = b.tahmin_tarihi

GROUP BY a.magaza_id

ORDER BY yuzde_fark DESC NULLS LAST

LIMIT 10;

-- Sorgu 11
SELECT
    table_name,
    column_name,
    data_type,
    is_nullable
FROM information_schema.columns
WHERE table_schema = 'public'
ORDER BY table_name, ordinal_position;

-- Sorgu 13
SELECT
    COUNT(*) AS toplam_kayit,
    COUNT(DISTINCT magaza_id) AS magaza_sayisi,
    MIN(tahmin_tarihi) AS ilk_tarih,
    MAX(tahmin_tarihi) AS son_tarih,
    ROUND(SUM(tahmini_satis), 2) AS toplam_satis
FROM satis_tahminleri_hist_gradient;
