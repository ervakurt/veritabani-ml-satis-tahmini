
import pandas as pd
import matplotlib.pyplot as plt

# Iki modelin tahminlerini oku
rf = pd.read_csv(
   "reports/csv/59_gunluk_satis_tahminleri.csv"
)

hgb = pd.read_csv(
    "reports/csv/hist_gradient_59_gunluk_tahmin.csv"
)

# Tarihleri duzenle
rf["tahmin_tarihi"] = pd.to_datetime(
    rf["tahmin_tarihi"]
)

hgb["tahmin_tarihi"] = pd.to_datetime(
    hgb["tahmin_tarihi"]
)

# Gunluk toplam satis tahminlerini hesapla
rf_gunluk = rf.groupby(
    "tahmin_tarihi"
)["tahmini_satis"].sum()

hgb_gunluk = hgb.groupby(
    "tahmin_tarihi"
)["tahmini_satis"].sum()

# Grafigi olustur
plt.figure(figsize=(14, 6))

plt.plot(
    rf_gunluk.index,
    rf_gunluk.values,
    label="Random Forest",
    color="royalblue",
    linewidth=2
)

plt.plot(
    hgb_gunluk.index,
    hgb_gunluk.values,
    label="HistGradientBoosting",
    color="darkorange",
    linewidth=2
)

plt.title(
    "59 Gunluk Satis Tahminleri - Model Karsilastirmasi"
)

plt.xlabel("Tarih")
plt.ylabel("Tahmini Gunluk Toplam Satis")

plt.legend()
plt.grid(alpha=0.3)
plt.xticks(rotation=45)
plt.tight_layout()

# Grafigi kaydet
dosya = "reports/grafikler/iki_model_grafik_karsilastirmasi.png"

plt.savefig(
    dosya,
    dpi=300,
    bbox_inches="tight"
)

print("Grafik kaydedildi:", dosya)

plt.show()
