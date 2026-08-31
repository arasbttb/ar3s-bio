import os
import sqlite3
import hashlib
import json
import uuid
from datetime import datetime
from flask import Flask, render_template, request, jsonify, session, send_from_directory, redirect, url_for
from flask_cors import CORS
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY', 'guns-lol-super-secret-key-change-this-2026')
CORS(app)

DB_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'portfolio.db')
UPLOAD_FOLDER = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'static', 'uploads')
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 50 * 1024 * 1024  # 50MB max upload

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'webp', 'svg', 'mp3', 'wav', 'ogg', 'mp4', 'webm'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def hash_password(password):
    """Hash password with SHA-256"""
    return hashlib.sha256(password.encode('utf-8')).hexdigest()

def get_db():
    """Get database connection"""
    conn = sqlite3.connect(DB_FILE)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    """Initialize database tables and default data"""
    conn = get_db()
    c = conn.cursor()

    # Admin users table
    c.execute('''CREATE TABLE IF NOT EXISTS admin_users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE NOT NULL,
        password TEXT NOT NULL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )''')

    # Profile table
    c.execute('''CREATE TABLE IF NOT EXISTS profile (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT NOT NULL DEFAULT 'aras',
        display_name TEXT NOT NULL DEFAULT 'Aras Bartu',
        bio TEXT NOT NULL DEFAULT 'Full-Stack Developer & Tech Enthusiast. Building aesthetic web experiences.',
        typing_texts TEXT NOT NULL DEFAULT '["Full-Stack Developer", "Ar3s", "UI/UX & Web Craftsman", "Cybersecurity & Code"]',
        location TEXT NOT NULL DEFAULT 'Istanbul, Turkey',
        occupation TEXT NOT NULL DEFAULT 'Developer',
        avatar_url TEXT NOT NULL DEFAULT 'https://images.unsplash.com/photo-1534528741775-53994a69daeb?w=500&auto=format&fit=crop&q=80',
        banner_url TEXT NOT NULL DEFAULT 'https://images.unsplash.com/photo-1618005182384-a83a8bd57fbe?w=1200&auto=format&fit=crop&q=80',
        discord_user_id TEXT DEFAULT '',
        custom_status TEXT DEFAULT 'Creating awesome projects 🚀',
        views INTEGER DEFAULT 0,
        updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )''')

    # Social links table
    c.execute('''CREATE TABLE IF NOT EXISTS social_links (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        platform TEXT NOT NULL,
        title TEXT NOT NULL,
        url TEXT NOT NULL,
        icon TEXT NOT NULL,
        color TEXT DEFAULT '#ffffff',
        sort_order INTEGER DEFAULT 0,
        clicks INTEGER DEFAULT 0
    )''')

    # Custom links / showcase projects table
    c.execute('''CREATE TABLE IF NOT EXISTS custom_links (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT NOT NULL,
        description TEXT DEFAULT '',
        url TEXT NOT NULL,
        icon TEXT DEFAULT 'fa-solid fa-arrow-up-right-from-square',
        badge_text TEXT DEFAULT '',
        badge_color TEXT DEFAULT '#8b5cf6',
        sort_order INTEGER DEFAULT 0,
        clicks INTEGER DEFAULT 0,
        is_visible INTEGER DEFAULT 1
    )''')

    # Badges table
    c.execute('''CREATE TABLE IF NOT EXISTS badges (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        icon TEXT NOT NULL,
        color TEXT NOT NULL DEFAULT '#8b5cf6',
        description TEXT DEFAULT '',
        sort_order INTEGER DEFAULT 0
    )''')

    # Theme settings table
    c.execute('''CREATE TABLE IF NOT EXISTS theme_settings (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        bg_type TEXT NOT NULL DEFAULT 'particles_stars',
        bg_url TEXT DEFAULT '',
        bg_blur INTEGER DEFAULT 0,
        bg_dim REAL DEFAULT 0.4,
        accent_color TEXT DEFAULT '#8b5cf6',
        glow_color TEXT DEFAULT '#a855f7',
        card_bg_color TEXT DEFAULT 'rgba(15, 15, 20, 0.75)',
        card_border_color TEXT DEFAULT 'rgba(255, 255, 255, 0.12)',
        card_blur INTEGER DEFAULT 20,
        card_radius INTEGER DEFAULT 24,
        font_family TEXT DEFAULT 'Outfit',
        cursor_effect TEXT DEFAULT 'guns_dot',
        click_effect TEXT DEFAULT 'sparkle',
        click_to_enter_enabled INTEGER DEFAULT 1,
        click_to_enter_text TEXT DEFAULT '[ click anywhere to enter ]',
        click_to_enter_subtext TEXT DEFAULT 'turn up your volume 🔊',
        custom_css TEXT DEFAULT ''
    )''')

    # Music settings table
    c.execute('''CREATE TABLE IF NOT EXISTS music_settings (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        enabled INTEGER DEFAULT 1,
        title TEXT DEFAULT 'Midnight City',
        artist TEXT DEFAULT 'M83',
        audio_url TEXT DEFAULT 'https://cdn.pixabay.com/download/audio/2022/05/27/audio_1808fbf07a.mp3?filename=lofi-study-112191.mp3',
        cover_url TEXT DEFAULT 'https://images.unsplash.com/photo-1511671782779-c97d3d27a1d4?w=200&auto=format&fit=crop&q=80',
        autoplay INTEGER DEFAULT 1,
        loop INTEGER DEFAULT 1,
        initial_volume REAL DEFAULT 0.5
    )''')

    # Analytics table
    c.execute('''CREATE TABLE IF NOT EXISTS analytics (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        event_type TEXT NOT NULL,
        target_id INTEGER,
        ip_hash TEXT,
        user_agent TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )''')

    conn.commit()

    # Seed default data if empty
    c.execute('SELECT COUNT(*) as count FROM profile')
    if c.fetchone()['count'] == 0:
        c.execute('''INSERT INTO profile (username, display_name, bio, typing_texts, location, occupation, avatar_url, banner_url, custom_status, views)
                     VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''',
                  ('aras', 'Aras Bartu', 'Full-Stack Developer & Tech Enthusiast. Building aesthetic web experiences.',
                   json.dumps(["Full-Stack Developer", "Ar3s", "UI/UX & Web Craftsman", "Cybersecurity & Code"]),
                   'Istanbul, Turkey', 'Full-Stack Developer',
                   'https://images.unsplash.com/photo-1535713875002-d1d0cf377fde?w=500&auto=format&fit=crop&q=80',
                   'https://images.unsplash.com/photo-1618005182384-a83a8bd57fbe?w=1200&auto=format&fit=crop&q=80',
                   'Building the future 🚀', 1337))

    c.execute('SELECT COUNT(*) as count FROM theme_settings')
    if c.fetchone()['count'] == 0:
        c.execute('''INSERT INTO theme_settings (bg_type, bg_url, bg_blur, bg_dim, accent_color, glow_color, card_bg_color, card_border_color, card_blur, card_radius, font_family, cursor_effect, click_effect, click_to_enter_enabled, click_to_enter_text, click_to_enter_subtext, custom_css)
                     VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''',
                  ('particles_stars', '', 0, 0.4, '#8b5cf6', '#a855f7', 'rgba(13, 13, 18, 0.75)', 'rgba(255, 255, 255, 0.12)', 20, 24, 'Outfit', 'guns_dot', 'sparkle', 1, '[ click anywhere to enter ]', 'turn up your volume 🔊', ''))

    c.execute('SELECT COUNT(*) as count FROM music_settings')
    if c.fetchone()['count'] == 0:
        c.execute('''INSERT INTO music_settings (enabled, title, artist, audio_url, cover_url, autoplay, loop, initial_volume)
                     VALUES (?, ?, ?, ?, ?, ?, ?, ?)''',
                  (1, 'Lofi Chill Vibes', 'Aesthetic Beats', 'https://cdn.pixabay.com/download/audio/2022/05/27/audio_1808fbf07a.mp3?filename=lofi-study-112191.mp3', 'https://images.unsplash.com/photo-1511671782779-c97d3d27a1d4?w=200&auto=format&fit=crop&q=80', 1, 1, 0.5))

    c.execute('SELECT COUNT(*) as count FROM badges')
    if c.fetchone()['count'] == 0:
        badges = [
            ('Verified', 'fa-solid fa-circle-check', '#3b82f6', 'Doğrulanmış Profil', 1),
            ('Developer', 'fa-solid fa-code', '#10b981', 'Yazılım Geliştirici', 2),
            ('VIP', 'fa-solid fa-crown', '#f59e0b', 'VIP Üye', 3),
            ('OG', 'fa-solid fa-fire', '#ec4899', 'Original Gangster', 4)
        ]
        c.executemany('INSERT INTO badges (name, icon, color, description, sort_order) VALUES (?, ?, ?, ?, ?)', badges)

    c.execute('SELECT COUNT(*) as count FROM social_links')
    if c.fetchone()['count'] == 0:
        socials = [
            ('discord', 'Discord', 'https://discord.com', 'fa-brands fa-discord', '#5865F2', 1),
            ('github', 'GitHub', 'https://github.com', 'fa-brands fa-github', '#ffffff', 2),
            ('spotify', 'Spotify', 'https://spotify.com', 'fa-brands fa-spotify', '#1DB954', 3),
            ('instagram', 'Instagram', 'https://instagram.com', 'fa-brands fa-instagram', '#E4405F', 4),
            ('x', 'X / Twitter', 'https://twitter.com', 'fa-brands fa-x-twitter', '#ffffff', 5),
            ('telegram', 'Telegram', 'https://telegram.org', 'fa-brands fa-telegram', '#24A1DE', 6),
            ('steam', 'Steam', 'https://steamcommunity.com', 'fa-brands fa-steam', '#66c0f4', 7)
        ]
        c.executemany('INSERT INTO social_links (platform, title, url, icon, color, sort_order) VALUES (?, ?, ?, ?, ?, ?)', socials)

    c.execute('SELECT COUNT(*) as count FROM custom_links')
    if c.fetchone()['count'] == 0:
        links = [
            ('🚀 GitHub Projelerim', 'Geliştirdiğim açık kaynaklı projeler ve repolar', 'https://github.com', 'fa-brands fa-github', 'HOT', '#ef4444', 1),
            ('🌐 Kişisel Web Sitem', 'Blog yazılarım, projelerim ve deneyimlerim', 'https://google.com', 'fa-solid fa-globe', 'WEB', '#3b82f6', 2),
            ('🎵 Spotify Çalma Listem', 'Kod yazarken dinlediğim favori parçalar', 'https://spotify.com', 'fa-brands fa-spotify', 'VIBE', '#10b981', 3),
            ('💬 İletişime Geç', 'Bana Telegram veya E-posta üzerinden ulaşın', 'mailto:contact@example.com', 'fa-solid fa-paper-plane', 'CONTACT', '#8b5cf6', 4)
        ]
        c.executemany('INSERT INTO custom_links (title, description, url, icon, badge_text, badge_color, sort_order) VALUES (?, ?, ?, ?, ?, ?, ?)', links)

    conn.commit()
    conn.close()

