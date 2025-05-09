# HTTP通信を行うためのrequestsライブラリ（今は未使用だが今後の拡張に備えてインポート）
import requests

# 自動生成されたgRPC関連のモジュールをインポート
import payment_pb2, payment_pb2_grpc

# PaymentServiceの実装クラス（gRPCサービスの中身を書く場所）
class PaymentService(payment_pb2_grpc.PaymentServiceServicer):

    # gRPC経由で呼び出される決済処理メソッド
    def PayOrder(self, request, context):
        # リクエスト情報（注文IDと金額）をログ出力
        print(f"決済処理: Order ID={request.order_id}, Amount={request.amount}")

        # 現状はダミー実装（本当の決済処理はまだ書かれていない）
        # ここで外部決済APIを呼び出したり、DBに記録することもできる

        # レスポンスを返す（成功とみなす）
        return payment_pb2.PaymentResponse(
            success=True,                 # 成功フラグ
            message="決済が成功しました"  # メッセージ（クライアントに返す）
        )
