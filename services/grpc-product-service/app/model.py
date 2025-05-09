# データベース接続用関数をインポート
from db.db import get_connection

# -----------------------------------------
# 商品情報をIDで取得する関数
# -----------------------------------------
def get_product_by_id(id: str) -> dict:
    # データベースに接続（with文で自動的にクローズされる）
    with get_connection() as conn:
        with conn.cursor() as cur:
            # 指定されたIDの商品を検索
            cur.execute("SELECT id, name, price, description FROM products WHERE id = %s", (id,))
            row = cur.fetchone()  # 結果を1行取得

            if row:
                # カラム名と値を結びつけて辞書型に変換して返す
                return dict(zip(['id', 'name', 'price', 'description'], row))
            return {}  # 商品が見つからなかった場合は空の辞書を返す

# -----------------------------------------
# 商品情報を更新 or 新規作成する関数
# -----------------------------------------
def update_or_create_product(id: str, name: str, price: float, description: str) -> bool:
    # データベースに接続
    with get_connection() as conn:
        with conn.cursor() as cur:
            # 商品がすでに存在するかチェック
            existing_product = get_product_by_id(id)

            if existing_product:
                # 存在する場合は更新処理
                cur.execute("""
                    UPDATE products
                    SET name = %s, price = %s, description = %s
                    WHERE id = %s
                """, (name, price, description, id))
                conn.commit()

                # 更新された行数が1以上なら成功
                return cur.rowcount > 0
            else:
                # 存在しない場合は新規挿入
                cur.execute("""
                    INSERT INTO products (id, name, price, description)
                    VALUES (%s, %s, %s, %s)
                """, (id, name, price, description))
                conn.commit()

                # 挿入された行数が1以上なら成功
                return cur.rowcount > 0
