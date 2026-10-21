# Python ka official image use karein
FROM python:3.10-slim

# Working directory set karein
WORKDIR /app

# System dependencies install karein (FFmpeg video/audio merge ke liye zaroori hai)
RUN apt-get update && \
    apt-get install -y ffmpeg && \
    rm -rf /var/lib/apt/lists/*

# Python dependencies install karein
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Baaki saari files copy karein
COPY . .

# Port expose karein
EXPOSE 8080

# App ko Gunicorn ke zariye run karein
CMD ["gunicorn", "--bind", "0.0.0.0:8080", "app:app"]
