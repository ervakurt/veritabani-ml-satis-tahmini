# Kurulum ve Çalıştırma Rehberi

## 1. Sistem Gereksinimleri

- Python 3.13
- PostgreSQL 18
- Git
- pgAdmin 4 (isteğe bağlı)

## 2. Projeyi İndirme

```bash
git clone https://github.com/ervakurt/veritabani-ml-satis-tahmini.git
cd veritabani-ml-satis-tahmini
```

## 3. Python Ortamını Hazırlama

```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
```

## 4. PostgreSQL Kurulumu

PostgreSQL sunucusu başlatılır. Yeni kurulumda pgAdmin üzerinden boş bir veritabanı oluşturulur.

```sql
CREATE DATABASE retail_ml_db;
```

PowerShell üzerinden tablo yapıları oluşturulur:

```powershell
& "C:\Program Files\PostgreSQL\18\bin\psql.exe" -U postgres -d retail_ml_db -v ON_ERROR_STOP=1 -f sql/schema.sql
```

PostgreSQL farklı bir konuma kurulmuşsa psql.exe yolu değiştirilmelidir.

| Parametre | Değer |
|---|---|
| Host | localhost |
| Port | 5432 |
| Database | retail_ml_db |
| User | postgres |

Veritabanı şifresi gerekli olduğunda terminal üzerinden girilir.

## 5. Veri Dosyalarının Hazırlanması

Proje ana dizininde data klasörü oluşturulur.

Gerekli veri dosyaları:

- sales.csv
- product_hierarchy.csv
- store_cities.csv

Ham veriler PostgreSQL'e aktarılır:

```bash
python src/load_products.py
python src/load_stores.py
python src/load_sales.py
```

## 6. SQL ile Veri Hazırlama

Ham verilerin aktarılması tamamlandıktan sonra SQL dosyaları sırasıyla çalıştırılır.

```powershell
& "C:\Program Files\PostgreSQL\18\bin\psql.exe" -U postgres -d retail_ml_db -v ON_ERROR_STOP=1 -f sql/veri_hazirlama.sql

& "C:\Program Files\PostgreSQL\18\bin\psql.exe" -U postgres -d retail_ml_db -v ON_ERROR_STOP=1 -f sql/egitim_test_hazirlama.sql

& "C:\Program Files\PostgreSQL\18\bin\psql.exe" -U postgres -d retail_ml_db -v ON_ERROR_STOP=1 -f sql/gelecek_tahmin_hazirlama.sql
```

### SQL Dosyaları

| Dosya | Açıklama |
|---|---|
| schema.sql | Tablo ve indeks yapıları |
| veri_hazirlama.sql | Günlük mağaza satış verileri |
| egitim_test_hazirlama.sql | Eğitim ve test veri setleri |
| gelecek_tahmin_hazirlama.sql | 59 günlük tahmin veri seti |
| analiz_sorgulari.sql | Model ve mağaza karşılaştırmaları |
| performans_analizi.sql | İndeks performans ölçümleri |

### Veri Doğrulama Sonuçları

| Tablo | Kayıt Sayısı | Eşleşme |
|---|---:|---:|
| magaza_gunluk | 136150 | %100 |
| tahmin_donemleri | 123 | %100 |
| donem_gecmis_ozet | 16448 | %100 |
| donem_gecmis_temiz | 16076 | %100 |
| yeni_ml_egitim | 945746 | %100 |
| yeni_ml_egitim_temiz | 622454 | %100 |
| yeni_ml_test | 286304 | %100 |
| magaza_gecmis_ozet | 144 | %100 |
| gelecek_tahmin_verisi | 8201 | %100 |

Yeniden oluşturulan veri hazırlama sorguları mevcut tablolarla karşılaştırılmıştır. Dokuz tablonun tamamında farklı ve eksik kayıt sayısı sıfırdır.

## 7. Model Eğitimi

```bash
python src/gelecek_tahmin_modeli.py
python src/model_iyilestirme.py
python src/hist_gradient_modeli.py
```

Eğitilmiş modeller models klasörüne kaydedilir.

## 8. Satış Tahminlerinin Oluşturulması

