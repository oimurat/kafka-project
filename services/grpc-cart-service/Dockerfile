FROM python:3.11

WORKDIR /app

COPY services/grpc-cart-service/app ./

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY shared /shared
RUN pip install -e /shared

RUN python -m grpc_tools.protoc \
    -I /shared/proto \
    --python_out=/app \
    --grpc_python_out=/app \
    /shared/proto/cart.proto

CMD ["python", "main.py"]
