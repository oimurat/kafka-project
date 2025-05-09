# 必要なライブラリをインポート
import asyncio
from temporalio.client import Client  # Temporal サーバーとの通信クライアント
from temporalio.worker import Worker  # Temporal Worker を定義するためのクラス
from workflow import OrderWorkflow  # 定義したワークフローをインポート
from activities import process_order, charge_payment, refund_order  # アクティビティ関数のインポート

# メイン関数（非同期）
async def main():
    # Temporal サーバーに接続（ワークフローやアクティビティを登録するため）
    client = await Client.connect("temporal:7233")

    # Worker を作成（ワークフローとアクティビティの実行者）
    worker = Worker(
        client,  # Temporal クライアント
        task_queue="order-task-queue",  # ワークフローからのタスクを受け取るキュー名（ワークフローと合わせる）
        workflows=[OrderWorkflow],  # この Worker が実行できるワークフローのリスト
        activities=[process_order, charge_payment, refund_order],  # 実行可能なアクティビティのリスト
    )

    # Worker を起動（無限ループでワークフロー/アクティビティの処理を待機）
    await worker.run()

# スクリプトとして実行された場合に main() を実行
if __name__ == "__main__":
    asyncio.run(main())
