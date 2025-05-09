import strawberry, aio_pika, json
from strawberry.types import Info
from typing import Optional

# gRPCクライアントをインポート（外部サービスと通信するためのクライアント）
from grpc_clients import (
    grpc_cart,     # カート関連の操作を行うgRPCクライアント
    grpc_product,  # 商品関連の操作を行うgRPCクライアント
    grpc_order,    # 注文関連の操作を行うgRPCクライアント
    grpc_payment   # 支払い関連の操作を行うgRPCクライアント
)

# ========================================================
# RabbitMQ
# ========================================================
# 注文イベントをRabbitMQに送信する非同期関数
async def publish_order_event(id: str, item_id: str) -> str:
    # RabbitMQに接続
    connection = await aio_pika.connect_robust("amqp://user:pass@rabbitmq/")
    # チャンネルを作成
    channel = await connection.channel()

    # 送信するメッセージを構築（注文IDと商品ID）
    message = aio_pika.Message(
        body=json.dumps({
            "id": id,       # 注文ID
            "item_id": item_id  # 商品ID
        }).encode()  # JSONデータをエンコードして送信
    )

    # メッセージを "order.created" キューに送信
    await channel.default_exchange.publish(message, routing_key="order.created")
    # 接続を閉じる
    await connection.close()
    
    return f"Order event published for {id}"

# ========================================================
# 共通関数
# ========================================================
def build_dynamic_object(cls, source_obj, fields: list[str]):
    """
    任意の Strawberry 型 `cls` に対して、
    指定された fields のみを初期化してインスタンスを返す
    """
    init_args = {
        field: getattr(source_obj, field, None)
        for field in cls.__annotations__.keys()
    }

    # 未指定のフィールドは None にする（GraphQL の __init__ 要件を満たす）
    for key in init_args:
        if key not in fields:
            init_args[key] = None

    return cls(**init_args)

# ========================================================
# GraphQL
# ========================================================
# DTO定義：Product（商品情報を保持するためのデータ構造）
@strawberry.type
class Product:
    id: Optional[str]           # 商品ID（任意）
    name: Optional[str]         # 商品名（任意）
    price: Optional[float]      # 商品価格（任意）
    description: Optional[str]  # 商品説明（任意）

# DTO定義：Cart（カート情報を保持するためのデータ構造）
@strawberry.type
class Cart:
    id: Optional[str]           # カートID（任意）
    product_id: Optional[str]   # 商品ID（任意）
    quantity: Optional[int]     # 数量（任意）

# GraphQLのクエリを定義
@strawberry.type
class Query:
    # 商品情報を取得するクエリ
    @strawberry.field
    def product(self, info: Info, id: str) -> Product:
        top = info.selected_fields[0]  # クエリで選択されたフィールドを取得
        requested_fields = [f.name for f in top.selections]  # リクエストされたフィールド名をリスト化

        # リクエストされたフィールドをログに出力
        print(f"[GraphQL] リクエストフィールド: {requested_fields}", flush=True)

        # gRPCクライアントを使って商品情報を取得
        product = grpc_product.get_product_by_id(id, fields=requested_fields)

        # 取得した商品情報をレスポンスとして返す
        return build_dynamic_object(Product, product, requested_fields)

    # カート情報を取得するクエリ
    @strawberry.field
    def cart(self, info: Info, id: str) -> Cart:
        top = info.selected_fields[0]  # クエリで選択されたフィールドを取得
        requested_fields = [f.name for f in top.selections]  # リクエストされたフィールド名をリスト化

        # リクエストされたフィールドをログに出力
        print(f"[GraphQL] リクエストフィールド: {requested_fields}", flush=True)

        # gRPCクライアントを使ってカート情報を取得
        cart = grpc_cart.get_cart_by_id(id, fields=requested_fields)

        # 取得したカート情報をレスポンスとして返す
        return build_dynamic_object(Cart, cart, requested_fields)

# GraphQLのミューテーションを定義（データを変更する操作）
@strawberry.type
class Mutation:
    # カートを作成するミューテーション
    @strawberry.field
    def create_cart(self, id: str, product_id: str, quantity: int) -> str:
        return grpc_cart.create_cart(id=id, product_id=product_id, quantity=quantity)

    # 注文を出すミューテーション
    @strawberry.field
    def place_order(self, id: str, item_id: str, quantity: int) -> str:
        return grpc_order.place_order(id, item_id, quantity)

    # 注文を返金するミューテーション
    @strawberry.field
    def refund_order(self, order_id: str) -> str:
        return grpc_order.refund_order(order_id)

    # 注文に対する支払いを行うミューテーション
    @strawberry.field
    def pay_order(self, order_id: str, amount: int) -> str:
        return grpc_payment.pay_order(order_id, amount)

    # ワークフローで注文イベントを処理する非同期ミューテーション
    @strawberry.field
    async def workflow_order(self, order_id: str, item_id: str) -> str:
        # RabbitMQに注文イベントを送信
        return await publish_order_event(order_id, item_id)
