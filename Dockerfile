FROM python:3.10-slim

WORKDIR /app

# FFmpeg install karein (yt-dlp ke liye zaroori)
RUN apt-get update && apt-get install -y ffmpeg && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# App ko start karne ki command (Gunicorn use kar rahe hain)
CMD ["gunicorn", "--bind", "0.0.0.0:8080", "app:app"]