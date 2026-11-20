import pandas as pd
import psycopg2
from getpass import getpass
# CSV dosyasını oku
df = pd.read_csv("data/store_cities.csv")

# PostgreSQL bağlantısı
conn = psycopg2.connect(
    host="localhost",
    port=5432,
    database="retail_ml_db",
    user="postgres",
    password=getpass("PostgreSQL şifresi: ")
)

cursor = conn.cursor()

# Mağazaları aktar
for _, row in df.iterrows():
    cursor.execute(
        """
        INSERT INTO stores (
            store_id,
            storetype_id,
            store_size,
            city_id
        )
        VALUES (%s, %s, %s, %s)
        """,
        (
            row["store_id"],
            row["storetype_id"],
            row["store_size"],
            row["city_id"]
        )
    )

conn.commit()

cursor.close()
conn.close()

print(f"{len(df)} mağaza başarıyla PostgreSQL'e aktarıldı.")