
import os
import pandas as pd
import matplotlib.pyplot as plt

# Gun 50 karsilastirma verilerini oku
veri = pd.read_csv(
    "reports/csv/uc_model_tahmin_karsilastirmasi.csv",
    parse_dates=["tahmin_tarihi"]
)

# Her gun icin tum magazalarin tahminlerini topla
gunluk = veri.groupby("tahmin_tarihi")[
    [
        "Ilk Random Forest",
        "Iyilestirilmis Random Forest",
        "HistGradientBoosting"
    ]
].sum().sort_index()

# Grafik olustur
plt.figure(figsize=(13, 6))

plt.plot(
    gunluk.index,
    gunluk["Ilk Random Forest"],
    label="Ilk Random Forest",
    linewidth=2
)

plt.plot(
    gunluk.index,
    gunluk["Iyilestirilmis Random Forest"],
    label="Iyilestirilmis Random Forest",
    linewidth=2
)

plt.plot(
    gunluk.index,
    gunluk["HistGradientBoosting"],
    label="HistGradientBoosting",
    linewidth=2
)

plt.title("Uc Modelin 59 Gunluk Satis Tahminleri")
plt.xlabel("Tahmin Tarihi")
plt.ylabel("Gunluk Toplam Tahmini Satis")
plt.legend()
plt.grid(True, alpha=0.3)
plt.xticks(rotation=45)
plt.tight_layout()

# Grafigi kaydet
os.makedirs("reports", exist_ok=True)

plt.savefig(
    "reports/grafikler/uc_model_tahmin_grafigi.png",
    dpi=300,
    bbox_inches="tight"
)

plt.show()

print("Grafik basariyla olusturuldu.")
print("Dosya: reports/grafikler/uc_model_tahmin_grafigi.png")
print("Karsilastirilan gun sayisi:", len(gunluk))
