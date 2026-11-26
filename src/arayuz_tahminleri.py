
import streamlit as st
import pandas as pd
import psycopg2
from psycopg2 import sql
from contextlib import closing


MODELLER = {
    "İlk Random Forest": "satis_tahminleri",
    "İyileştirilmiş Random Forest":
        "satis_tahminleri_rf_iyilestirilmis",
    "HistGradientBoosting":
        "satis_tahminleri_hist_gradient"
}


def sayi_formatla(sayi, basamak=0):
    return (
        f"{sayi:,.{basamak}f}"
        .replace(",", "_")
        .replace(".", ",")
        .replace("_", ".")
    )


def satis_tahminleri(sifre):

    st.title("Satış Tahminleri")
    st.caption("Model ve mağaza bazlı satış tahmin analizi")

    if not sifre:
        st.info("Lütfen PostgreSQL şifrenizi giriniz.")
        return

    model = st.selectbox(
        "Makine öğrenmesi modeli",
        list(MODELLER.keys()),
        index=1
    )

    tablo = sql.Identifier("public", MODELLER[model])

    try:
        with closing(psycopg2.connect(
            host="localhost",
            port=5432,
            database="retail_ml_db",
            user="postgres",
            password=sifre,
            connect_timeout=5
        )) as conn:

            conn.set_session(readonly=True)

            with conn.cursor() as cur:

                cur.execute(
                    sql.SQL("""
                        SELECT DISTINCT magaza_id
                        FROM {}
                        ORDER BY magaza_id
                    """).format(tablo)
                )

                magazalar = [
                    kayit[0] for kayit in cur.fetchall()
                ]

                cur.execute(
                    sql.SQL("""
                        SELECT MIN(tahmin_tarihi),
                               MAX(tahmin_tarihi)
                        FROM {}
                    """).format(tablo)
                )

                ilk_tarih, son_tarih = cur.fetchone()

                if not magazalar or ilk_tarih is None:
                    st.warning("Tahmin kaydı bulunamadı.")
                    return

                magaza = st.selectbox(
                    "Mağaza seçiniz",
                    ["Tüm mağazalar"] + magazalar
                )

                sol, sag = st.columns(2)

                baslangic = sol.date_input(
                    "Başlangıç tarihi",
                    value=ilk_tarih,
                    min_value=ilk_tarih,
                    max_value=son_tarih
                )

                bitis = sag.date_input(
                    "Bitiş tarihi",
                    value=son_tarih,
                    min_value=ilk_tarih,
                    max_value=son_tarih
                )

                if baslangic > bitis:
                    st.warning("Tarih aralığı geçersiz.")
                    return

                sorgu = sql.SQL("""
                    SELECT magaza_id,
                           tahmin_tarihi,
                           tahmin_gunu,
                           tahmini_satis::double precision
                    FROM {}
                    WHERE tahmin_tarihi BETWEEN %s AND %s
                """).format(tablo)

                parametreler = [baslangic, bitis]

                if magaza != "Tüm mağazalar":
                    sorgu += sql.SQL(
                        " AND magaza_id = %s"
                    )
                    parametreler.append(magaza)

                sorgu += sql.SQL(
                    " ORDER BY tahmin_tarihi, magaza_id"
                )

                cur.execute(sorgu, parametreler)

                df = pd.DataFrame(
                    cur.fetchall(),
                    columns=[
                        "magaza_id",
                        "tahmin_tarihi",
                        "tahmin_gunu",
                        "tahmini_satis"
                    ]
                )

        st.sidebar.success("PostgreSQL bağlantısı başarılı")

    except psycopg2.Error:
        st.error("Veritabanı bağlantısı veya sorgu hatası.")
        return

    if df.empty:
        st.warning("Seçilen filtrelere uygun kayıt bulunamadı.")
        return

    df["tahmin_tarihi"] = pd.to_datetime(
        df["tahmin_tarihi"]
    )

    st.divider()

    col1, col2, col3 = st.columns(3)

    col1.metric(
        "Toplam tahmini satış",
        sayi_formatla(df["tahmini_satis"].sum(), 2),
        border=True
    )

    col2.metric(
        "Mağaza sayısı",
        sayi_formatla(df["magaza_id"].nunique()),
        border=True
    )

    col3.metric(
        "Tahmin kaydı",
        sayi_formatla(len(df)),
        border=True
    )

    st.subheader("Günlük Satış Tahminleri")

    gunluk = (
        df.groupby("tahmin_tarihi", as_index=False)
        ["tahmini_satis"].sum()
    )

    st.line_chart(
        gunluk,
        x="tahmin_tarihi",
        y="tahmini_satis",
        color="#60A5FA"
    )

    st.subheader("Tahmin Sonuçları")

    st.dataframe(
        df,
        hide_index=True
    )

    st.download_button(
        label="Tahminleri CSV olarak indir",
        data=df.to_csv(index=False).encode("utf-8-sig"),
        file_name="satis_tahminleri.csv",
        mime="text/csv"
    )

    st.caption(
        f"Veri kaynağı: PostgreSQL / {MODELLER[model]}"
    )