# Helper to get full site data
def get_site_data():
    conn = get_db()
    c = conn.cursor()

    c.execute('SELECT * FROM profile LIMIT 1')
    profile_row = c.fetchone()
    profile = dict(profile_row) if profile_row else {}
    if profile.get('typing_texts'):
        try:
            profile['typing_texts_list'] = json.loads(profile['typing_texts'])
        except Exception:
            profile['typing_texts_list'] = ["Developer"]
    else:
        profile['typing_texts_list'] = ["Developer"]

    c.execute('SELECT * FROM theme_settings LIMIT 1')
    theme_row = c.fetchone()
    theme = dict(theme_row) if theme_row else {}

    c.execute('SELECT * FROM music_settings LIMIT 1')
    music_row = c.fetchone()
    music = dict(music_row) if music_row else {}

    c.execute('SELECT * FROM badges ORDER BY sort_order ASC, id ASC')
    badges = [dict(r) for r in c.fetchall()]

    c.execute('SELECT * FROM social_links ORDER BY sort_order ASC, id ASC')
    socials = [dict(r) for r in c.fetchall()]

    c.execute('SELECT * FROM custom_links WHERE is_visible = 1 ORDER BY sort_order ASC, id ASC')
    links = [dict(r) for r in c.fetchall()]

    conn.close()

    return {
        'profile': profile,
        'theme': theme,
        'music': music,
        'badges': badges,
        'socials': socials,
        'links': links
    }

