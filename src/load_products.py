import os
import pandas as pd
import psycopg2
from getpass import getpass
# CSV dosyasını oku
df = pd.read_csv("data/product_hierarchy.csv")

# PostgreSQL bağlantısı
conn = psycopg2.connect(
    host="localhost",
    port=5432,
    database=os.getenv("PGDATABASE", "retail_ml_db"),
    user="postgres",
    password=os.getenv("PGPASSWORD") or getpass("PostgreSQL şifresi: ")
)

cursor = conn.cursor()

# Verileri PostgreSQL'e ekle
for _, row in df.iterrows():
    cursor.execute(
        """
        INSERT INTO products (
            product_id,
            product_length,
            product_depth,
            product_width,
            cluster_id,
            hierarchy1_id,
            hierarchy2_id,
            hierarchy3_id,
            hierarchy4_id,
            hierarchy5_id
        )
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        ON CONFLICT (product_id) DO NOTHING
        """,
        (
            row["product_id"],
            row["product_length"],
            row["product_depth"],
            row["product_width"],
            row["cluster_id"],
            row["hierarchy1_id"],
            row["hierarchy2_id"],
            row["hierarchy3_id"],
            row["hierarchy4_id"],
            row["hierarchy5_id"],
        )
    )

conn.commit()

cursor.close()
conn.close()

print(f"{len(df)} ürün başarıyla PostgreSQL'e aktarıldı.")
