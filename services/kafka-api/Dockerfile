FROM python:3.11

WORKDIR /app

COPY services/kafka-api/app ./

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY shared /shared
RUN pip install -e /shared

CMD ["python", "main.py"]
