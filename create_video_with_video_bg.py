import random
from moviepy import VideoFileClip, AudioFileClip, TextClip, CompositeVideoClip
import os

# Paths
videos_folder = "videos"  # Create this folder and put your video files here
music_folder = "music"
proverbs_file = "proverbs.txt"

# Pick random background video, music, and proverb
video_files = [f for f in os.listdir(videos_folder) if f.endswith(('.mp4', '.mov', '.avi', '.mkv'))]
if not video_files:
    print("No video files found in 'videos' folder!")
    exit(1)

background_video_path = os.path.join(videos_folder, random.choice(video_files))
music_path = os.path.join(music_folder, random.choice(os.listdir(music_folder)))

with open(proverbs_file, "r", encoding="utf-8") as f:
    proverbs = [line.strip() for line in f if line.strip()]
proverb = random.choice(proverbs)

print(f"Using background video: {background_video_path}")
print(f"Using music: {music_path}")
print(f"Using proverb: {proverb}")

# Load the background video
background_clip = VideoFileClip(background_video_path)

# Set duration (you can adjust this)
final_duration = min(10, background_clip.duration)  # Use 10 seconds or video length, whichever is shorter
background_clip = background_clip.subclipped(0, final_duration)

# Resize video if needed (optional - for consistent output size)
background_clip = background_clip.resized(width=640)

# Create text overlay with better visibility
txt_clip = TextClip(text=proverb, color='white', font_size=30, 
                   stroke_color='black', stroke_width=3)
txt_clip = txt_clip.with_position('center').with_duration(final_duration)

# Add background music
audio_clip = AudioFileClip(music_path).subclipped(0, final_duration)

# Combine background video + text
video = CompositeVideoClip([background_clip, txt_clip])

# Mix the original video audio with background music (optional)
# You can choose one of these options:

# Option 1: Use only background music (replace original audio)
video = video.with_audio(audio_clip)

# Option 2: Mix original video audio with background music (commented out)
# original_audio = background_clip.audio
# if original_audio:
#     mixed_audio = CompositeAudioClip([original_audio.with_volume_scaled(0.3), 
#                                      audio_clip.with_volume_scaled(0.7)])
#     video = video.with_audio(mixed_audio)
# else:
#     video = video.with_audio(audio_clip)

# Export final video
output_path = "motivational_video_with_video_bg.mp4"
video.write_videofile(output_path, fps=24, codec='libx264', audio_codec='aac', bitrate="1000k")

print(f"Video saved as {output_path}")

# Clean up
background_clip.close()
audio_clip.close()
video.close()