# Frontend Routes
@app.route('/')
def index():
    """Main Ar3s portfolio page"""
    conn = get_db()
    c = conn.cursor()
    # Increment views
    c.execute('UPDATE profile SET views = views + 1')
    conn.commit()
    conn.close()

    data = get_site_data()
    return render_template('index.html', **data)

@app.route('/login')
def login_page():
    if 'admin' in session:
        return redirect(url_for('admin_page'))
    return render_template('login.html')

@app.route('/admin')
def admin_page():
    if 'admin' not in session:
        return redirect(url_for('login_page'))
    return render_template('admin.html')

# API Routes for Site Data
@app.route('/api/data', methods=['GET'])
def api_data():
    return jsonify(get_site_data())

@app.route('/api/stats', methods=['GET'])
def api_stats():
    if 'admin' not in session:
        return jsonify({'error': 'Unauthorized'}), 401
    
    conn = get_db()
    c = conn.cursor()
    c.execute('SELECT views FROM profile LIMIT 1')
    row = c.fetchone()
    views = row['views'] if row else 0

    c.execute('SELECT SUM(clicks) as total_link_clicks FROM custom_links')
    row_links = c.fetchone()
    link_clicks = row_links['total_link_clicks'] if row_links and row_links['total_link_clicks'] else 0

    c.execute('SELECT SUM(clicks) as total_social_clicks FROM social_links')
    row_socials = c.fetchone()
    social_clicks = row_socials['total_social_clicks'] if row_socials and row_socials['total_social_clicks'] else 0

    c.execute('SELECT title, clicks, url FROM custom_links ORDER BY clicks DESC')
    top_links = [dict(r) for r in c.fetchall()]

    c.execute('SELECT platform, title, clicks FROM social_links ORDER BY clicks DESC')
    top_socials = [dict(r) for r in c.fetchall()]

    conn.close()

    return jsonify({
        'views': views,
        'total_link_clicks': link_clicks,
        'total_social_clicks': social_clicks,
        'top_links': top_links,
        'top_socials': top_socials
    })

