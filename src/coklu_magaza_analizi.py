
import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path

# Tahmin dosyalarini oku
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

# Incelenecek magazalar
magazalar = ["S0020", "S0026", "S0038"]

# Rapor klasorunu kontrol et
Path("reports").mkdir(exist_ok=True)

sonuclar = []

for magaza in magazalar:
    rf_magaza = rf[
        rf["magaza_id"] == magaza
    ].sort_values("tahmin_tarihi")

    hgb_magaza = hgb[
        hgb["magaza_id"] == magaza
    ].sort_values("tahmin_tarihi")

    # Her magaza icin 59 gunluk kayit kontrolu
    if len(rf_magaza) != 59 or len(hgb_magaza) != 59:
        raise ValueError(
            f"{magaza} icin 59 gunluk veri bulunamadi!"
        )

    if not rf_magaza["tahmin_tarihi"].reset_index(
        drop=True
    ).equals(
        hgb_magaza["tahmin_tarihi"].reset_index(
            drop=True
        )
    ):
        raise ValueError(
            f"{magaza} icin tahmin tarihleri eslesmiyor!"
        )

    rf_toplam = rf_magaza["tahmini_satis"].sum()
    hgb_toplam = hgb_magaza["tahmini_satis"].sum()

    fark = hgb_toplam - rf_toplam

    sonuclar.append({
        "magaza_id": magaza,
        "random_forest": round(rf_toplam, 2),
        "hist_gradient": round(hgb_toplam, 2),
        "fark": round(fark, 2)
    })

    # Grafik olustur
    plt.figure(figsize=(12, 5))

    plt.plot(
        rf_magaza["tahmin_tarihi"],
        rf_magaza["tahmini_satis"],
        label="Random Forest",
        color="royalblue",
        linewidth=2
    )

    plt.plot(
        hgb_magaza["tahmin_tarihi"],
        hgb_magaza["tahmini_satis"],
        label="HistGradientBoosting",
        color="darkorange",
        linewidth=2
    )

    plt.title(
        f"{magaza} - 59 Gunluk Satis Tahminleri"
    )
    plt.xlabel("Tarih")
    plt.ylabel("Tahmini Gunluk Satis")
    plt.legend()
    plt.grid(alpha=0.3)
    plt.xticks(rotation=45)
    plt.tight_layout()

    dosya = f"reports/grafikler/{magaza}_tahmin_grafigi.png"

    plt.savefig(
        dosya,
        dpi=300,
        bbox_inches="tight"
    )

    plt.close()

    print(f"{magaza} grafigi kaydedildi.")

# Sonuc tablosunu olustur
sonuc_tablosu = pd.DataFrame(sonuclar)

print("\n--- MAGAZA KARSILASTIRMASI ---")
print(sonuc_tablosu.to_string(index=False))

# CSV raporunu kaydet
sonuc_tablosu.to_csv(
    "reports/csv/magaza_analizi.csv",
    index=False,
    encoding="utf-8-sig"
)


print("\nTum grafikler ve rapor kaydedildi.")
