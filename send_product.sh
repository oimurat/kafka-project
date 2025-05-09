#!/bin/bash

# --------------------------------------------
# 商品データをKafka経由で送信するスクリプト
# --------------------------------------------

curl -X POST http://localhost:8001/update_product/ \
  -H "Content-Type: application/json" \
  -d '{
        "id": "p3",
        "name": "サンプル商品",
        "price": 1234.56,
        "description": "これはサンプルの商品です"
      }'
