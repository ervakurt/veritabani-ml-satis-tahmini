
import os
import pandas as pd

# Modellerin tahmin dosyalari
dosyalar = {
    "Ilk Random Forest":
        "reports/59_gunluk_satis_tahminleri.csv",
    "Iyilestirilmis Random Forest":
        "reports/iyilestirilmis_rf_59_gunluk_tahmin.csv",
    "HistGradientBoosting":
        "reports/hist_gradient_59_gunluk_tahmin.csv"
}

veriler = []
ozetler = []

for model_adi, dosya in dosyalar.items():
    veri = pd.read_csv(dosya)

    gerekli = {
        "magaza_id", "tahmin_tarihi", "tahmini_satis"
    }
    if not gerekli.issubset(veri.columns):
        raise ValueError(
            f"{model_adi} dosyasinda gerekli sutunlar eksik."
        )

    veri["tahmin_tarihi"] = pd.to_datetime(
        veri["tahmin_tarihi"]
    )

    if veri.duplicated(
        ["magaza_id", "tahmin_tarihi"]
    ).any():
        raise ValueError(
            f"{model_adi} dosyasinda tekrar eden tahminler var."
        )

    ozetler.append({
        "model": model_adi,
        "tahmin_sayisi": len(veri),
        "magaza_sayisi": veri["magaza_id"].nunique(),
        "toplam_tahmini_satis": veri["tahmini_satis"].sum(),
        "ortalama_gunluk_magaza_satisi":
            veri["tahmini_satis"].mean()
    })

    veriler.append(
        veri[[
            "magaza_id", "tahmin_tarihi", "tahmini_satis"
        ]].rename(
            columns={"tahmini_satis": model_adi}
        )
    )

# Ayni magaza ve tarihe ait tahminleri eslestir
karsilastirma = veriler[0]

for veri in veriler[1:]:
    karsilastirma = karsilastirma.merge(
        veri,
        on=["magaza_id", "tahmin_tarihi"],
        how="inner",
        validate="one_to_one"
    )

if len(karsilastirma) != len(veriler[0]) or any(
    len(karsilastirma) != len(veri)
    for veri in veriler[1:]
):
    raise ValueError(
        "Modellerin magaza-tarih tahminleri tam eslesmiyor."
    )

# Model tahminleri arasindaki farklar
karsilastirma["RF_iyilestirme_farki"] = (
    karsilastirma["Iyilestirilmis Random Forest"]
    - karsilastirma["Ilk Random Forest"]
)

karsilastirma["RF_HistGradient_farki"] = (
    karsilastirma["Iyilestirilmis Random Forest"]
    - karsilastirma["HistGradientBoosting"]
)

# Ozet tablo
ozet = pd.DataFrame(ozetler)

os.makedirs("reports", exist_ok=True)

ozet.to_csv(
    "reports/gun50_model_ozeti.csv",
    index=False,
    encoding="utf-8-sig"
)

karsilastirma.to_csv(
    "reports/gun50_tahmin_karsilastirma.csv",
    index=False,
    encoding="utf-8-sig"
)

print("\n--- GUN 50 MODEL KARSILASTIRMASI ---")
print(ozet.round(2).to_string(index=False))

print("\nKarsilastirilan magaza-tarih sayisi:",
      len(karsilastirma))

print("\nIlk 5 karsilastirma:")
print(
    karsilastirma.head(5).round(2).to_string(index=False)
)

print("\nSonuclar reports klasorune kaydedildi.")
