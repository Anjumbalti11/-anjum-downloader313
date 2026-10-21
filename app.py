from flask import Flask, request, jsonify
import yt_dlp
import os

app = Flask(__name__)

@app.route('/')
def home():
    return "Anjum Downloader API is Running!"

@app.route('/api/download')
def download_video():
    url = request.args.get('url')
    if not url:
        return jsonify({'error': 'YouTube URL required'}), 400

    # Agar cookies file mojood hai toh use karein
    cookie_file = 'cookies.txt'
    cookie_path = cookie_file if os.path.exists(cookie_file) else None

    ydl_opts = {
        'format': 'best',
        'quiet': True,
        'no_warnings': True,
        'extract_flat': False
    }

    if cookie_path:
        ydl_opts['cookiefile'] = cookie_path

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)
            
            # Direct video/audio link nikalein
            formats = info.get('formats', [])
            best_video = next((f for f in formats if f.get('ext') == 'mp4' and f.get('vcodec') != 'none'), None)
            best_audio = next((f for f in formats if f.get('ext') == 'm4a' or f.get('acodec') != 'none'), None)

            return jsonify({
                'success': True,
                'title': info.get('title'),
                'thumbnail': info.get('thumbnail'),
                'video_url': best_video['url'] if best_video else '',
                'audio_url': best_audio['url'] if best_audio else '',
                'duration': info.get('duration')
            })
            
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 8080)))