```bash
python src/59_gunluk_tahmin.py
python src/iyilestirilmis_rf_59_gunluk_tahmin.py
python src/hist_gradient_59_gunluk_tahmin.py
```

139 mağaza için 59 günlük satış tahmini oluşturulur. Her model için toplam 8201 tahmin kaydı elde edilir.

Tahmin sonuçları reports/csv klasörüne kaydedilir.

## 9. Model Performanslarının Karşılaştırılması

```bash
python src/model_secimi.py
```

Modeller MAE, RMSE ve R² metrikleriyle karşılaştırılır.

## 10. Tahminlerin PostgreSQL'e Kaydedilmesi

```bash
python src/ilk_rf_veritabanina_kaydet.py
python src/rf_tahminlerini_veritabanina_kaydet.py
python src/hist_gradient_veritabanina_kaydet.py
```

Bu komutlar üç modelin tahminlerini PostgreSQL veritabanına kaydeder.

Üç modelin PostgreSQL kayıt işlemleri başarıyla test edilmiştir.

## 11. Grafiklerin Oluşturulması

```bash
python src/uc_model_tahmin_karsilastirma.py
python src/uc_model_tahmin_grafigi.py
python src/magaza_tahmin_grafigi.py
python src/coklu_magaza_analizi.py
```

Grafikler reports/grafikler klasöründe saklanır.

## 12. SQL Analizleri

Model ve mağaza karşılaştırmaları için:

```powershell
& "C:\Program Files\PostgreSQL\18\bin\psql.exe" -U postgres -d retail_ml_db -v ON_ERROR_STOP=1 -f sql/analiz_sorgulari.sql
```

Üç modelin eksiksiz karşılaştırılması için üç tahmin tablosunun da doldurulmuş olması gerekir.

Veritabanı performans analizi için:

```powershell
& "C:\Program Files\PostgreSQL\18\bin\psql.exe" -U postgres -d retail_ml_db -v ON_ERROR_STOP=1 -f sql/performans_analizi.sql
```

## 13. Veritabanı Performans Sonuçları

magaza_gunluk tablosunda magaza_id ve tarih sütunları üzerinde birleşik B-tree indeksi bulunmaktadır.

Performans ölçümleri EXPLAIN ANALYZE ve BUFFERS kullanılarak gerçekleştirilmiştir.

| Ölçüm | İndeksli | İndeks Kullanımı Kapalı |
|---|---:|---:|
| Birinci ölçüm | 0.194 ms | 285.761 ms |
| İkinci ölçüm | 0.196 ms | 259.638 ms |
| Üçüncü ölçüm | 0.201 ms | 236.247 ms |
| Ortalama | 0.197 ms | 260.549 ms |
| Bellek bloğu erişimi | 64 | 3310 |

Seçilen sorguda indeks kullanımıyla çalışma süresi yaklaşık %99.92 azalmıştır.

Ölçüm sırasında mevcut indeks silinmemiştir. İndeks kullanımı geçici olarak kapatılmış ve işlem sonunda ayarlar geri alınmıştır.

Sonuçlar kullanılan sorguya ve çalışma ortamına özeldir.

## 14. Önemli Notlar

- Ham veri ve eğitilmiş model dosyaları GitHub deposuna dahil edilmemiştir.
- Hazır tahmin sonuçları ve grafikler reports klasöründe bulunmaktadır.
- Veri hazırlama SQL sorguları yeniden oluşturulmuş ve kayıt bazında doğrulanmıştır.
- Veri hazırlama dosyaları boş hedef tablolar için tasarlanmıştır.
- Eski deneysel tabloların tamamı bu kurulum akışına dahil değildir.
- Docker kullanımı zorunlu değildir.
- Ayrı bir test veritabanında 19 tablo oluşturulmuş, 699 ürün, 144 mağaza ve 19.454.838 satış kaydı yüklenmiştir. Dokuz veri hazırlama tablosunun kayıt sayıları ve MD5 içerik özetleri asıl veritabanıyla eşleşmiştir. Model eğitimi sıfırdan tekrarlanmamıştır.

[Ana proje sayfasına dön](../README.md)