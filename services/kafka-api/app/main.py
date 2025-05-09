import asyncio
import json
import os
from typing import Dict

from fastapi import FastAPI
from aiokafka import AIOKafkaProducer
import logging
import uvicorn

# -----------------------------
# 設定
# -----------------------------
KAFKA_TOPIC = os.getenv("KAFKA_TOPIC", "product-updates")
KAFKA_BOOTSTRAP_SERVERS = os.getenv("KAFKA_BOOTSTRAP_SERVERS", "kafka:9092")

# ロガー設定
logging.basicConfig(
    format="%(asctime)s - %(levelname)s - %(message)s",
    level=logging.INFO
)
log = logging.getLogger(__name__)

# FastAPI アプリ初期化
app = FastAPI()

# グローバルProducer（起動時に作成・再利用）
producer: AIOKafkaProducer = None

# -----------------------------
# ライフサイクルイベント
# -----------------------------

@app.on_event("startup")
async def startup_event():
    global producer
    log.info("🚀 Kafka Producer starting...")
    producer = AIOKafkaProducer(
        bootstrap_servers=KAFKA_BOOTSTRAP_SERVERS
    )
    await producer.start()
    log.info("Kafka Producer started.")

@app.on_event("shutdown")
async def shutdown_event():
    global producer
    log.info("🛑 Kafka Producer shutting down...")
    await producer.stop()
    log.info("Kafka Producer stopped.")

# -----------------------------
# エンドポイント
# -----------------------------

@app.post("/update_product/")
async def update_product(product: Dict):
    """
    Kafkaに商品情報を送信するエンドポイント
    """
    global producer

    log.info(f"📤 Sending message to Kafka: {product}")

    try:
        message = {
            "type": "update_product",
            "payload": product
        }
        value_json = json.dumps(message).encode("utf-8")

        await producer.send_and_wait(KAFKA_TOPIC, value_json)

        log.info("Message sent to Kafka successfully.")
        return {"status": "success", "data": product}
    except Exception as e:
        log.error(f"❌ Failed to send message: {e}")
        return {"status": "error", "detail": str(e)}

# -----------------------------
# ローカル実行用
# -----------------------------
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8001)
