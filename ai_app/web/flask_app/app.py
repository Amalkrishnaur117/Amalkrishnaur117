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
        # Return just the filename to use in the template
        video_filename = os.path.basename(video_filename)
    return render_template('index.html', video_filename=video_filename)

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
