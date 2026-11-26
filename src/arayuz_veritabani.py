
import streamlit as st
import pandas as pd
import psycopg2
from psycopg2 import sql
from contextlib import closing


def veritabani_analizi(sifre):

    st.title("Veritabanı Analizi")
    st.caption("PostgreSQL tablo yapısı ve sorgu performansı")

    if not sifre:
        st.warning("Veritabanı bağlantı ayarları eksik.")
        return

    tablolar = [
        "sales",
        "stores",
        "products",
        "magaza_gunluk",
        "yeni_ml_egitim_temiz",
        "yeni_ml_test",
        "gelecek_tahmin_verisi",
        "satis_tahminleri",
        "satis_tahminleri_rf_iyilestirilmis",
        "satis_tahminleri_hist_gradient"
    ]

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
                    SELECT COUNT(*)
                    FROM information_schema.tables
                    WHERE table_schema = 'public'
                    AND table_type = 'BASE TABLE'
                """)

                tablo_sayisi = cur.fetchone()[0]

                veriler = []

                for tablo in tablolar:
                    cur.execute(
                        sql.SQL("SELECT COUNT(*) FROM {}")
                        .format(sql.Identifier("public", tablo))
                    )

                    veriler.append([
                        tablo,
                        cur.fetchone()[0]
                    ])

        st.sidebar.success("PostgreSQL bağlantısı başarılı")

    except psycopg2.Error:
        st.error("Veritabanı bağlantısı veya sorgu hatası.")
        return

    st.metric("Toplam tablo sayısı", tablo_sayisi)

    st.subheader("Temel Veritabanı Tabloları")

    df = pd.DataFrame(
        veriler,
        columns=["Tablo", "Kayıt Sayısı"]
    )

    st.dataframe(df, hide_index=True)

    st.caption("Kayıt sayıları doğrudan PostgreSQL'den alınmıştır.")

    st.divider()

    st.subheader("İndeks Performansı")

    performans = pd.DataFrame({
        "Sorgu": [
            "İndeksli",
            "İndeks kullanımı kapalı"
        ],
        "Süre (ms)": [0.197, 260.549],
        "Bellek Bloğu Erişimi": [64, 3310]
    })

    st.dataframe(performans, hide_index=True)

    st.bar_chart(
        performans,
        x="Sorgu",
        y="Süre (ms)",
        color="#60A5FA"
    )

    st.write(
        "Birleşik B-tree indeksi sayesinde test edilen "
        "sorgunun çalışma süresi yaklaşık %99,92 azalmıştır."
    )

    st.caption(
        "Performans değerleri daha önce yapılan üç ölçümün "
        "sonuçlarına dayanmaktadır."
    )
