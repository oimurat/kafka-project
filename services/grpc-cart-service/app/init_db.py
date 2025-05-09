# データベース接続関数をインポート
from db.db import get_connection

# テーブルを初期化する関数
def init_tables():
    # データベースに接続（with文で自動的にクローズされる）
    with get_connection() as conn:
        # SQLを実行するためのカーソルを作成
        with conn.cursor() as cur:
            # carts（カート）テーブルを作成
            # IF NOT EXISTS を使って、すでに存在する場合は作成しない
            cur.execute("""
            CREATE TABLE IF NOT EXISTS carts (
                id TEXT PRIMARY KEY,                         -- カートの一意なID（主キー）
                product_id TEXT NOT NULL REFERENCES products(id),  -- 商品ID（productsテーブルのidを参照）
                quantity INTEGER NOT NULL                    -- 商品の数量
            );
            """)

            # carts テーブルにテストデータを追加
            # ON CONFLICT (id) DO NOTHING により、すでに同じidのデータがある場合は無視される
            cur.execute("""
                INSERT INTO carts (id, product_id, quantity)
                VALUES 
                    ('c1', 'p1', 2),  -- 商品p1を2個入れたカートc1
                    ('c2', 'p2', 1)   -- 商品p2を1個入れたカートc2
                ON CONFLICT (id) DO NOTHING;
            """)

        # すべての変更をデータベースに保存（コミット）
        conn.commit()
        print("Tables created successfully.", flush=True)

# スクリプトが直接実行された場合、テーブル初期化関数を呼び出す
if __name__ == "__main__":
    init_tables()
