
import pandas as pd
import matplotlib.pyplot as plt

veri = pd.read_csv("reports/csv/59_gunluk_satis_tahminleri.csv")

veri["tahmin_tarihi"] = pd.to_datetime(veri["tahmin_tarihi"])

gunluk = veri.groupby("tahmin_tarihi")["tahmini_satis"].sum()

plt.figure(figsize=(12, 5))
plt.plot(gunluk.index, gunluk.values, marker="o", markersize=3)

plt.title("59 Günlük Toplam Satış Tahmini")
plt.xlabel("Tarih")
plt.ylabel("Tahmini Satış Miktarı")
plt.xticks(rotation=45)
plt.grid(True, alpha=0.3)
plt.tight_layout()

plt.savefig("reports/grafikler/59_gunluk_satis_grafigi.png", dpi=150)

plt.show()

print("Satış tahmin grafiği başarıyla kaydedildi!")
