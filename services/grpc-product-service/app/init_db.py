from db.db import get_connection

def init_tables():
    with get_connection() as conn:
        with conn.cursor() as cur:
            # products テーブル
            cur.execute("""
            CREATE TABLE IF NOT EXISTS products (
                id TEXT PRIMARY KEY,
                name TEXT NOT NULL,
                price NUMERIC NOT NULL,
                description TEXT
            );
            """)

            # products にテストデータ追加
            cur.execute("""
                INSERT INTO products (id, name, price, description)
                VALUES 
                    ('p1', 'Product 1', 19.99, 'Sample product 1'),
                    ('p2', 'Product 2', 29.99, 'Sample product 2')
                ON CONFLICT (id) DO NOTHING;
            """)

        conn.commit()
        print("Tables created successfully.", flush=True)

if __name__ == "__main__":
    init_tables()
