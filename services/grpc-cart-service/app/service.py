# gRPCメッセージとサービス定義（自動生成されたファイル）をインポート
import cart_pb2, cart_pb2_grpc

# データベース操作用の関数をインポート（create_cart, get_cart_by_id）
from model import create_cart, get_cart_by_id

# CartService（gRPCサービスの実装クラス）
class CartService(cart_pb2_grpc.CartServiceServicer):

    # カート情報を取得する処理（GetCart RPC）
    def GetCart(self, request, context):
        # データベースから指定されたIDのカート情報を取得
        cart_data = get_cart_by_id(request.id)

        # 受け取ったリクエストのログ出力
        print(f"gRPC Request: id={request.id}, fields={request.fields}", flush=True)

        # Cart 型のレスポンスオブジェクトを作成（空の状態）
        cart = cart_pb2.Cart()

        # クライアントから要求されたフィールドだけをセットする
        for field in request.fields:
            if field in cart_data:
                setattr(cart, field, cart_data[field])  # 例：cart.id = cart_data["id"]

        # 返す内容のログを出力
        print(f"Returning Product: {cart}", flush=True)

        # レスポンスとして CartResponse を返す
        return cart_pb2.CartResponse(cart=cart)

    # カートを新規作成する処理（CreateCart RPC）
    def CreateCart(self, request, context):
        # リクエストのログを表示
        print(f"[CartService] create_cart: {request}")

        # モデル層の関数を使って、カートをデータベースに追加
        create_cart(
            id=request.id,
            product_id=request.product_id,
            quantity=request.quantity
        )

        # 成功メッセージを返す
        return cart_pb2.CreateCartResponse(
            message=f"Cart {request.id} created successfully."
        )
