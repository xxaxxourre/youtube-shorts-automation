from flask import Flask, render_template, jsonify
import sqlite3
from datetime import datetime, timedelta
from collections import defaultdict
from pathlib import Path

app = Flask(__name__)
DB_PATH = Path("data/generated_scripts.db")

def get_stats():
    if not DB_PATH.exists():
        return {}

    conn = sqlite3.connect(str(DB_PATH))
    c = conn.cursor()

    c.execute('SELECT channel, COUNT(*) FROM scripts GROUP BY channel')
    scripts_by_channel = dict(c.fetchall())

    c.execute('SELECT channel, COUNT(*) FROM videos GROUP BY channel')
    videos_by_channel = dict(c.fetchall())

    c.execute('SELECT channel, COUNT(*) FROM uploads GROUP BY channel')
    uploads_by_channel = dict(c.fetchall())

    c.execute('''SELECT channel, COUNT(*) FROM scripts
                 WHERE created_at > datetime('now', '-1 day')
                 GROUP BY channel''')
    scripts_24h = dict(c.fetchall())

    c.execute('''SELECT channel, COUNT(*) FROM uploads
                 WHERE uploaded_at > datetime('now', '-1 day')
                 GROUP BY channel''')
    uploads_24h = dict(c.fetchall())

    stats = {}
    all_channels = set(scripts_by_channel.keys()) | set(videos_by_channel.keys())

    for channel in all_channels:
        scripts_total = scripts_by_channel.get(channel, 0)
        videos_total = videos_by_channel.get(channel, 0)
        uploads_total = uploads_by_channel.get(channel, 0)

        stats[channel] = {
            "scripts_total": scripts_total,
            "videos_total": videos_total,
            "uploads_total": uploads_total,
            "scripts_24h": scripts_24h.get(channel, 0),
            "uploads_24h": uploads_24h.get(channel, 0),
            "completion_rate": round(uploads_total / max(scripts_total, 1) * 100, 1) if scripts_total > 0 else 0,
        }

    conn.close()
    return stats

def get_upload_history():
    if not DB_PATH.exists():
        return []

    conn = sqlite3.connect(str(DB_PATH))
    c = conn.cursor()

    c.execute('''SELECT channel, youtube_url, uploaded_at
                 FROM uploads
                 ORDER BY uploaded_at DESC
                 LIMIT 20''')
    uploads = c.fetchall()

    conn.close()
    return uploads

@app.route('/')
def index():
    return render_template('dashboard.html')

@app.route('/api/stats')
def api_stats():
    return jsonify(get_stats())

@app.route('/api/uploads')
def api_uploads():
    uploads = get_upload_history()
    return jsonify([{
        "channel": u[0],
        "url": u[1],
        "time": u[2]
    } for u in uploads])

@app.route('/api/health')
def health():
    return jsonify({"status": "ok", "timestamp": datetime.now().isoformat()})

if __name__ == '__main__':
    app.run(debug=True, port=5000, host='127.0.0.1')
