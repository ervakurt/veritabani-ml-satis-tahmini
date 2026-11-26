
import streamlit as st
import pandas as pd
import psycopg2
from psycopg2 import sql
from contextlib import closing
from src.arayuz_tahminleri import MODELLER


def magaza_analizi(sifre):

    st.title("Mağaza Analizi")
    st.caption("Üç modelin mağaza bazlı satış tahminleri")

    if not sifre:
        st.info("Lütfen PostgreSQL şifrenizi giriniz.")
        return

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

                cur.execute("""
                    SELECT magaza_id FROM public.satis_tahminleri
                    INTERSECT
                    SELECT magaza_id FROM public.satis_tahminleri_rf_iyilestirilmis
                    INTERSECT
                    SELECT magaza_id FROM public.satis_tahminleri_hist_gradient
                    ORDER BY magaza_id
                """)

                magazalar = [satir[0] for satir in cur.fetchall()]

                if not magazalar:
                    st.warning("Ortak mağaza kaydı bulunamadı.")
                    return

                magaza = st.selectbox("Mağaza seçiniz", magazalar)

                veriler = []

                for model, tablo in MODELLER.items():

                    cur.execute(
                        sql.SQL("""
                            SELECT tahmin_tarihi,
                                   tahmini_satis::double precision
                            FROM {}
                            WHERE magaza_id = %s
                            ORDER BY tahmin_tarihi
                        """).format(sql.Identifier("public", tablo)),
                        (magaza,)
                    )

                    for tarih, satis in cur.fetchall():
                        veriler.append([tarih, model, satis])

        st.sidebar.success("PostgreSQL bağlantısı başarılı")

    except psycopg2.Error:
        st.error("Veritabanı bağlantısı veya sorgu hatası.")
        return

    df = pd.DataFrame(
        veriler,
        columns=["Tarih", "Model", "Tahmini Satış"]
    )

    df["Tarih"] = pd.to_datetime(df["Tarih"])

    st.subheader("Toplam Satış Tahminleri")

    ozet = df.groupby(
        "Model", as_index=False
    )["Tahmini Satış"].sum()

    st.dataframe(ozet.round(2), hide_index=True)

    st.subheader("Günlük Tahmin Karşılaştırması")

    st.line_chart(
        df,
        x="Tarih",
        y="Tahmini Satış",
        color="Model"
    )

    st.caption("Veri kaynağı: PostgreSQL tahmin tabloları")
