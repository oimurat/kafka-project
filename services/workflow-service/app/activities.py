# Temporal の Activity（業務処理）定義用ライブラリをインポート
from temporalio import activity

# gRPC の通信ライブラリと、各サービスの gRPC 定義ファイルをインポート
import grpc
import order_pb2, order_pb2_grpc
import payment_pb2, payment_pb2_grpc

# gRPC 経由で注文サービスに接続（ホスト名とポート番号指定）
order_channel = grpc.insecure_channel("grpc-order-service:50053")
order_stub = order_pb2_grpc.OrderServiceStub(order_channel)  # サービスクライアント作成

# gRPC 経由で決済サービスに接続
payment_channel = grpc.insecure_channel("grpc-payment-service:50054")
payment_stub = payment_pb2_grpc.PaymentServiceStub(payment_channel)

# ------------------------
# 商品注文の処理を行うアクティビティ
# ------------------------
@activity.defn
async def process_order(id: str, item_id: str):
    quantity = 1  # 数量は固定で1（本番では柔軟にすることも多い）
    
    # gRPC のリクエストメッセージを作成
    request = order_pb2.OrderRequest(id=id, item_id=item_id, quantity=quantity)

    # gRPC 経由で注文を送信（非同期ではないため、同期呼び出し）
    response = order_stub.PlaceOrder(request)

    # 結果をログ出力（デバッグ用）
    print(f"[Activity] Order placed: {response.message}", flush=True)

    # 処理結果のメッセージを返す（次の処理に使える）
    return response.message

# ------------------------
# 決済処理を行うアクティビティ
# ------------------------
@activity.defn
async def charge_payment(order_id: str):
    amount = 1000  # 金額は固定（例：テスト環境）。本番では柔軟に。
    
    # 決済リクエストを作成
    request = payment_pb2.PaymentRequest(order_id=order_id, amount=amount)

    # gRPC 経由で決済リクエストを送信
    response = payment_stub.PayOrder(request)

    print(f"[Activity] Payment charged: {response.message}", flush=True)

    return response.message

# ------------------------
# 注文キャンセル（返金）処理のアクティビティ
# ------------------------
@activity.defn
async def refund_order(id: str):
    # 返金リクエストを作成
    request = order_pb2.RefundRequest(id=id)

    # 注文サービスへ返金処理を依頼
    response = order_stub.RefundOrder(request)

    print(f"[Activity] Order refunded: {response.message}", flush=True)

    return response.message
