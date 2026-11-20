# PostgreSQL ve Makine Öğrenmesi ile Mağaza Satış Tahmini

## 1. Projenin Amacı

Bu projede PostgreSQL veritabanı ve makine öğrenmesi yöntemlerini kullanarak mağazaların gelecekteki satışlarını tahmin etmeyi amaçladım.

Satış verilerini PostgreSQL veritabanında sakladım. Python ile verileri işledim, makine öğrenmesi modelleri geliştirdim ve elde ettiğim tahminleri tekrar PostgreSQL'e kaydettim.

## 2. Kullanılan Teknolojiler

- Python
- PostgreSQL 18
- pandas ve NumPy
- scikit-learn
- Matplotlib
- psycopg2
- joblib
- Visual Studio Code
- pgAdmin 4

## 3. Veri Seti

Projede ürün, mağaza ve satış verileri kullandım.

Veriler PostgreSQL veritabanına aktarıldı. Daha sonra mağazaların geçmiş satış bilgileri kullanılarak makine öğrenmesi için eğitim ve test verileri hazırlandı.

## 4. Makine Öğrenmesi Modelleri

Projede üç farklı model üzerinde çalıştım:

1. İlk Random Forest
2. İyileştirilmiş Random Forest
3. HistGradientBoosting

Modelleri MAE, RMSE ve R² metrikleriyle değerlendirdim.

İyileştirilmiş Random Forest modelinde MAE 14,77, RMSE 31,18 ve R² 0,720 elde ettim.

HistGradientBoosting modelinde MAE 14,81, RMSE 30,75 ve R² 0,728 elde ettim.

Bu sonuçlar kullanılan test verisi üzerinde hesaplandı.

## 5. Gelecek Satış Tahminleri

Modellerle 139 mağaza için 59 günlük satış tahminleri oluşturdum.

Tahmin dönemi 1 Kasım 2019 ile 29 Aralık 2019 arasındadır.

| Model | Toplam Tahmini Satış |
|---|---:|
| İlk Random Forest | 465.375,62 |
| İyileştirilmiş Random Forest | 461.598,54 |
| HistGradientBoosting | 443.460,94 |

Her model 8.201 satış tahmini oluşturdu.

## 6. PostgreSQL Entegrasyonu

Makine öğrenmesi için kullanılan veriler PostgreSQL üzerinden okundu.

Modellerin oluşturduğu satış tahminleri CSV dosyalarına ve PostgreSQL tablolarına kaydedildi.

Model sonuçları SQL sorgularıyla karşılaştırıldı.

Veritabanının yapısı `sql/schema.sql` dosyasında bulunmaktadır.

## 7. Proje Klasörleri

- `data/`: Veri dosyaları
- `models/`: Eğitilmiş modeller
- `notebooks/`: Jupyter Notebook çalışmaları
- `reports/`: Grafikler ve analiz sonuçları
- `sql/`: Veritabanı şeması
- `src/`: Python kaynak kodları
- `requirements.txt`: Python bağımlılıkları

## 8. Kurulum

Python ve PostgreSQL kurulu olmalıdır.

Proje klasöründe sanal ortam oluşturulur:

```bash
python -m venv venv
```

Windows üzerinde sanal ortam etkinleştirilir:

```powershell
.\venv\Scripts\Activate.ps1
```

Gerekli Python kütüphaneleri yüklenir:

```bash
python -m pip install -r requirements.txt
```

PostgreSQL üzerinde `retail_ml_db` isimli veritabanı oluşturulur.

`sql/schema.sql` dosyası kullanılarak veritabanı yapısı hazırlanabilir.

**Not:** Şema dosyası satış verilerini içermez. Modelleri yeniden eğitmek veya tahminleri üretmek için gerekli verilerin ayrıca yüklenmesi gerekir.

## 9. Proje Sonuçları

Bu projede PostgreSQL ile makine öğrenmesi modellerini birlikte kullandım.

Üç farklı model geliştirdim ve sonuçlarını karşılaştırdım. Modellerin mağaza bazlı ve günlük satış tahminlerini analiz ettim.

Elde ettiğim sonuçları grafiklerle gösterdim ve PostgreSQL üzerinde sakladım.

Böylece veritabanı ve makine öğrenmesi entegrasyonunu uygulamalı olarak gerçekleştirdim.