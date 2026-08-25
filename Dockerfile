FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

RUN apt-get update && apt-get install -y \
    gcc \
    libglib2.0-0 \
    libsm6 \
    libxext6 \
    libxrender-dev \
    libgomp1 \
    && rm -rf /var/lib/apt/lists/*

RUN pip install --upgrade pip && \
    pip install --no-cache-dir \
    google-genai \
    google-api-python-client \
    google-auth \
    google-auth-oauthlib \
    google-auth-httplib2 \
    opencv-python-headless \
    pillow \
    numpy \
    python-dotenv \
    keyboard

COPY . .

RUN mkdir -p imagens_iniciais resultados

CMD ["python", "main.py"]