# Click tracking
@app.route('/api/click/link/<int:link_id>', methods=['POST'])
def track_link_click(link_id):
    conn = get_db()
    c = conn.cursor()
    c.execute('UPDATE custom_links SET clicks = clicks + 1 WHERE id = ?', (link_id,))
    conn.commit()
    conn.close()
    return jsonify({'success': True})

@app.route('/api/click/social/<int:social_id>', methods=['POST'])
def track_social_click(social_id):
    conn = get_db()
    c = conn.cursor()
    c.execute('UPDATE social_links SET clicks = clicks + 1 WHERE id = ?', (social_id,))
    conn.commit()
    conn.close()
    return jsonify({'success': True})

# Admin Auth APIs
@app.route('/api/admin/login', methods=['POST'])
def admin_login():
    data = request.get_json() or {}
    username = data.get('username', '').strip()
    password = data.get('password', '').strip()

    conn = get_db()
    c = conn.cursor()
    c.execute('SELECT * FROM admin_users WHERE username = ?', (username,))
    user = c.fetchone()
    conn.close()

    if user and user['password'] == hash_password(password):
        session['admin'] = username
        return jsonify({'success': True, 'username': username})

    return jsonify({'error': 'Geçersiz kullanıcı adı veya şifre!'}), 401

@app.route('/api/admin/logout', methods=['POST'])
def admin_logout():
    session.pop('admin', None)
    return jsonify({'success': True})

