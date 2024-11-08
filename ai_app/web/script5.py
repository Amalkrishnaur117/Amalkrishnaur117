import os

def create_flask_structure():
    # Define the directory structure
    structure = {
        'flask_app1': {
            'app.py': """from flask import Flask, render_template, request, redirect, url_for, flash, send_from_directory
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required
import os
import json
from PIL import Image, ImageDraw, ImageFont
from gtts import gTTS
from moviepy.editor import *
from pydub import AudioSegment

app = Flask(__name__)
app.secret_key = 'your_secret_key'
login_manager = LoginManager(app)
login_manager.login_view = 'login'

users = {}

class User(UserMixin):
    def __init__(self, username):
        self.username = username

    def get_id(self):
        return self.username

@login_manager.user_loader
def load_user(username):
    return User(username) if username in users else None

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if username in users:
            flash('Username already exists', 'danger')
        else:
            users[username] = password
            flash('Signup successful! Please log in.', 'success')
            return redirect(url_for('login'))
    return render_template('signup.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if username in users and users[username] == password:
            user = User(username)
            login_user(user)
            return redirect(url_for('index'))
        else:
            flash('Invalid username or password', 'danger')
    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

@app.route('/', methods=['GET', 'POST'])
@login_required
def index():
    video_filename = None
    if request.method == 'POST':
        topic = request.form['topic']
        level = request.form['level']
        language = request.form['language']
        
        json_data = {
            "scenes": [
                {
                    "title": topic,
                    "points": [f"Point {i+1}" for i in range(3)],
                    "script": f"This is the script for {topic} at {level} level in {language}."
                }
            ]
        }
        
        video_filename = create_video(json_data)
        video_filename = os.path.basename(video_filename)
    return render_template('index.html', video_filename=video_filename)

@app.route('/videos/<filename>')
def uploaded_file(filename):
    return send_from_directory('static/videos', filename)

def create_video(json_data):
    video_files = []
    for i, scene in enumerate(json_data['scenes']):
        title = scene['title']
        points = scene['points']
        script = scene['script']

        image_file = f'static/videos/scene_{i+1}.png'
        audio_file = f'static/videos/scene_{i+1}.mp3'
        video_file = f'static/videos/scene_{i+1}.mp4'

        generate_image(title, points, image_file)
        generate_audio(script, audio_file)
        generate_video(image_file, audio_file, video_file)

        video_files.append(video_file)

    final_video_file = 'static/videos/final_video.mp4'
    concatenate_videos(video_files, final_video_file)
    return final_video_file

def generate_image(text, points, file_name):
    img_width, img_height = 800, 600
    font = ImageFont.truetype('arial.ttf', 24)
    img = Image.new('RGB', (img_width, img_height), color=(73, 109, 137))
    d = ImageDraw.Draw(img)
    d.text((10, 10), text, font=font, fill=(255, 255, 0))
    for i, point in enumerate(points):
        d.text((10, 50 + i * 30), point, font=font, fill=(255, 255, 255))
    img.save(file_name)

def generate_audio(text, file_name):
    audio = gTTS(text=text, lang='en')
    audio.save(file_name)

def generate_video(image_file, audio_file, video_file):
    audio_clip = AudioFileClip(audio_file)
    clip = ImageClip(image_file).set_duration(audio_clip.duration)
    clip = clip.set_audio(audio_clip)
    clip.write_videofile(video_file, fps=24)

def concatenate_videos(video_files, output_file):
    clips = [VideoFileClip(file) for file in video_files]
    final_clip = concatenate_videoclips(clips)
    final_clip.write_videofile(output_file, fps=24)

if __name__ == '__main__':
    if not os.path.exists('static/videos'):
        os.makedirs('static/videos')
    app.run(debug=True)
""",
            'templates': {
                'index.html': """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Video Generator</title>
    <link rel="stylesheet" href="https://stackpath.bootstrapcdn.com/bootstrap/4.5.2/css/bootstrap.min.css">
</head>
<body>
    <div class="container">
        <h1 class="mt-5">Generate Video</h1>
        <form method="post">
            <div class="form-group">
                <label for="topic">Topic</label>
                <input type="text" class="form-control" id="topic" name="topic" required>
            </div>
            <div class="form-group">
                <label for="level">Level</label>
                <div>
                    <label><input type="radio" name="level" value="beginner" required> Beginner</label>
                    <label><input type="radio" name="level" value="medium"> Medium</label>
                    <label><input type="radio" name="level" value="advanced"> Advanced</label>
                </div>
            </div>
            <div class="form-group">
                <label for="language">Language</label>
                <input type="text" class="form-control" id="language" name="language" required>
            </div>
            <button type="submit" class="btn btn-primary">Generate Video</button>
        </form>

        {% if video_filename %}
            <h2 class="mt-5">Generated Video</h2>
            <video width="800" controls>
                <source src="{{ url_for('uploaded_file', filename=video_filename) }}" type="video/mp4">
                Your browser does not support the video tag.
            </video>
        {% endif %}
    </div>
</body>
</html>
""",
                'signup.html': """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Sign Up</title>
    <link rel="stylesheet" href="https://stackpath.bootstrapcdn.com/bootstrap/4.5.2/css/bootstrap.min.css">
</head>
<body>
    <div class="container">
        <h1 class="mt-5">Sign Up</h1>
        <form method="post">
            <div class="form-group">
                <label for="username">Username</label>
                <input type="text" class="form-control" id="username" name="username" required>
            </div>
            <div class="form-group">
                <label for="password">Password</label>
                <input type="password" class="form-control" id="password" name="password" required>
            </div>
            <button type="submit" class="btn btn-primary">Sign Up</button>
        </form>
    </div>
</body>
</html>
""",
                'login.html': """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Login</title>
    <link rel="stylesheet" href="https://stackpath.bootstrapcdn.bootstrapcdn.com/bootstrap/4.5.2/css/bootstrap.min.css">
</head>
<body>
    <div class="container">
        <h1 class="mt-5">Login</h1>
        <form method="post">
            <div class="form-group">
                <label for="username">Username</label>
                <input type="text" class="form-control" id="username" name="username" required>
            </div>
            <div class="form-group">
                <label for="password">Password</label>
                <input type="password" class="form-control" id="password" name="password" required>
            </div>
            <button type="submit" class="btn btn-primary">Login</button>
        </form>
    </div>
</body>
</html>
"""
            },
            'static': {
                'videos': {}
            }
        }
    }

    # Create the directory structure
    for folder, subfolders in structure.items():
        folder_path = os.path.join(os.getcwd(), folder)
        os.makedirs(folder_path, exist_ok=True)
        if isinstance(subfolders, dict):
            for subfolder, file_content in subfolders.items():
                if isinstance(file_content, dict):
                    subfolder_path = os.path.join(folder_path, subfolder)
                    os.makedirs(subfolder_path, exist_ok=True)
                else:
                    with open(os.path.join(folder_path, subfolder), 'w') as f:
                        f.write(file_content)

if __name__ == "__main__":
    create_flask_structure()
