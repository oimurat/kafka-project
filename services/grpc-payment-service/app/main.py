# 非同期処理用の asyncio モジュールと、サービス処理を実装した service モジュールをインポート
import asyncio, service

# gRPCライブラリと、自動生成された payment_pb2_grpc をインポート
import grpc, payment_pb2_grpc

# gRPCサーバーを起動する非同期関数
async def serve():
    # 非同期対応の gRPC サーバーを作成
    server = grpc.aio.server()

    # 実装された PaymentService をサーバーに登録
    payment_pb2_grpc.add_PaymentServiceServicer_to_server(service.PaymentService(), server)

    # サーバーをポート50054で起動（[::]は全IPアドレスに対応するIPv6形式）
    server.add_insecure_port("[::]:50054")

    # サーバーの起動
    await server.start()

    # サーバーが終了されるまで待機（通常は無限に待つ）
    await server.wait_for_termination()

# スクリプトが直接実行された場合に gRPC サーバーを起動する
if __name__ == "__main__":
    # 非同期関数 serve() を実行（asyncio イベントループで）
    asyncio.run(serve())