@app.route('/api/admin/register', methods=['POST'])
def admin_register():
    conn = get_db()
    c = conn.cursor()
    c.execute('SELECT COUNT(*) as count FROM admin_users')
    user_count = c.fetchone()['count']

    # If admins already exist, registration requires being logged in as admin
    if user_count > 0 and 'admin' not in session:
        conn.close()
        return jsonify({'error': 'Yönetici hesabı zaten mevcut! Lütfen giriş yapın.'}), 403

    data = request.get_json() or {}
    username = data.get('username', '').strip()
    password = data.get('password', '').strip()

    if not username or not password:
        conn.close()
        return jsonify({'error': 'Kullanıcı adı ve şifre zorunludur!'}), 400

    try:
        c.execute('INSERT INTO admin_users (username, password) VALUES (?, ?)',
                  (username, hash_password(password)))
        conn.commit()
        conn.close()
        session['admin'] = username
        return jsonify({'success': True, 'username': username})
    except sqlite3.IntegrityError:
        conn.close()
        return jsonify({'error': 'Bu kullanıcı adı zaten alınmış!'}), 400

@app.route('/api/admin/status', methods=['GET'])
def admin_status():
    conn = get_db()
    c = conn.cursor()
    c.execute('SELECT COUNT(*) as count FROM admin_users')
    has_admin = c.fetchone()['count'] > 0
    conn.close()

    return jsonify({
        'is_logged_in': 'admin' in session,
        'admin_username': session.get('admin', ''),
        'has_admin': has_admin
    })

@app.route('/api/admin/change-password', methods=['POST'])
def change_password():
    if 'admin' not in session:
        return jsonify({'error': 'Unauthorized'}), 401

    data = request.get_json() or {}
    current_password = data.get('current_password', '')
    new_username = data.get('new_username', '').strip()
    new_password = data.get('new_password', '').strip()

    conn = get_db()
    c = conn.cursor()
    c.execute('SELECT * FROM admin_users WHERE username = ?', (session['admin'],))
    user = c.fetchone()

    if not user or user['password'] != hash_password(current_password):
        conn.close()
        return jsonify({'error': 'Mevcut şifre hatalı!'}), 400

    username_to_set = new_username if new_username else session['admin']
    if new_password:
        hashed_new_pwd = hash_password(new_password)
        c.execute('UPDATE admin_users SET username = ?, password = ? WHERE id = ?',
                  (username_to_set, hashed_new_pwd, user['id']))
    else:
        c.execute('UPDATE admin_users SET username = ? WHERE id = ?',
                  (username_to_set, user['id']))

    conn.commit()
    conn.close()
    session['admin'] = username_to_set

    return jsonify({'success': True, 'message': 'Hesap bilgileri başarıyla güncellendi!'})

# File Upload Endpoint
@app.route('/api/upload', methods=['POST'])
def upload_file():
    if 'admin' not in session:
        return jsonify({'error': 'Unauthorized'}), 401

    if 'file' not in request.files:
        return jsonify({'error': 'Dosya bulunamadı!'}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'Dosya seçilmedi!'}), 400

    if file and allowed_file(file.filename):
        ext = file.filename.rsplit('.', 1)[1].lower()
        unique_filename = f"{uuid.uuid4().hex}_{int(datetime.now().timestamp())}.{ext}"
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], unique_filename)
        file.save(filepath)
        file_url = f"/static/uploads/{unique_filename}"
        return jsonify({'success': True, 'url': file_url})

    return jsonify({'error': 'Desteklenmeyen dosya türü!'}), 400

