import pandas as pd
import psycopg2
from io import StringIO
from getpass import getpass
CSV_FILE = "data/sales.csv"
CHUNK_SIZE = 50000

conn = psycopg2.connect(
    host="localhost",
    port=5432,
    database="retail_ml_db",
    user="postgres",
    password=getpass("PostgreSQL şifresi: ")
)

try:
    total_rows = 0

    for chunk_number, df in enumerate(
        pd.read_csv(CSV_FILE, chunksize=CHUNK_SIZE),
        start=1
    ):
        buffer = StringIO()

        df.to_csv(
            buffer,
            index=False,
            header=False,
            na_rep="\\N"
        )

        buffer.seek(0)

        with conn.cursor() as cursor:
            cursor.copy_expert(
                """
                COPY sales (
                    product_id,
                    store_id,
                    date,
                    sales,
                    revenue,
                    stock,
                    price,
                    promo_type_1,
                    promo_bin_1,
                    promo_type_2,
                    promo_bin_2,
                    promo_discount_2,
                    promo_discount_type_2
                )
                FROM STDIN
                WITH (
                    FORMAT CSV,
                    NULL '\\N'
                )
                """,
                buffer
            )

        conn.commit()

        total_rows += len(df)

        print(
            f"Parça {chunk_number} tamamlandı | "
            f"Bu parça: {len(df):,} | "
            f"Toplam: {total_rows:,}"
        )

finally:
    conn.close()

print(f"\nAktarım tamamlandı. Toplam {total_rows:,} satış kaydı aktarıldı.")