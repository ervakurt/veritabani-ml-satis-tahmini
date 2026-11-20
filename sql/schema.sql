--
-- PostgreSQL database dump
--

\restrict jyL5gVFygq3EQkh60Zew5PkvCUGQ5jkE2Zaf44muie7XD64ZKhFgLWKWKaGGcx2

-- Dumped from database version 18.6
-- Dumped by pg_dump version 18.6

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET transaction_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- Name: donem_gecmis_ozet; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.donem_gecmis_ozet (
    baslangic_tarihi date,
    magaza_id character varying(20),
    gecmis_7_gun_ortalama numeric,
    gecmis_28_gun_ortalama numeric,
    gecmis_59_gun_ortalama numeric,
    gecmis_kayit_sayisi bigint
);


--
-- Name: donem_gecmis_temiz; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.donem_gecmis_temiz (
    baslangic_tarihi date,
    magaza_id character varying(20),
    gecmis_7_gun_ortalama numeric,
    gecmis_28_gun_ortalama numeric,
    gecmis_59_gun_ortalama numeric,
    gecmis_kayit_sayisi bigint
);


--
-- Name: gelecek_ml_egitim; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.gelecek_ml_egitim (
    magaza_id character varying(20),
    tarih date,
    gunluk_satis numeric,
    haftanin_gunu numeric,
    ay numeric,
    gecmis_7_gun_ortalama numeric,
    gecmis_28_gun_ortalama numeric,
    gecmis_59_gun_ortalama numeric
);


--
-- Name: gelecek_ml_temiz; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.gelecek_ml_temiz (
    magaza_id character varying(20),
    tarih date,
    gunluk_satis numeric,
    haftanin_gunu numeric,
    ay numeric,
    gecmis_7_gun_ortalama numeric,
    gecmis_28_gun_ortalama numeric,
    gecmis_59_gun_ortalama numeric
);


--
-- Name: gelecek_tahmin_verisi; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.gelecek_tahmin_verisi (
    magaza_id character varying(20),
    tahmin_tarihi date,
    tahmin_gunu integer,
    haftanin_gunu numeric,
    ay numeric,
    gecmis_7_gun_ortalama numeric,
    gecmis_28_gun_ortalama numeric,
    gecmis_59_gun_ortalama numeric
);


--
-- Name: magaza_gecmis_ozet; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.magaza_gecmis_ozet (
    magaza_id character varying(20),
    son_7_gun_ortalama numeric,
    son_28_gun_ortalama numeric,
    son_59_gun_ortalama numeric
);


--
-- Name: magaza_gunluk; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.magaza_gunluk (
    tarih date,
    magaza_id character varying(20),
    gunluk_satis numeric,
    ortalama_fiyat numeric,
    toplam_stok numeric,
    urun_sayisi bigint,
    promosyon1_sayisi bigint,
    promosyon2_sayisi bigint,
    magaza_tipi_id character varying(20),
    magaza_boyutu numeric,
    sehir_id character varying(20)
);


--
-- Name: ml_egitim; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.ml_egitim (
    tarih date,
    magaza_id character varying(20),
    gunluk_satis numeric,
    ortalama_fiyat numeric,
    toplam_stok numeric,
    urun_sayisi bigint,
    promosyon1_sayisi bigint,
    promosyon2_sayisi bigint,
    magaza_tipi_id character varying(20),
    magaza_boyutu numeric,
    sehir_id character varying(20),
    gecmis_1_gun numeric,
    gecmis_7_gun numeric,
    gecmis_14_gun numeric,
    gecmis_28_gun numeric,
    haftanin_gunu numeric,
    ay numeric
);


--
-- Name: ml_verisi; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.ml_verisi (
    tarih date,
    magaza_id character varying(20),
    gunluk_satis numeric,
    ortalama_fiyat numeric,
    toplam_stok numeric,
    urun_sayisi bigint,
    promosyon1_sayisi bigint,
    promosyon2_sayisi bigint,
    magaza_tipi_id character varying(20),
    magaza_boyutu numeric,
    sehir_id character varying(20),
    gecmis_1_gun numeric,
    gecmis_7_gun numeric,
    gecmis_14_gun numeric,
    gecmis_28_gun numeric,
    haftanin_gunu numeric,
    ay numeric
);


--
-- Name: products; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.products (
    product_id character varying(20) NOT NULL,
    product_length numeric,
    product_depth numeric,
    product_width numeric,
    cluster_id character varying(20),
    hierarchy1_id character varying(20),
    hierarchy2_id character varying(20),
    hierarchy3_id character varying(20),
    hierarchy4_id character varying(20),
    hierarchy5_id character varying(20)
);


