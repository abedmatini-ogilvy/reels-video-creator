import random
import textwrap
from moviepy import ImageClip, AudioFileClip, TextClip, CompositeVideoClip, ColorClip
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

print(f"Using image: {image_path}")
print(f"Using music: {music_path}")
print(f"Using proverb: {proverb}")

# Create video clip from image with higher resolution
image_clip = ImageClip(image_path).with_duration(10).resized(width=1080)  # Full HD

def create_enhanced_text(text, max_width=40):
    """Create multi-line text with enhanced styling"""
    # Break long text into multiple lines
    lines = textwrap.wrap(text, width=max_width)
    text_clips = []
    
    for i, line in enumerate(lines):
        line_clip = TextClip(text=line, 
                           color='white', 
                           font_size=45,  # Larger font size for HD
                           stroke_color='black', 
                           stroke_width=4)  # Thicker stroke for HD
        
        # Position each line with proper spacing
        if len(lines) == 1:
            y_position = 'center'
        else:
            # Calculate vertical positioning for multiple lines
            total_height = len(lines) * 60
            start_y = -total_height // 2 + 30
            y_position = ('center', start_y + i * 60)
        
        # Add positioning and duration
        line_clip = line_clip.with_position(y_position).with_duration(10)
        # Note: Fade effects removed for compatibility - can be added with proper imports
        
        text_clips.append(line_clip)
    
    return text_clips

def create_text_with_background(text_clips, bg_opacity=0.4):
    """Add semi-transparent background to text for better readability"""
    if not text_clips:
        return []
    
    # Calculate total text area
    total_width = max(clip.size[0] for clip in text_clips) + 80
    total_height = len(text_clips) * 60 + 40
    
    # Create background box
    txt_bg = ColorClip(size=(total_width, total_height), 
                      color=(0, 0, 0))  # Black background
    txt_bg = txt_bg.with_opacity(bg_opacity).with_duration(10)
    txt_bg = txt_bg.with_position('center')
    
    return [txt_bg] + text_clips

# Create enhanced text overlay
text_clips = create_enhanced_text(proverb)
text_with_bg = create_text_with_background(text_clips, bg_opacity=0.3)

# Add background music
audio_clip = AudioFileClip(music_path).subclipped(0, 10)
# Note: Audio fade effects removed for compatibility - can be added with proper imports

# Combine image + enhanced text
video = CompositeVideoClip([image_clip] + text_with_bg)
video = video.with_audio(audio_clip)

# Export final video with higher quality settings
output_path = "motivational_video_enhanced.mp4"
video.write_videofile(output_path, 
                     fps=30,  # Higher frame rate
                     codec='libx264', 
                     audio_codec='aac', 
                     bitrate="2000k")  # Higher bitrate for better quality

print(f"Enhanced video saved as {output_path}")

# Clean up resources
image_clip.close()
audio_clip.close()
video.close()
