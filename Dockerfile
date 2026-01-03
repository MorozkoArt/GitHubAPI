FROM python:3.13-slim

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PYTHONPATH=/app/src

RUN apt-get update && \
    apt-get install -y --no-install-recommends ca-certificates && \
    rm -rf /var/lib/apt/lists/*

COPY requirements.txt .

RUN pip install --upgrade pip setuptools wheel && \
    pip install --prefer-binary -r requirements.txt && \
    rm -rf /root/.cache/pip

COPY src/ ./src

CMD sh -c '\
    if [ "$RUN_MODE" = "train" ]; then \
        python src/ml/train.py; \
    else \
        python src/app/main.py; \
    fi'