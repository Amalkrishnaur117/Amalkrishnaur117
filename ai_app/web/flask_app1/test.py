import re
import json
import ollama
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
language = "english"
topic = "mqtt"
level = "beginers"
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
language is {language} topic is {topic} and level is {level}

  """,
  },
])
print(response['message']['content'])
json_data = extract_json_from_text(response['message']['content'])

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
def generate_image(text, points, file_name):
    try:
        img_width, img_height = 800, 600
        font = ImageFont.truetype('arial.ttf', 24)
        img = Image.new('RGB', (img_width, img_height), color=(73, 109, 137))
        d = ImageDraw.Draw(img)
        d.text((10, 10), text, font=font, fill=(255, 255, 0))
        for i, point in enumerate(points):
            d.text((10, 50 + i * 30), point, font=font, fill=(255, 255, 255))
        img.save(file_name)
    except Exception as e:
        print(f"Error generating image: {str(e)}")

# Generate audio from text
def generate_audio(text, file_name):
    try:
        audio = gTTS(text=text, lang='en')
        audio.save(file_name)
    except Exception as e:
        print(f"Error generating audio: {str(e)}")

# Generate video from image and audio
def generate_video(image_file, audio_file, video_file):
    try:
        audio_clip = AudioFileClip(audio_file)
        clip = ImageClip(image_file).set_duration(audio_clip.duration)
        clip = clip.set_audio(audio_clip)
        clip.write_videofile(video_file, fps=24)
    except Exception as e:
        print(f"Error generating video: {str(e)}")

# Concatenate videos
def concatenate_videos(video_files, output_file):
    try:
        clips = [VideoFileClip(file) for file in video_files]
        final_clip = concatenate_videoclips(clips)
        final_clip.write_videofile(output_file, fps=24)
    except Exception as e:
        print(f"Error concatenating videos: {str(e)}")

def main():
    json_data = load_json('data.json')
    if json_data is None:
        return

    video_files = []
    for i, scene in enumerate(json_data['scenes']):
        title = scene['title']
        points = scene['points']
        script = scene['script']

        image_file = f'scene_{i+1}.png'
        audio_file = f'scene_{i+1}.mp3'
        video_file = f'scene_{i+1}.mp4'

        generate_image(title, points, image_file)
        generate_audio(script, audio_file)
        generate_video(image_file, audio_file, video_file)

        video_files.append(video_file)

    concatenate_videos(video_files, 'final_video.mp4')

if __name__ == "__main__":
    main()
