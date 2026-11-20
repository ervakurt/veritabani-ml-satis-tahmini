
import pandas as pd
import matplotlib.pyplot as plt

# Iki modelin tahminlerini oku
rf = pd.read_csv(
    "reports/59_gunluk_satis_tahminleri.csv"
)

hgb = pd.read_csv(
    "reports/hist_gradient_59_gunluk_tahmin.csv"
)

# S0085 magazasini sec
magaza = "S0085"

rf = rf[rf["magaza_id"] == magaza].copy()
hgb = hgb[hgb["magaza_id"] == magaza].copy()

# Tarihleri duzenle
rf["tahmin_tarihi"] = pd.to_datetime(
    rf["tahmin_tarihi"]
)

hgb["tahmin_tarihi"] = pd.to_datetime(
    hgb["tahmin_tarihi"]
)

rf = rf.sort_values("tahmin_tarihi")
hgb = hgb.sort_values("tahmin_tarihi")

# Kayit sayilarini kontrol et
if len(rf) != 59 or len(hgb) != 59:
    raise ValueError("S0085 icin 59 gunluk tahmin bulunamadi!")

# Toplam tahminleri hesapla
rf_toplam = rf["tahmini_satis"].sum()
hgb_toplam = hgb["tahmini_satis"].sum()

print("\n--- S0085 MAGAZASI ---")
print(f"Random Forest toplam: {rf_toplam:.2f}")
print(f"HistGradientBoosting toplam: {hgb_toplam:.2f}")
print(f"Tahmin farki: {hgb_toplam - rf_toplam:.2f}")

# Grafigi olustur
plt.figure(figsize=(14, 6))

plt.plot(
    rf["tahmin_tarihi"],
    rf["tahmini_satis"],
    label="Random Forest",
    color="royalblue",
    linewidth=2
)

plt.plot(
    hgb["tahmin_tarihi"],
    hgb["tahmini_satis"],
    label="HistGradientBoosting",
    color="darkorange",
    linewidth=2
)

plt.title("S0085 Magazasi - 59 Gunluk Satis Tahminleri")
plt.xlabel("Tarih")
plt.ylabel("Tahmini Gunluk Satis")

plt.legend()
plt.grid(alpha=0.3)
plt.xticks(rotation=45)
plt.tight_layout()

# Grafigi kaydet
dosya = "reports/gun20_S0085_tahmin_grafigi.png"

plt.savefig(
    dosya,
    dpi=300,
    bbox_inches="tight"
)

print("\nGrafik kaydedildi:", dosya)

plt.show()
