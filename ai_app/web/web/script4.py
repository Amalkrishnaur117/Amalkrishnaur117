import os

# Define the folder structure
folders = [
    'flask_app',
    'flask_app/static',
    'flask_app/static/css',
    'flask_app/static/videos',
    'flask_app/templates'
]

# Define the content for each file
files = {
    'flask_app/app.py': """from flask import Flask, render_template, request, redirect, url_for, flash, send_from_directory
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
""",
    'flask_app/templates/login.html': """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Login</title>
    <link rel="stylesheet" href="https://stackpath.bootstrapcdn.com/bootstrap/4.5.2/css/bootstrap.min.css">
</head>
<body>
    <div class="container">
        <h1 class="mt-5">Login</h1>
        {% with messages = get_flashed_messages(with_categories=true) %}
            {% if messages %}
                {% for category, message in messages %}
                    <div class="alert alert-{{ category }}">{{ message }}</div>
                {% endfor %}
            {% endif %}
        {% endwith %}
        <form method="POST" class="mt-3">
            <div class="form-group">
                <label for="username">Username</label>
                <input type="text" class="form-control" id="username" name="username" required>
            </div>
            <div class="form-group">
                <label for="password">Password</label>
                <input type="password" class="form-control" id="password" name="password" required>
            </div>
            <button type="submit" class="btn btn-primary">Login</button>
            <p class="mt-3">Don't have an account? <a href="{{ url_for('signup') }}">Sign up</a></p>
        </form>
    </div>
</body>
</html>
""",
    'flask_app/templates/signup.html': """<!DOCTYPE html>
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
        {% with messages = get_flashed_messages(with_categories=true) %}
            {% if messages %}
                {% for category, message in messages %}
                    <div class="alert alert-{{ category }}">{{ message }}</div>
                {% endfor %}
            {% endif %}
        {% endwith %}
        <form method="POST" class="mt-3">
            <div class="form-group">
                <label for="username">Username</label>
                <input type="text" class="form-control" id="username" name="username" required>
            </div>
            <div class="form-group">
                <label for="password">Password</label>
                <input type="password" class="form-control" id="password" name="password" required>
            </div>
            <button type="submit" class="btn btn-primary">Sign Up</button>
            <p class="mt-3">Already have an account? <a href="{{ url_for('login') }}">Login</a></p>
        </form>
    </div>
</body>
</html>
""",
    'flask_app/templates/index.html': """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Video Generator</title>
    <link rel="stylesheet" href="https://stackpath.bootstrapcdn.com/bootstrap/4.5.2/css/bootstrap.min.css">
</head>
<body>
    <div class="container">
        <h1 class="mt-5">Video Generator</h1>
        <form method="POST" class="mt-3">
            <div class="form-group">
                <label for="topic">Topic</label>
                <input type="text" class="form-control" id="topic" name="topic" required>
            </div>
            <div class="form-group">
                <label>Level</label><br>
                <div>
                    <input type="radio" id="beginner" name="level" value="beginner" required>
                    <label for="beginner">Beginner</label>
                </div>
                <div>
                    <input type="radio" id="medium" name="level" value="medium">
                    <label for="medium">Medium</label>
                </div>
                <div>
                    <input type="radio" id="advanced" name="level" value="advanced">
                    <label for="advanced">Advanced</label>
                </div>
            </div>
            <div class="form-group">
                <label for="language">Language</label>
                <input type="text" class="form-control" id="language" name="language" required>
            </div>
            <button type="submit" class="btn btn-primary">Generate Video</button>
        </form>
        {% if video_filename %}
            <h3 class="mt-4">Generated Video:</h3>
            <video width="320" height="240" controls>
                <source src="{{ url_for('uploaded_file', filename=video_filename) }}" type="video/mp4">
                Your browser does not support the video tag.
            </video>
        {% endif %}
        <a href="{{ url_for('logout') }}" class="btn btn-danger mt-3">Logout</a>
    </div>
</body>
</html>
"""
}

# Create folders
for folder in folders:
    os.makedirs(folder, exist_ok=True)

# Create files and write content
for file_path, content in files.items():
    with open(file_path, 'w') as file:
        file.write(content.strip())

print("Folder structure and files created successfully.")