# Profile API
@app.route('/api/profile', methods=['POST'])
def update_profile():
    if 'admin' not in session:
        return jsonify({'error': 'Unauthorized'}), 401

    data = request.get_json() or {}
    typing_texts = data.get('typing_texts', [])
    if isinstance(typing_texts, list):
        typing_texts_str = json.dumps(typing_texts)
    else:
        typing_texts_str = json.dumps([typing_texts])

    conn = get_db()
    c = conn.cursor()
    c.execute('''UPDATE profile SET 
                 username = ?, display_name = ?, bio = ?, typing_texts = ?, 
                 location = ?, occupation = ?, avatar_url = ?, banner_url = ?, 
                 discord_user_id = ?, custom_status = ?, updated_at = CURRENT_TIMESTAMP
                 WHERE id = (SELECT id FROM profile LIMIT 1)''',
              (data.get('username', 'aras'),
               data.get('display_name', 'Aras Bartu'),
               data.get('bio', ''),
               typing_texts_str,
               data.get('location', ''),
               data.get('occupation', ''),
               data.get('avatar_url', ''),
               data.get('banner_url', ''),
               data.get('discord_user_id', ''),
               data.get('custom_status', '')))
    conn.commit()
    conn.close()

    return jsonify({'success': True, 'message': 'Profil başarıyla güncellendi!'})

# Theme API
@app.route('/api/theme', methods=['POST'])
def update_theme():
    if 'admin' not in session:
        return jsonify({'error': 'Unauthorized'}), 401

    data = request.get_json() or {}
    conn = get_db()
    c = conn.cursor()
    c.execute('''UPDATE theme_settings SET 
                 bg_type = ?, bg_url = ?, bg_blur = ?, bg_dim = ?,
                 accent_color = ?, glow_color = ?, card_bg_color = ?, card_border_color = ?,
                 card_blur = ?, card_radius = ?, font_family = ?, cursor_effect = ?,
                 click_effect = ?, click_to_enter_enabled = ?, click_to_enter_text = ?,
                 click_to_enter_subtext = ?, custom_css = ?
                 WHERE id = (SELECT id FROM theme_settings LIMIT 1)''',
              (data.get('bg_type', 'particles_stars'),
               data.get('bg_url', ''),
               int(data.get('bg_blur', 0)),
               float(data.get('bg_dim', 0.4)),
               data.get('accent_color', '#8b5cf6'),
               data.get('glow_color', '#a855f7'),
               data.get('card_bg_color', 'rgba(15, 15, 20, 0.75)'),
               data.get('card_border_color', 'rgba(255, 255, 255, 0.12)'),
               int(data.get('card_blur', 20)),
               int(data.get('card_radius', 24)),
               data.get('font_family', 'Outfit'),
               data.get('cursor_effect', 'guns_dot'),
               data.get('click_effect', 'sparkle'),
               1 if data.get('click_to_enter_enabled', True) else 0,
               data.get('click_to_enter_text', '[ click anywhere to enter ]'),
               data.get('click_to_enter_subtext', 'turn up your volume 🔊'),
               data.get('custom_css', '')))
    conn.commit()
    conn.close()

    return jsonify({'success': True, 'message': 'Tema ayarları kaydedildi!'})

# Music API
@app.route('/api/music', methods=['POST'])
def update_music():
    if 'admin' not in session:
        return jsonify({'error': 'Unauthorized'}), 401

    data = request.get_json() or {}
    conn = get_db()
    c = conn.cursor()
    c.execute('''UPDATE music_settings SET 
                 enabled = ?, title = ?, artist = ?, audio_url = ?,
                 cover_url = ?, autoplay = ?, loop = ?, initial_volume = ?
                 WHERE id = (SELECT id FROM music_settings LIMIT 1)''',
              (1 if data.get('enabled', True) else 0,
               data.get('title', ''),
               data.get('artist', ''),
               data.get('audio_url', ''),
               data.get('cover_url', ''),
               1 if data.get('autoplay', True) else 0,
               1 if data.get('loop', True) else 0,
               float(data.get('initial_volume', 0.5))))
    conn.commit()
    conn.close()

    return jsonify({'success': True, 'message': 'Müzik ayarları kaydedildi!'})

