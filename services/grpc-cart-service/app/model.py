# データベース接続用の関数をインポート
from db.db import get_connection

# カートを新しく作成する関数
def create_cart(id: str, product_id: str, quantity: int):
    # データベースに接続（with文で自動的にクローズされる）
    with get_connection() as conn:
        # SQL実行のためのカーソルを取得
        with conn.cursor() as cur:
            # cartsテーブルに新しいレコードを追加
            # %s を使うことでSQLインジェクションを防ぐ（プレースホルダー）
            cur.execute("""
                INSERT INTO carts (id, product_id, quantity)
                VALUES (%s, %s, %s)
                ON CONFLICT (id) DO NOTHING;  -- 同じIDが既にある場合は挿入しない
            """, (id, product_id, quantity))
        # 変更を保存（コミット）
        conn.commit()

# カートIDでカート情報を取得する関数
def get_cart_by_id(id: str) -> dict:
    # データベースに接続
    with get_connection() as conn:
        with conn.cursor() as cur:
            # 指定されたIDのカート情報を取得
            cur.execute("""
                SELECT id, product_id, quantity FROM carts WHERE id = %s
            """, (id,))
            row = cur.fetchone()  # 結果を1件だけ取得
            if row:
                # 結果があれば辞書型で返す（キーと値を結びつける）
                return dict(zip(['id', 'product_id', 'quantity'], row))
            # 該当するカートがなければ空の辞書を返す
            return {}
