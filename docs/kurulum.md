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

Sanal ortam oluşturulur:

```powershell
python -m venv venv
```

Windows PowerShell üzerinde etkinleştirilir:

```powershell
.\venv\Scripts\Activate.ps1
```

Gerekli kütüphaneler yüklenir:

```bash
python -m pip install -r requirements.txt
```

## 4. PostgreSQL Kurulumu

PostgreSQL sunucusu başlatılır ve aşağıdaki veritabanı oluşturulur:

```sql
CREATE DATABASE retail_ml_db;
```

Oluşturulan veritabanında `sql/schema.sql` dosyası çalıştırılır.

Bağlantı bilgileri:

| Parametre | Değer |
|---|---|
| Host | localhost |
| Port | 5432 |
| Database | retail_ml_db |
| User | postgres |

Veritabanı şifresi gerekli olduğunda terminal üzerinden girilir.

## 5. Veri Dosyalarının Hazırlanması

Proje ana dizininde `data/` klasörü oluşturulur.

Gerekli veri dosyaları:

- `sales.csv`
- `products.csv`
- `stores.csv`

Veriler PostgreSQL'e aktarılır:

```bash
python src/load_products.py
python src/load_stores.py
python src/load_sales.py
```

Model eğitiminden önce gerekli eğitim, test ve gelecek tahmin veri yapıları hazırlanmalıdır.

## 6. Model Eğitimi

```bash
python src/gelecek_tahmin_modeli.py
python src/model_iyilestirme.py
python src/hist_gradient_modeli.py
```

Eğitilmiş modeller `models/` klasörüne kaydedilir.

## 7. Satış Tahminlerinin Oluşturulması

```bash
python src/59_gunluk_tahmin.py
python src/iyilestirilmis_rf_59_gunluk_tahmin.py
python src/hist_gradient_59_gunluk_tahmin.py
```

Tahmin sonuçları `reports/csv/` klasörüne kaydedilir.

## 8. Model Performanslarının Karşılaştırılması

```bash
python src/model_secimi.py
```

Modeller MAE, RMSE ve R² metrikleriyle karşılaştırılır.

## 9. Tahminlerin PostgreSQL'e Kaydedilmesi

```bash
python src/rf_tahminlerini_veritabanina_kaydet.py
python src/hist_gradient_veritabanina_kaydet.py
```

## 10. Grafiklerin Oluşturulması

```bash
python src/uc_model_tahmin_karsilastirma.py
python src/uc_model_tahmin_grafigi.py
python src/magaza_tahmin_grafigi.py
python src/coklu_magaza_analizi.py
```

Grafikler `reports/grafikler/` klasöründe saklanır.

## 11. Önemli Notlar

- Ham veri dosyaları ve eğitilmiş model dosyaları GitHub deposuna dahil edilmemiştir.
- Hazır tahmin sonuçları ve grafikler `reports/` klasöründe bulunmaktadır.
- Model eğitimi ve tahmin işlemlerinden önce gerekli veritabanı yapıları hazırlanmalıdır.
- Docker kullanımı zorunlu değildir.
- Sıfırdan kurulum sürecinin tamamı henüz bağımsız bir ortamda doğrulanmamıştır.

[Ana proje sayfasına dön](../README.md)