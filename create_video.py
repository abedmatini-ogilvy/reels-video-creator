import random
from moviepy import ImageClip, AudioFileClip, TextClip, CompositeVideoClip
import os

# Paths
images_folder = "images"
music_folder = "music"
proverbs_file = "proverbs.txt"

# Pick random image, music, and proverb
image_path = os.path.join(images_folder, random.choice(os.listdir(images_folder)))
music_path = os.path.join(music_folder, random.choice(os.listdir(music_folder)))

with open(proverbs_file, "r", encoding="utf-8") as f:
	proverbs = [line.strip() for line in f if line.strip()]
proverb = random.choice(proverbs)

# Create video clip from image
image_clip = ImageClip(image_path).with_duration(10).resized(width=640)  # 10 seconds video, lower resolution

# Create text overlay
txt_clip = TextClip(text=proverb, color='white', font_size=30)
txt_clip = txt_clip.with_position('center').with_duration(10)

# Add background music
audio_clip = AudioFileClip(music_path).subclipped(0, 10)  # first 10 seconds of music

# Combine image + text
video = CompositeVideoClip([image_clip, txt_clip])
video = video.with_audio(audio_clip)

# Export final video
output_path = "motivational_video.mp4"
video.write_videofile(output_path, fps=24, codec='libx264', audio_codec='aac', bitrate="1000k")

print(f"Video saved as {output_path}")