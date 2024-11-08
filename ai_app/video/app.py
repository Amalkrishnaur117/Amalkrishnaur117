from flask import Flask, render_template, request, send_from_directory
import os

app = Flask(__name__)

def generate_video(topic, level, language):
    # Dummy video generation logic; replace with your actual implementation.
    video_filename = f"{topic}_{level}_{language}.mp4"
    # Create a fake video file for demonstration
    with open(os.path.join('static/videos', video_filename), 'w') as f:
        f.write("This is a dummy video content.")
    return video_filename

@app.route('/', methods=['GET', 'POST'])
def index():
    video_filename = None
    if request.method == 'POST':
        topic = request.form['topic']
        level = request.form['level']
        language = request.form['language']
        video_filename = generate_video(topic, level, language)
    return render_template('index.html', video_filename=video_filename)

@app.route('/videos/<path:filename>')
def uploaded_file(filename):
    return send_from_directory('static/videos', filename)

if __name__ == '__main__':
    if not os.path.exists('static/videos'):
        os.makedirs('static/videos')
    app.run(debug=True)
