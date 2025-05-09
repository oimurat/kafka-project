# gRPCで自動生成されたメッセージ・サービス定義をインポート
import product_pb2, product_pb2_grpc

# 商品取得・更新処理の関数をインポート（model.py）
from model import get_product_by_id, update_or_create_product

# 商品サービス（gRPCサービスの実装）
class ProductService(product_pb2_grpc.ProductServiceServicer):

    # 商品をIDで取得するメソッド
    def GetProduct(self, request, context):
        print(f"gRPC Request: id={request.id}, fields={request.fields}", flush=True)

        # DBから商品情報を取得
        data = get_product_by_id(request.id)
        print(f"get_product_by_id result: {data}", flush=True)

        # gRPCで返すためのレスポンスオブジェクトを作成
        product = product_pb2.Product()

        # クライアントがリクエストで指定したフィールドだけセットする
        for field in request.fields:
            if field in data:
                setattr(product, field, data[field])

        print(f"Returning Product: {product}", flush=True)

        # レスポンスとして返す
        return product_pb2.ProductResponse(product=product)

    # 商品を更新または新規作成するメソッド
    def UpdateProduct(self, request, context):
        print(f"gRPC Request: id={request.id}", flush=True)

        # リクエストから商品情報を取得
        product_id = request.id
        name = request.name
        price = request.price
        description = request.description

        # 商品の更新または新規作成処理（model.py内の関数）
        updated = update_or_create_product(product_id, name, price, description)
        print(f"Updating product {product_id}: {name}, {price}, {description}")

        # 処理が成功した場合、ステータス付きで返す
        if updated:
            return product_pb2.ProductResponse(
                product=product_pb2.Product(
                    id=product_id,
                    name=name,
                    price=price,
                    description=description
                )
            )
        else:
            # 失敗した場合はエラーメッセージを設定し、status=failed を返す
            context.set_details(f"Failed to update or create product with ID {product_id}.")
            return product_pb2.ProductResponse(status="failed")
