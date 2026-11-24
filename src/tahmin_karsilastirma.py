
import pandas as pd

# Iki modelin tahminlerini oku
rf = pd.read_csv(
    "reports/csv/59_gunluk_satis_tahminleri.csv"
)

hgb = pd.read_csv(
    "reports/csv/hist_gradient_59_gunluk_tahmin.csv"
)

# Magaza ve tarihe gore birlestir
karsilastirma = pd.merge(
    rf[["magaza_id", "tahmin_tarihi", "tahmini_satis"]],
    hgb[["magaza_id", "tahmin_tarihi", "tahmini_satis"]],
    on=["magaza_id", "tahmin_tarihi"],
    how="inner",
    suffixes=("_rf", "_hgb"),
    validate="one_to_one"
)

if len(karsilastirma) != len(rf) or len(karsilastirma) != len(hgb):
    raise ValueError("Iki dosyanin tahmin kayitlari tam eslesmiyor!")

# Tahmin farklarini hesapla
karsilastirma["fark"] = (
    karsilastirma["tahmini_satis_hgb"]
    - karsilastirma["tahmini_satis_rf"]
)

# Magaza bazinda toplam tahminler
magaza_ozet = karsilastirma.groupby(
    "magaza_id", as_index=False
).agg(
    random_forest=("tahmini_satis_rf", "sum"),
    hist_gradient=("tahmini_satis_hgb", "sum"),
    fark=("fark", "sum")
)

magaza_ozet["mutlak_fark"] = magaza_ozet["fark"].abs()

# En buyuk fark olan 10 magaza
en_buyuk_farklar = magaza_ozet.sort_values(
    "mutlak_fark", ascending=False
).head(10)

print("\n--- GENEL KARSILASTIRMA ---")
print("Eslesen tahmin:", len(karsilastirma))
print("Magaza sayisi:", karsilastirma["magaza_id"].nunique())

print(
    "Random Forest toplam:",
    round(karsilastirma["tahmini_satis_rf"].sum(), 2)
)

print(
    "HistGradientBoosting toplam:",
    round(karsilastirma["tahmini_satis_hgb"].sum(), 2)
)

print("\n--- EN BUYUK FARK OLAN 10 MAGAZA ---")
print(en_buyuk_farklar.to_string(index=False))

# Raporlari kaydet
karsilastirma.to_csv(
    "reports/csv/iki_model_tahmin_karsilastirmasi.csv",
    index=False,
    encoding="utf-8-sig"
)

magaza_ozet.to_csv(
    "reports/csv/magaza_karsilastirmasi.csv",
    index=False,
    encoding="utf-8-sig"
)

print("\nKarsilastirma raporlari kaydedildi.")