# Social Links CRUD
@app.route('/api/socials', methods=['GET'])
def get_socials():
    conn = get_db()
    c = conn.cursor()
    c.execute('SELECT * FROM social_links ORDER BY sort_order ASC, id ASC')
    socials = [dict(r) for r in c.fetchall()]
    conn.close()
    return jsonify(socials)

@app.route('/api/socials', methods=['POST'])
def add_social():
    if 'admin' not in session:
        return jsonify({'error': 'Unauthorized'}), 401

    data = request.get_json() or {}
    platform = data.get('platform', 'custom')
    title = data.get('title', platform.capitalize())
    url = data.get('url', '').strip()
    icon = data.get('icon', 'fa-solid fa-link')
    color = data.get('color', '#ffffff')

    if not url:
        return jsonify({'error': 'Link URL zorunludur!'}), 400

    conn = get_db()
    c = conn.cursor()
    c.execute('SELECT COALESCE(MAX(sort_order), 0) + 1 as next_order FROM social_links')
    next_order = c.fetchone()['next_order']

    c.execute('''INSERT INTO social_links (platform, title, url, icon, color, sort_order)
                 VALUES (?, ?, ?, ?, ?, ?)''',
              (platform, title, url, icon, color, next_order))
    conn.commit()
    new_id = c.lastrowid
    conn.close()

    return jsonify({'success': True, 'id': new_id, 'message': 'Sosyal link eklendi!'})

@app.route('/api/socials/<int:social_id>', methods=['PUT'])
def edit_social(social_id):
    if 'admin' not in session:
        return jsonify({'error': 'Unauthorized'}), 401

    data = request.get_json() or {}
    conn = get_db()
    c = conn.cursor()
    c.execute('''UPDATE social_links SET 
                 platform = ?, title = ?, url = ?, icon = ?, color = ?
                 WHERE id = ?''',
              (data.get('platform', 'custom'),
               data.get('title', ''),
               data.get('url', ''),
               data.get('icon', 'fa-solid fa-link'),
               data.get('color', '#ffffff'),
               social_id))
    conn.commit()
    conn.close()

    return jsonify({'success': True, 'message': 'Sosyal link güncellendi!'})

@app.route('/api/socials/<int:social_id>', methods=['DELETE'])
def delete_social(social_id):
    if 'admin' not in session:
        return jsonify({'error': 'Unauthorized'}), 401

    conn = get_db()
    c = conn.cursor()
    c.execute('DELETE FROM social_links WHERE id = ?', (social_id,))
    conn.commit()
    conn.close()

    return jsonify({'success': True, 'message': 'Sosyal link silindi!'})

# Custom Links CRUD
@app.route('/api/links', methods=['GET'])
def get_links():
    conn = get_db()
    c = conn.cursor()
    c.execute('SELECT * FROM custom_links ORDER BY sort_order ASC, id ASC')
    links = [dict(r) for r in c.fetchall()]
    conn.close()
    return jsonify(links)

@app.route('/api/links', methods=['POST'])
def add_link():
    if 'admin' not in session:
        return jsonify({'error': 'Unauthorized'}), 401

    data = request.get_json() or {}
    title = data.get('title', '').strip()
    url = data.get('url', '').strip()

    if not title or not url:
        return jsonify({'error': 'Başlık ve URL zorunludur!'}), 400

    conn = get_db()
    c = conn.cursor()
    c.execute('SELECT COALESCE(MAX(sort_order), 0) + 1 as next_order FROM custom_links')
    next_order = c.fetchone()['next_order']

    c.execute('''INSERT INTO custom_links (title, description, url, icon, badge_text, badge_color, sort_order, is_visible)
                 VALUES (?, ?, ?, ?, ?, ?, ?, ?)''',
              (title,
               data.get('description', ''),
               url,
               data.get('icon', 'fa-solid fa-arrow-up-right-from-square'),
               data.get('badge_text', ''),
               data.get('badge_color', '#8b5cf6'),
               next_order,
               1 if data.get('is_visible', True) else 0))
    conn.commit()
    new_id = c.lastrowid
    conn.close()

    return jsonify({'success': True, 'id': new_id, 'message': 'Özel buton / proje eklendi!'})

