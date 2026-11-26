
import streamlit as st
import psycopg2
from contextlib import closing

st.set_page_config(
    page_title="Mağaza Satış Tahmin Sistemi",
    page_icon="📊",
    layout="wide"
)

# Tasarım
st.markdown("""
<style>
.block-container {
    padding-top: 2rem;
    padding-bottom: 2rem;
}
.hero-box {
    background-color: #161616;
    padding: 28px;
    border-radius: 18px;
    border: 1px solid #2a2a2a;
    margin-bottom: 20px;
    color: #ffffff;
}
.hero-title {
    font-size: 36px;
    font-weight: 700;
    margin-bottom: 10px;
}
.hero-text {
    font-size: 17px;
    color: #d0d0d0;
}
</style>
""", unsafe_allow_html=True)


# PostgreSQL bağlantısı
def genel_ozet(sifre):
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
                SELECT
                    (SELECT COUNT(*) FROM public.sales),
                    (SELECT COUNT(*) FROM public.stores),
                    (SELECT COUNT(*) FROM public.products)
            """)

            return cur.fetchone()


def sayi_formatla(sayi):
    return f"{sayi:,}".replace(",", ".")


# Sol menü
st.sidebar.title("Satış Tahmin Sistemi")

sayfa = st.sidebar.radio(
    "Menü",
    [
        "Genel Bakış",
        "Satış Tahminleri",
        "Model Karşılaştırması",
        "Mağaza Analizi",
        "Veritabanı Analizi"
    ]
)

st.sidebar.divider()



try:
    sifre = st.secrets["postgresql"]["password"]
except (FileNotFoundError, KeyError):
    st.error("Veritabanı bağlantı ayarları eksik.")
    st.stop()
st.sidebar.caption("PostgreSQL ve Makine Öğrenmesi")


# Genel Bakış
if sayfa == "Genel Bakış":

    st.markdown("""
    <div class="hero-box">
        <div class="hero-title">
            Mağaza Satış Tahmin Sistemi
        </div>
        <div class="hero-text">
            PostgreSQL ve makine öğrenmesi kullanılarak
            geliştirilen satış tahmin ve analiz sistemi.
        </div>
    </div>
    """, unsafe_allow_html=True)

    if not sifre:
        st.info("Bağlanmak için PostgreSQL şifrenizi giriniz.")
        st.stop()

    try:
        with st.spinner("Veriler PostgreSQL'den alınıyor..."):
            satis, magaza, urun = genel_ozet(sifre)

        st.sidebar.success("PostgreSQL bağlantısı başarılı")

    except psycopg2.Error:
        st.error(
            "Veritabanına bağlanılamadı. "
            "Şifrenizi ve sunucu durumunu kontrol ediniz."
        )
        st.stop()

    st.subheader("Genel Özet")

    col1, col2, col3, col4 = st.columns(4)

    col1.metric(
        "Satış Kaydı",
        sayi_formatla(satis),
        border=True
    )

    col2.metric(
        "Mağaza",
        sayi_formatla(magaza),
        border=True
    )

    col3.metric(
        "Ürün",
        sayi_formatla(urun),
        border=True
    )

    col4.metric(
        "Geliştirilen Model",
        "3",
        border=True
    )

    st.caption("Veri kaynağı: PostgreSQL — retail_ml_db")

    st.subheader("Proje İçeriği")

    sol, sag = st.columns(2)

    with sol:
        with st.container(border=True):
            st.markdown("### Projede Yapılanlar")
            st.markdown("""
- Ham verilerin PostgreSQL'e aktarılması
- SQL ile veri hazırlama
- Eğitim ve test veri setlerinin oluşturulması
- Makine öğrenmesi ile satış tahmini
- Tahminlerin PostgreSQL'e kaydedilmesi
            """)

    with sag:
        with st.container(border=True):
            st.markdown("### Kullanılan Modeller")
            st.markdown("""
- İlk Random Forest
- İyileştirilmiş Random Forest
- HistGradientBoosting

139 mağaza için 59 günlük satış tahmini.
            """)


elif sayfa == "Satış Tahminleri":
    from src.arayuz_tahminleri import satis_tahminleri
    satis_tahminleri(sifre)

elif sayfa == "Model Karşılaştırması":
    import pandas as pd

    st.title("Model Karşılaştırması")
    st.caption("Makine öğrenmesi modellerinin test sonuçları")

    veriler = pd.DataFrame({
        "Model": [
            "İlk Random Forest",
            "İyileştirilmiş Random Forest",
            "HistGradientBoosting"
        ],
        "MAE": [15.12, 14.77, 14.81],
        "RMSE": [32.54, 31.18, 30.75],
        "R²": [0.695, 0.720, 0.728]
    })

    st.dataframe(veriler, hide_index=True)

    st.subheader("MAE Karşılaştırması")

    st.bar_chart(
        veriler,
        x="Model",
        y="MAE",
        color="#60A5FA",
        horizontal=True
    )

    st.subheader("Değerlendirme")

    st.write(
        "İyileştirilmiş Random Forest en düşük MAE "
        "değerine sahiptir. HistGradientBoosting ise "
        "RMSE ve R² açısından daha başarılıdır."
    )

    st.caption(
        "Kaynak: Daha önce gerçekleştirilen model testleri."
    )

elif sayfa == "Mağaza Analizi":
    from src.arayuz_magaza import magaza_analizi
    magaza_analizi(sifre)

elif sayfa == "Veritabanı Analizi":
    from src.arayuz_veritabani import veritabani_analizi
    veritabani_analizi(sifre)