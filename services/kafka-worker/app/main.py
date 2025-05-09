# 非同期処理に対応したKafkaコンシューマー関数をインポート
from consumer import consume
import asyncio

# スクリプトが直接実行された場合（他からimportされた時は実行されない）
if __name__ == "__main__":
    # 非同期関数 consume() を asyncio.run() で実行（イベントループを自動で作ってくれる）
    asyncio.run(consume())
