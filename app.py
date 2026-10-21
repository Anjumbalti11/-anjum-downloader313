from flask import Flask, request, jsonify
from flask_cors import CORS
import yt_dlp
import os

app = Flask(__name__)
CORS(app)  # Yeh line InfinityFree se connect hone ke liye zaroori hai

@app.route('/')
def home():
    return "Anjum Downloader API is Running!"

@app.route('/api/download')
def download_video():
    url = request.args.get('url')
    if not url:
        return jsonify({'error': 'YouTube URL required'}), 400

    # Cookies path check karein
    cookie_path = '/app/cookies.txt' if os.path.exists('/app/cookies.txt') else 'cookies.txt'
    
    ydl_opts = {
        'format': 'best',
        'quiet': True,
        'no_warnings': True,
        'extract_flat': False,
        'cookiefile': cookie_path,
        'nocheckcertificate': True
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)
            formats = info.get('formats', [])
            
            # Best Video (MP4) nikalne ki koshish
            best_video = next((f for f in formats if f.get('ext') == 'mp4' and f.get('vcodec') != 'none'), None)
            # Best Audio (M4A/MP3) nikalne ki koshish
            best_audio = next((f for f in formats if f.get('acodec') != 'none' and f.get('vcodec') == 'none'), None)

            return jsonify({
                'success': True,
                'title': info.get('title'),
                'thumbnail': info.get('thumbnail'),
                'video_url': best_video['url'] if best_video else '',
                'audio_url': best_audio['url'] if best_audio else ''
            })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 8080)))
