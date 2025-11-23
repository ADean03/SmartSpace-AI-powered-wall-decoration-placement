FROM python:3.8-slim

RUN apt-get update && apt-get install -y --no-install-recommends \
    git ffmpeg libsm6 libxext6 \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY src/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY src/ .

EXPOSE 7860
EXPOSE 8000

CMD ["python", "main.py"]
