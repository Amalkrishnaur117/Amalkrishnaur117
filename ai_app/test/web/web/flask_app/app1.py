from flask import Flask, render_template, request, redirect, url_for, flash, send_from_directory
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required
import os

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Change this to a random secret key for production
login_manager = LoginManager(app)
login_manager.login_view = 'login'

# User storage for demonstration (replace with database in production)
users = {}

class User(UserMixin):
    def __init__(self, username):
        self.username = username

    def get_id(self):
        return self.username  # Return the username as the unique identifier

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
        video_filename = generate_video(topic, level, language)
    return render_template('index.html', video_filename=video_filename)

@app.route('/videos/<filename>')
def uploaded_file(filename):
    return send_from_directory('static/videos', filename)

def generate_video(topic, level, language):
    video_filename = f"{topic}_{level}_{language}.mp4"
    with open(os.path.join('static/videos', video_filename), 'w') as f:
        f.write("This is a dummy video content.")
    return video_filename

if __name__ == '__main__':
    if not os.path.exists('static/videos'):
        os.makedirs('static/videos')
    app.run(debug=True)