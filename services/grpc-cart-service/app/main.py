# 非同期処理に使う asyncio、サービス実装をまとめたモジュール service をインポート
import asyncio, service

# gRPC 関連のモジュールと、コード生成された cart_pb2_grpc をインポート
import grpc, cart_pb2_grpc

# gRPCサーバーを起動する非同期関数
async def serve():
    # 非同期対応の gRPC サーバーを作成
    server = grpc.aio.server()

    # CartService サービスをサーバーに登録
    # → service.CartService() は実装クラス（resolversと繋がってることが多い）
    cart_pb2_grpc.add_CartServiceServicer_to_server(service.CartService(), server)

    # サーバーをポート50051で待ち受け（[::] は全てのIPアドレスで受け入れ）
    server.add_insecure_port('[::]:50051')

    # サーバーを開始（非同期）
    await server.start()

    # サーバーが終了するまで待機（通常はずっと実行中）
    await server.wait_for_termination()

# このスクリプトが直接実行されたときだけ gRPC サーバーを起動する
if __name__ == "__main__":
    # 非同期関数 serve() を実行
    asyncio.run(serve())
