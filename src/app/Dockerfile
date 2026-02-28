FROM python:3.13-slim

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PYTHONPATH=/app/src:/app/src/app:/app/src/common

RUN apt-get update && \
    apt-get install -y --no-install-recommends ca-certificates && \
    rm -rf /var/lib/apt/lists/*

COPY src/app/requirements.txt .

RUN pip install --upgrade pip setuptools wheel && \
    pip install --prefer-binary -r requirements.txt && \
    rm -rf /root/.cache/pip

COPY src/ ./src/

CMD ["python", "src/app/main.py"]