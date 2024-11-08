import json
from PIL import Image, ImageDraw, ImageFont
from gtts import gTTS
from moviepy.editor import *
from pydub import AudioSegment
import os

# Load JSON data
def load_json(file_path):
    try:
        with open(file_path) as f:
            return json.load(f)
    except FileNotFoundError:
        print("JSON file not found.")
        return None
    except json.JSONDecodeError:
        print("Invalid JSON format.")
        return None

# Generate image from text
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