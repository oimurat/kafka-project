# Strawberry GraphQL, resolvers, osモジュールのインポート
import strawberry, resolvers, os
from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from strawberry.fastapi import GraphQLRouter
from strawberry.schema.config import StrawberryConfig

# アプリの構成図（簡易フロー）
# [1] schema.graphql       ← GraphQLのスキーマ定義（「何ができるか」を書く）
#  ↓
# [2] resolvers.py         ← 各操作に対する実際の処理内容（「何をするか」を書く）
#  ↓
# [3] grpc_clients/        ← gRPC経由で他マイクロサービスと通信するラッパー
#  ↓
# [4] gRPC Service         ← 実際のマイクロサービス（例：注文、支払いなど）

# GraphQLスキーマを定義
schema = strawberry.Schema(
    query=resolvers.Query,                   # クエリのエントリポイント（読み取り操作）
    mutation=resolvers.Mutation,             # ミューテーションのエントリポイント（書き込み操作）
    config=StrawberryConfig(auto_camel_case=False)  # フィールド名をスネークケースのまま使用
)

# GraphQLエンドポイントを FastAPI に統合するためのルーターを作成
graphql_app = GraphQLRouter(schema)

# FastAPIアプリケーションを作成
app = FastAPI()

# /graphql に GraphQL のルーターをマウント
app.include_router(graphql_app, prefix="/graphql")

# staticディレクトリ（HTMLやJSなどの静的ファイルを配置）をアプリにマウント
static_dir = os.path.join(os.path.dirname(__file__), "static")
app.mount("/static", StaticFiles(directory=static_dir), name="static")

# /ui エンドポイント：GraphQLのテストUI（例：GraphiQLなど）を表示するHTMLを返す
@app.get("/ui", response_class=HTMLResponse)
async def graphql_ui():
    # static/graphql_ui.html を読み込んで返す
    with open(os.path.join(static_dir, "graphql_ui.html")) as f:
        return f.read()
