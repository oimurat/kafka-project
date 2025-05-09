import asyncio
import os
import json
import logging
import grpc

from aiokafka import AIOKafkaConsumer

# gRPC モジュール（product.proto から生成されている想定）
import product_pb2
import product_pb2_grpc

# ロガー設定（見やすくログを表示）
logging.basicConfig(level=logging.INFO)
log = logging.getLogger("kafka-worker")

# 環境変数の読み込み（なければデフォルト値を使用）
KAFKA_TOPIC = os.getenv("KAFKA_TOPIC", "product-updates")
KAFKA_BOOTSTRAP_SERVERS = os.getenv("KAFKA_BOOTSTRAP_SERVERS", "kafka:9092")
KAFKA_CONSUMER_GROUP = os.getenv("KAFKA_CONSUMER_GROUP", "product-consumer-group")

# gRPC で ProductService に接続（ホスト名はサービス名に対応）
product_channel = grpc.insecure_channel("grpc-product-service:50052")
product_stub = product_pb2_grpc.ProductServiceStub(product_channel)

# 非同期Kafkaコンシューマー処理
async def consume():
    # Kafkaコンシューマー初期化（トピック、接続先、グループ指定）
    consumer = AIOKafkaConsumer(
        KAFKA_TOPIC,
        bootstrap_servers=KAFKA_BOOTSTRAP_SERVERS,
        group_id=KAFKA_CONSUMER_GROUP,
        enable_auto_commit=True
    )

    await consumer.start()

    log.info("Kafka consumer started.")

    try:
        # Kafka からメッセージを受信し続けるループ
        async for msg in consumer:
            await asyncio.sleep(10)

            log.info(f"📩 Consumed Kafka message: {msg.value}")

            try:
                value = json.loads(msg.value)
                # "type" を元にイベント種別をチェック
                if value.get("type") == "update_product":
                    payload = value.get("payload", {})
                    handle_product_update(payload)
                else:
                    log.warning(f"⚠️ Unknown message type: {value.get('type')}")

            except json.JSONDecodeError as e:
                log.error(f"❌ Failed to decode JSON: {e}")
    finally:
        # コンシューマーを停止（シャットダウン）
        await consumer.stop()
        log.info("🛑 Kafka consumer stopped.")

# Kafka メッセージから商品を更新する処理（gRPC呼び出し）
def handle_product_update(data: dict):
    try:
        # データを gRPC のリクエスト形式に変換
        request = product_pb2.UpdateProductRequest(
            id=data.get("id"),
            name=data.get("name"),
            price=data.get("price"),
            description=data.get("description")
        )

        # ProductService の gRPC メソッドを呼び出し
        response = product_stub.UpdateProduct(request)
        log.info(f"Product updated via gRPC: {response.product}")

    except grpc.RpcError as e:
        log.error(f"❌ gRPC call failed: {e.details()}")
