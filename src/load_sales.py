import os
import pandas as pd
import psycopg2
from io import StringIO
from getpass import getpass

CSV_FILE = "data/sales.csv"
CHUNK_SIZE = 50000

COLUMNS = [
    "product_id",
    "store_id",
    "date",
    "sales",
    "revenue",
    "stock",
    "price",
    "promo_type_1",
    "promo_bin_1",
    "promo_type_2",
    "promo_bin_2",
    "promo_discount_2",
    "promo_discount_type_2"
]

conn = psycopg2.connect(
    host="localhost",
    port=5432,
    database=os.getenv("PGDATABASE", "retail_ml_db"),
    user="postgres",
    password=os.getenv("PGPASSWORD") or getpass(
        "PostgreSQL sifresi: "
    )
)

try:
    total_rows = 0

    with conn.cursor() as cursor:
        cursor.execute(
            "LOCK TABLE sales IN SHARE ROW EXCLUSIVE MODE"
        )

        cursor.execute(
            "SELECT EXISTS (SELECT 1 FROM sales)"
        )

        if cursor.fetchone()[0]:
            raise RuntimeError(
                "Sales tablosu dolu. Aktarim iptal edildi."
            )

    for chunk_number, df in enumerate(
        pd.read_csv(CSV_FILE, chunksize=CHUNK_SIZE),
        start=1
    ):
        if set(df.columns) != set(COLUMNS):
            raise ValueError("CSV sutunlari uyumsuz.")

        df = df[COLUMNS]

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

        total_rows += len(df)

        print(
            f"Parca {chunk_number} islendi | "
            f"Bu parca: {len(df):,} | "
            f"Toplam: {total_rows:,}"
        )

    conn.commit()

    print(
        f"\nAktarim tamamlandi. "
        f"Toplam {total_rows:,} satis kaydi aktarildi."
    )

except Exception:
    conn.rollback()
    print("Aktarim iptal edildi. Degisiklikler geri alindi.")
    raise

finally:
    conn.close()