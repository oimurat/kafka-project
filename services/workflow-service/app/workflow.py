# ワークフローに必要なライブラリをインポート
from datetime import timedelta
from temporalio import workflow
from temporalio.common import RetryPolicy

# 定義したアクティビティ関数をインポート
from activities import process_order, charge_payment, refund_order

# -----------------------------
# 注文処理を行うワークフローの定義
# -----------------------------
@workflow.defn
class OrderWorkflow:

    # ワークフローのメイン処理
    @workflow.run
    async def run(self, id: str, item_id: str):
        try:
            # =======================
            # 1. 注文アクティビティを実行
            # =======================
            await workflow.execute_activity(
                process_order,
                args=[id, item_id],  # アクティビティに渡す引数
                start_to_close_timeout=timedelta(seconds=30),  # アクティビティの実行時間の上限
                retry_policy=RetryPolicy(  # リトライポリシー設定
                    initial_interval=timedelta(seconds=2),  # 最初のリトライまでの待ち時間
                    maximum_attempts=1,  # 最大試行回数（1＝リトライしない）
                    backoff_coefficient=2.0  # リトライ間隔を指数的に増やす（今回は使われない）
                )
            )

            # =======================
            # 2. 決済アクティビティを実行
            # =======================
            await workflow.execute_activity(
                charge_payment,
                args=[id],
                start_to_close_timeout=timedelta(seconds=30),
                retry_policy=RetryPolicy(
                    initial_interval=timedelta(seconds=2),
                    maximum_attempts=1,
                    backoff_coefficient=2.0
                )
            )

        except Exception as e:
            # =======================
            # エラーが発生したら返金処理を実行
            # =======================
            await workflow.execute_activity(
                refund_order,
                args=[id],
                start_to_close_timeout=timedelta(seconds=30),
                retry_policy=RetryPolicy(
                    initial_interval=timedelta(seconds=2),
                    maximum_attempts=1,
                    backoff_coefficient=2.0
                )
            )
            # エラーを再送出してワークフローを失敗させる（エラーの原因を上位に伝える）
            raise e
