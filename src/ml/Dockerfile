FROM python:3.11-slim

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PYTHONPATH=/app/src:/app/src/ml:/app/src/common

RUN apt-get update && \
    apt-get install -y --no-install-recommends ca-certificates && \
    rm -rf /var/lib/apt/lists/*

COPY src/ml/requirements.txt .

RUN pip install --upgrade pip setuptools wheel && \
    pip install --prefer-binary -r requirements.txt && \
    rm -rf /root/.cache/pip

COPY src/ ./src/

CMD ["python", "src/ml/train.py"]