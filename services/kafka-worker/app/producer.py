# import asyncio
# import json
# import os
# from aiokafka import AIOKafkaProducer
# from random import randint
# import logging

# logging.basicConfig(level=logging.INFO)
# log = logging.getLogger(__name__)

# KAFKA_TOPIC = os.getenv("KAFKA_TOPIC", "product-updates")
# KAFKA_BOOTSTRAP_SERVERS = os.getenv("KAFKA_BOOTSTRAP_SERVERS", "kafka:9092")


# async def start_producer():
#     producer = AIOKafkaProducer(
#         bootstrap_servers=KAFKA_BOOTSTRAP_SERVERS
#     )
#     await producer.start()
#     try:
#         while True:
#             # ダミーデータ生成
#             msg_id = str(randint(1000, 9999))
#             data = {
#                 "type": "update_product",
#                 "payload": {
#                     "id": f"p-{msg_id}",
#                     "name": f"Test Product {msg_id}",
#                     "price": round(randint(1000, 5000) / 100, 2),
#                     "description": "Auto-generated product"
#                 }
#             }
#             value = json.dumps(data).encode("utf-8")
#             await producer.send_and_wait(KAFKA_TOPIC, value)
#             log.info(f"Sent message: {data}")
#             await asyncio.sleep(5)  # 5秒ごとに送信
#     except Exception as e:
#         log.error(f"❌ Error while producing: {e}")
#     finally:
#         await producer.stop()
