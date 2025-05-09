# 自動生成されたgRPCのメッセージクラスとサービスクラスをインポート
import order_pb2, order_pb2_grpc

# OrderService の実装（gRPCサービスの中身を定義）
class OrderService(order_pb2_grpc.OrderServiceServicer):

    # 注文を処理するメソッド（gRPCリクエストを受けて返す）
    def PlaceOrder(self, request, context):
        # リクエストの内容をログに出力（どの注文IDか確認）
        print(f"[OrderService] PlaceOrder requested: {request.id}", flush=True)

        # 成功レスポンスを返す（実際の注文処理はまだ未実装）
        return order_pb2.OrderResponse(
            success=True,                         # 成功フラグ
            message="注文が成功しました"         # メッセージ（日本語でもOK）
        )
    
    # 注文の返金処理をするメソッド
    def RefundOrder(self, request, context):
        # 返金対象の注文IDをログ出力
        print(f"[OrderService] RefundOrder requested: {request.id}", flush=True)

        # 成功レスポンスを返す（ここもロジックは未実装）
        return order_pb2.OrderResponse(
            success=True,
            message=f"注文 {request.id} の取消が完了しました"
        )
