import sqlite3
import json
from datetime import datetime
from pathlib import Path

DB_PATH = Path("data/generated_scripts.db")
DB_PATH.parent.mkdir(parents=True, exist_ok=True)

def init_db():
    conn = sqlite3.connect(str(DB_PATH))
    c = conn.cursor()

    c.execute('''CREATE TABLE IF NOT EXISTS scripts
                 (id INTEGER PRIMARY KEY,
                  channel TEXT,
                  niche TEXT,
                  script TEXT,
                  title TEXT,
                  description TEXT,
                  tags TEXT,
                  created_at TIMESTAMP,
                  status TEXT)''')

    c.execute('''CREATE TABLE IF NOT EXISTS videos
                 (id INTEGER PRIMARY KEY,
                  channel TEXT,
                  script_id INTEGER,
                  video_path TEXT,
                  created_at TIMESTAMP,
                  status TEXT,
                  FOREIGN KEY(script_id) REFERENCES scripts(id))''')

    c.execute('''CREATE TABLE IF NOT EXISTS uploads
                 (id INTEGER PRIMARY KEY,
                  channel TEXT,
                  video_id INTEGER,
                  youtube_id TEXT,
                  youtube_url TEXT,
                  uploaded_at TIMESTAMP,
                  status TEXT,
                  FOREIGN KEY(video_id) REFERENCES videos(id))''')

    conn.commit()
    conn.close()

def add_script(channel, niche, script, title, description, tags):
    conn = sqlite3.connect(str(DB_PATH))
    c = conn.cursor()
    c.execute('''INSERT INTO scripts
                 (channel, niche, script, title, description, tags, created_at, status)
                 VALUES (?, ?, ?, ?, ?, ?, ?, ?)''',
              (channel, niche, script, title, description, json.dumps(tags),
               datetime.now().isoformat(), 'generated'))
    conn.commit()
    script_id = c.lastrowid
    conn.close()
    return script_id

def get_pending_scripts(channel, limit=5):
    conn = sqlite3.connect(str(DB_PATH))
    c = conn.cursor()
    c.execute('''SELECT id, script, title, description, tags
                 FROM scripts
                 WHERE channel=? AND status='generated'
                 ORDER BY created_at ASC
                 LIMIT ?''', (channel, limit))
    results = c.fetchall()
    conn.close()
    return results

def update_script_status(script_id, status):
    conn = sqlite3.connect(str(DB_PATH))
    c = conn.cursor()
    c.execute('UPDATE scripts SET status=? WHERE id=?', (status, script_id))
    conn.commit()
    conn.close()

def add_video(channel, script_id, video_path):
    conn = sqlite3.connect(str(DB_PATH))
    c = conn.cursor()
    c.execute('''INSERT INTO videos
                 (channel, script_id, video_path, created_at, status)
                 VALUES (?, ?, ?, ?, ?)''',
              (channel, script_id, video_path, datetime.now().isoformat(), 'created'))
    conn.commit()
    video_id = c.lastrowid
    conn.close()
    return video_id

def get_pending_videos(channel, limit=5):
    conn = sqlite3.connect(str(DB_PATH))
    c = conn.cursor()
    c.execute('''SELECT v.id, v.video_path, s.title, s.description, s.tags
                 FROM videos v
                 JOIN scripts s ON v.script_id = s.id
                 WHERE v.channel=? AND v.status='created'
                 ORDER BY v.created_at ASC
                 LIMIT ?''', (channel, limit))
    results = c.fetchall()
    conn.close()
    return results

def add_upload(channel, video_id, youtube_id, youtube_url):
    conn = sqlite3.connect(str(DB_PATH))
    c = conn.cursor()
    c.execute('''INSERT INTO uploads
                 (channel, video_id, youtube_id, youtube_url, uploaded_at, status)
                 VALUES (?, ?, ?, ?, ?, ?)''',
              (channel, video_id, youtube_id, youtube_url, datetime.now().isoformat(), 'uploaded'))
    conn.commit()
    conn.close()

def update_video_status(video_id, status):
    conn = sqlite3.connect(str(DB_PATH))
    c = conn.cursor()
    c.execute('UPDATE videos SET status=? WHERE id=?', (status, video_id))
    conn.commit()
    conn.close()
