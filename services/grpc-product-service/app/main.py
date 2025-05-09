# 非同期処理のための asyncio と、サービスの実装を含む service モジュールをインポート
import asyncio, service

# gRPCの基本機能と、product.proto から自動生成されたモジュールをインポート
import grpc, product_pb2_grpc

# gRPCサーバーを非同期で起動する関数
async def serve():
    # 非同期対応の gRPC サーバーを作成
    server = grpc.aio.server()

    # ProductService（商品情報を提供するサービス）の実装をサーバーに登録
    product_pb2_grpc.add_ProductServiceServicer_to_server(
        service.ProductService(),  # 実際の処理を担当するクラス
        server
    )

    # サーバーをすべてのIPアドレスに対してポート50052で待ち受け
    server.add_insecure_port('[::]:50052')

    # サーバーの起動
    await server.start()

    # サーバーが終了されるまで処理をブロック（待機）
    await server.wait_for_termination()

# スクリプトが直接実行された場合、gRPCサーバーを起動
if __name__ == "__main__":
    # 非同期関数 serve() をイベントループで実行
    asyncio.run(serve())