--
-- Name: sales; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.sales (
    product_id character varying(20),
    store_id character varying(20),
    date date,
    sales numeric,
    revenue numeric,
    stock numeric,
    price numeric,
    promo_type_1 character varying(20),
    promo_bin_1 character varying(20),
    promo_type_2 character varying(20),
    promo_bin_2 character varying(20),
    promo_discount_2 numeric,
    promo_discount_type_2 character varying(20)
);


--
-- Name: satis_tahminleri; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.satis_tahminleri (
    magaza_id character varying(20) NOT NULL,
    tahmin_tarihi date NOT NULL,
    tahmin_gunu integer,
    tahmini_satis double precision
);


--
-- Name: satis_tahminleri_hist_gradient; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.satis_tahminleri_hist_gradient (
    magaza_id character varying(20) NOT NULL,
    tahmin_tarihi date NOT NULL,
    tahmin_gunu integer NOT NULL,
    tahmini_satis numeric(15,4) NOT NULL
);


--
-- Name: satis_tahminleri_rf_iyilestirilmis; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.satis_tahminleri_rf_iyilestirilmis (
    magaza_id character varying(20) NOT NULL,
    tahmin_tarihi date NOT NULL,
    tahmin_gunu integer NOT NULL,
    tahmini_satis numeric(15,4) NOT NULL
);


--
-- Name: stores; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.stores (
    store_id character varying(20) NOT NULL,
    storetype_id character varying(20),
    store_size numeric,
    city_id character varying(20)
);


--
-- Name: tahmin_donemleri; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.tahmin_donemleri (
    baslangic_tarihi date
);


--
-- Name: yeni_ml_egitim; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.yeni_ml_egitim (
    magaza_id character varying(20),
    baslangic_tarihi date,
    tahmin_tarihi date,
    tahmin_gunu integer,
    haftanin_gunu numeric,
    ay numeric,
    gecmis_7_gun_ortalama numeric,
    gecmis_28_gun_ortalama numeric,
    gecmis_59_gun_ortalama numeric,
    gercek_satis numeric
);


--
-- Name: yeni_ml_egitim_temiz; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.yeni_ml_egitim_temiz (
    magaza_id character varying(20),
    baslangic_tarihi date,
    tahmin_tarihi date,
    tahmin_gunu integer,
    haftanin_gunu numeric,
    ay numeric,
    gecmis_7_gun_ortalama numeric,
    gecmis_28_gun_ortalama numeric,
    gecmis_59_gun_ortalama numeric,
    gercek_satis numeric
);


--
-- Name: yeni_ml_test; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.yeni_ml_test (
    magaza_id character varying(20),
    baslangic_tarihi date,
    tahmin_tarihi date,
    tahmin_gunu integer,
    haftanin_gunu numeric,
    ay numeric,
    gecmis_7_gun_ortalama numeric,
    gecmis_28_gun_ortalama numeric,
    gecmis_59_gun_ortalama numeric,
    gercek_satis numeric
);


--
-- Name: products products_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.products
    ADD CONSTRAINT products_pkey PRIMARY KEY (product_id);


--
-- Name: satis_tahminleri_hist_gradient satis_tahminleri_hist_gradient_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.satis_tahminleri_hist_gradient
    ADD CONSTRAINT satis_tahminleri_hist_gradient_pkey PRIMARY KEY (magaza_id, tahmin_tarihi);


--
-- Name: satis_tahminleri satis_tahminleri_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.satis_tahminleri
    ADD CONSTRAINT satis_tahminleri_pkey PRIMARY KEY (magaza_id, tahmin_tarihi);


--
-- Name: satis_tahminleri_rf_iyilestirilmis satis_tahminleri_rf_iyilestirilmis_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.satis_tahminleri_rf_iyilestirilmis
    ADD CONSTRAINT satis_tahminleri_rf_iyilestirilmis_pkey PRIMARY KEY (magaza_id, tahmin_tarihi);


--
-- Name: stores stores_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.stores
    ADD CONSTRAINT stores_pkey PRIMARY KEY (store_id);


--
-- Name: idx_magaza_gunluk_magaza_tarih; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX idx_magaza_gunluk_magaza_tarih ON public.magaza_gunluk USING btree (magaza_id, tarih);


--
-- PostgreSQL database dump complete
--

\unrestrict jyL5gVFygq3EQkh60Zew5PkvCUGQ5jkE2Zaf44muie7XD64ZKhFgLWKWKaGGcx2

