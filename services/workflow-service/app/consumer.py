# 必要なライブラリをインポート
import asyncio  # 非同期処理を扱う標準ライブラリ
import aio_pika  # RabbitMQ と非同期通信するためのライブラリ
import json  # JSON データの変換用
from temporalio.client import Client  # Temporal のクライアントライブラリ
from workflow import OrderWorkflow  # 定義済みのワークフローをインポート

# メイン関数（非同期で実行される）
async def main():
    print("[Consumer] consumer.py started", flush=True)

    # RabbitMQ に接続（接続が切れても自動で再接続してくれる）
    connection = await aio_pika.connect_robust("amqp://user:pass@rabbitmq/")
    channel = await connection.channel()  # チャンネルを開く

    # "order.created" という名前のキューを取得（無ければ作成）
    queue = await channel.declare_queue("order.created", durable=True)

    # Temporal サーバーに接続（ワークフローを実行するため）
    client = await Client.connect("temporal:7233")

    print("[Consumer] Waiting for 'order.created' events...", flush=True)

    # キューからのメッセージを非同期で監視
    async with queue.iterator() as queue_iter:
        async for message in queue_iter:  # 新しいメッセージが来るたびに繰り返し
            async with message.process():  # メッセージの処理開始（ACK自動送信）

                # メッセージの本文を JSON として読み込む
                data = json.loads(message.body)
                print(f"[Consumer] Event received: {data}", flush=True)

                # メッセージから注文IDと商品IDを取り出す
                id = data["id"]
                item_id = data["item_id"]

                # ワークフローをすぐ開始せずに少し待つ（例：外部サービスの準備を待つなど）
                await asyncio.sleep(10)

                # Temporal ワークフローを起動（IDと商品IDを引数に渡す）
                await client.start_workflow(
                    OrderWorkflow.run,         # 実行するワークフロー関数
                    args=[id, item_id],        # ワークフローに渡す引数
                    id=f"order-{id}",          # 一意のワークフローID（重複防止）
                    task_queue="order-task-queue"  # ワークフローが処理されるタスクキュー名
                )

                print(f"[✓] Started workflow for {id}", flush=True)

# Pythonスクリプトとして直接実行された場合、main()を実行
if __name__ == "__main__":
    asyncio.run(main())