@app.route('/api/links/<int:link_id>', methods=['PUT'])
def edit_link(link_id):
    if 'admin' not in session:
        return jsonify({'error': 'Unauthorized'}), 401

    data = request.get_json() or {}
    conn = get_db()
    c = conn.cursor()
    c.execute('''UPDATE custom_links SET 
                 title = ?, description = ?, url = ?, icon = ?, 
                 badge_text = ?, badge_color = ?, is_visible = ?
                 WHERE id = ?''',
              (data.get('title', ''),
               data.get('description', ''),
               data.get('url', ''),
               data.get('icon', 'fa-solid fa-arrow-up-right-from-square'),
               data.get('badge_text', ''),
               data.get('badge_color', '#8b5cf6'),
               1 if data.get('is_visible', True) else 0,
               link_id))
    conn.commit()
    conn.close()

    return jsonify({'success': True, 'message': 'Buton / proje güncellendi!'})

@app.route('/api/links/<int:link_id>', methods=['DELETE'])
def delete_link(link_id):
    if 'admin' not in session:
        return jsonify({'error': 'Unauthorized'}), 401

    conn = get_db()
    c = conn.cursor()
    c.execute('DELETE FROM custom_links WHERE id = ?', (link_id,))
    conn.commit()
    conn.close()

    return jsonify({'success': True, 'message': 'Buton / proje silindi!'})

# Badges CRUD
@app.route('/api/badges', methods=['GET'])
def get_badges():
    conn = get_db()
    c = conn.cursor()
    c.execute('SELECT * FROM badges ORDER BY sort_order ASC, id ASC')
    badges = [dict(r) for r in c.fetchall()]
    conn.close()
    return jsonify(badges)

@app.route('/api/badges', methods=['POST'])
def add_badge():
    if 'admin' not in session:
        return jsonify({'error': 'Unauthorized'}), 401

    data = request.get_json() or {}
    name = data.get('name', '').strip()
    icon = data.get('icon', 'fa-solid fa-certificate').strip()
    color = data.get('color', '#8b5cf6').strip()
    description = data.get('description', '').strip()

    if not name:
        return jsonify({'error': 'Rozet ismi zorunludur!'}), 400

    conn = get_db()
    c = conn.cursor()
    c.execute('SELECT COALESCE(MAX(sort_order), 0) + 1 as next_order FROM badges')
    next_order = c.fetchone()['next_order']

    c.execute('''INSERT INTO badges (name, icon, color, description, sort_order)
                 VALUES (?, ?, ?, ?, ?)''',
              (name, icon, color, description, next_order))
    conn.commit()
    new_id = c.lastrowid
    conn.close()

    return jsonify({'success': True, 'id': new_id, 'message': 'Rozet eklendi!'})

@app.route('/api/badges/<int:badge_id>', methods=['DELETE'])
def delete_badge(badge_id):
    if 'admin' not in session:
        return jsonify({'error': 'Unauthorized'}), 401

    conn = get_db()
    c = conn.cursor()
    c.execute('DELETE FROM badges WHERE id = ?', (badge_id,))
    conn.commit()
    conn.close()

    return jsonify({'success': True, 'message': 'Rozet silindi!'})

# Serve uploaded static files
@app.route('/static/uploads/<path:filename>')
def serve_upload(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

if __name__ == '__main__':
    init_db()
    print("=" * 60)
    print("🚀 Ar3s Portfolio & Bio Link Sitesi Başlatılıyor...")
    print("🌐 Ana Sayfa: http://127.0.0.1:5000")
    print("⚙️  Admin Paneli: http://127.0.0.1:5000/admin")
    print("=" * 60)
    app.run(debug=True, port=5000, host='0.0.0.0')
