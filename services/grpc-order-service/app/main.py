# 非同期処理のための asyncio と、Orderサービス実装を含む service モジュールをインポート
import asyncio, service

# gRPCの基本機能と、自動生成された order_pb2_grpc（gRPC定義）をインポート
import grpc, order_pb2_grpc

# gRPCサーバーを起動する非同期関数
async def serve():
    # 非同期対応の gRPC サーバーを作成
    server = grpc.aio.server()

    # OrderService の実装を gRPC サーバーに登録
    # service.OrderService() は実際の処理内容（注文処理など）を持ったクラス
    order_pb2_grpc.add_OrderServiceServicer_to_server(service.OrderService(), server)

    # サーバーをポート50053で起動（[::]は全てのIPアドレスで待ち受け）
    server.add_insecure_port("[::]:50053")

    # サーバーの起動
    await server.start()

    # サーバーが終了されるまで処理を待つ（通常はずっと実行され続ける）
    await server.wait_for_termination()

# スクリプトが直接実行されたときに gRPC サーバーを起動する
if __name__ == "__main__":
    # 非同期関数 serve() を実行（asyncio.runでイベントループを開始）
    asyncio.run(serve())
