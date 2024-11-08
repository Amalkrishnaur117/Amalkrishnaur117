from flask import Flask, render_template, request, redirect, url_for, flash, send_from_directory
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required
import os
import json
from PIL import Image, ImageDraw, ImageFont
from gtts import gTTS
from moviepy.editor import *
from pydub import AudioSegment
import ollama
import re
import json

def extract_json_from_text(text):
    # Regular expression to find JSON objects within text
    json_pattern = r"\{(?:[^{}]|(?R))*\}"
    
    # Search for JSON structure in the text
    json_match = re.search(json_pattern, text, re.DOTALL)
    
    if json_match:
        json_str = json_match.group()
        try:
            # Parse the JSON string
            parsed_json = json.loads(json_str)
            return parsed_json
        except json.JSONDecodeError:
            print("Found JSON-like text, but it's not valid JSON.")
            return None
    else:
        print("No JSON structure found in the text.")
        return None
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
        
        
        
        response = ollama.chat(model='llama3.2', messages=[
  {
    'role': 'user',
    'content': f"""Generate a JSON file for a presentation based on a given topic and specified learning level (beginner, medium, or advanced). Each JSON object should contain multiple scenes, with each scene structured as follows:

    id: A unique identifier for each scene, numbered sequentially.
    title: A concise title summarizing the main idea of the scene.
    points: A list of 2-4 essential points related to the topic.
    script: A single, detailed narration text tailored to the specified learning level.

For the script content:

    Include only the specified learning level’s content.
    Do not include language categories (e.g., "English").
    If a specific language is given, translate the script to that language; otherwise, default to English.
    Customize the content depth as follows:
        Beginner: Use simple language and provide clear explanations, assuming no prior knowledge.
        Medium: Include moderate detail, assuming basic familiarity with the topic.
        Advanced: Offer concise, technical content, assuming the audience has advanced understanding.
don't need to show level in script
language is {language} topic is {topic} and level is {level} i need only json file how to extract the json file

  """,
  },
])
        print(response['message']['content'])
        input_string = response['message']['content']
        json_string = re.search(r'\{.*\}', input_string, re.DOTALL).group(0)
        #json_data = json.load(response['message']['content'])
        print(json_string)
        with open("output.json", "w") as json_file:
            json_file.write(json_string)
        print(json_string)
        
#        json_data = json.load(response['message']['content'])

        f = open('data.json')

        # returns JSON object as a dictionary
        json_data = json.load(f)
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