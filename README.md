# 🎬 Motivational Video Generator

A Python-based tool for creating motivational videos with customizable backgrounds, text overlays, and background music. Supports both image and video backgrounds.

## 📋 Features

- 🖼️ **Image Background Videos**: Create videos using static images as backgrounds
- 🎥 **Video Background Videos**: Use existing videos as animated backgrounds
- 📝 **Dynamic Text Overlays**: Automatically adds motivational quotes with enhanced visibility
- 🎵 **Background Music**: Randomly selects and adds background music
- 🎲 **Randomization**: Randomly picks images/videos, music, and quotes for variety
- ⚙️ **Optimized Output**: Configured for social media-friendly formats

## 🚀 Quick Start

### Prerequisites

- Python 3.12+
- FFmpeg (automatically installed during setup)

### Installation

1. **Clone or download this repository**

2. **Set up virtual environment and dependencies:**
   ```bash
   # Create virtual environment
   python3 -m venv video_env
   
   # Activate virtual environment
   source video_env/bin/activate
   
   # Install dependencies
   pip install moviepy
   ```

3. **Install FFmpeg (if not already installed):**
   ```bash
   sudo apt update && sudo apt install -y ffmpeg
   ```

### Project Structure

```
reels-video-creator/
├── create_video.py                    # Main script for image backgrounds
├── create_video_with_video_bg.py     # Script for video backgrounds
├── check_video_setup.py              # Video setup verification tool
├── proverbs.txt                       # Collection of motivational quotes
├── images/                            # Folder for background images
│   ├── christina-deravedisian-X9zaPw3fUAY-unsplash-min.jpg
│   ├── jan-valecka-6SMIS29eRSk-unsplash-min.jpg
│   └── lerone-pieters-vF6mSAWAzzU-unsplash-min.jpg
├── music/                             # Folder for background music
│   ├── instagram-reels-ads-background-music-292484.mp3
│   ├── instagram-reels-marketing-music-384448.mp3
│   └── marketing-instagram-reels-music-381070.mp3
├── videos/                            # Folder for background videos
│   └── 4434150-hd_1080_1920_30fps.mp4
└── video_env/                         # Virtual environment
```

## 🎯 Usage

### Image Background Videos

```bash
# Activate virtual environment
source video_env/bin/activate

# Create video with image background
python create_video.py
```

**Output:** `motivational_video.mp4`

### Video Background Videos

```bash
# Activate virtual environment
source video_env/bin/activate

# Check video setup (optional)
python check_video_setup.py

# Create video with video background
python create_video_with_video_bg.py
```

**Output:** `motivational_video_with_video_bg.mp4`

## 🔧 How the Code Works

### Image Background Script (`create_video.py`)

```python
# 1. Random Selection
image_path = os.path.join(images_folder, random.choice(os.listdir(images_folder)))
music_path = os.path.join(music_folder, random.choice(os.listdir(music_folder)))
proverb = random.choice(proverbs)

# 2. Create Image Clip
image_clip = ImageClip(image_path).with_duration(10).resized(width=640)

# 3. Create Text Overlay with Enhanced Visibility
txt_clip = TextClip(text=proverb, color='white', font_size=30, 
                   stroke_color='black', stroke_width=3)
txt_clip = txt_clip.with_position('center').with_duration(10)

# 4. Add Background Music
audio_clip = AudioFileClip(music_path).subclipped(0, 10)

# 5. Composite Video Creation
video = CompositeVideoClip([image_clip, txt_clip])
video = video.with_audio(audio_clip)

# 6. Export with Optimized Settings
video.write_videofile(output_path, fps=24, codec='libx264', audio_codec='aac', bitrate="1000k")
```

### Video Background Script (`create_video_with_video_bg.py`)

```python
# 1. Load Background Video
background_clip = VideoFileClip(background_video_path)
final_duration = min(10, background_clip.duration)
background_clip = background_clip.subclipped(0, final_duration).resized(width=640)

# 2. Create Text Overlay (same as image version)
txt_clip = TextClip(text=proverb, color='white', font_size=30, 
                   stroke_color='black', stroke_width=3)

# 3. Audio Processing
audio_clip = AudioFileClip(music_path).subclipped(0, final_duration)

# 4. Composite and Export
video = CompositeVideoClip([background_clip, txt_clip])
video = video.with_audio(audio_clip)  # Replaces original video audio
```

### Key Components Explained

1. **MoviePy Library**: Handles video/audio processing and composition
2. **Random Selection**: Ensures variety in content for each generation
3. **Text Enhancement**: Stroke outline ensures text visibility on any background
4. **Audio Management**: Clips music to match video duration
5. **Optimization**: Resizing and codec settings for social media compatibility

## 📁 Adding Your Own Content

### Images
- Add `.jpg`, `.png`, or `.jpeg` files to the `images/` folder
- Recommended resolution: 1080x1080 or higher
- Format: RGB color space

### Videos
- Add `.mp4`, `.mov`, `.avi`, or `.mkv` files to the `videos/` folder
- Any resolution supported (automatically resized)
- Duration: Any length (script uses first 10 seconds by default)

### Music
- Add `.mp3` files to the `music/` folder
- Duration: At least 10 seconds
- Recommended: Royalty-free tracks for commercial use

### Quotes
- Edit `proverbs.txt` file
- Add one quote per line
- Keep quotes concise for better readability

## 🔧 Customization Options

### Duration
```python
# Change video length (both scripts)
final_duration = 15  # 15 seconds instead of 10
```

### Text Styling
```python
# Modify text appearance
txt_clip = TextClip(text=proverb, 
                   color='yellow',           # Text color
                   font_size=40,             # Size
                   stroke_color='red',       # Outline color
                   stroke_width=2)           # Outline thickness
```

### Text Positioning
```python
# Different text positions
txt_clip.with_position('center')              # Center
txt_clip.with_position(('center', 'top'))     # Top center
txt_clip.with_position(('center', 'bottom'))  # Bottom center
txt_clip.with_position((50, 100))             # Specific coordinates
```

### Output Quality
```python
# Higher quality output
video.write_videofile(output_path, 
                     fps=30,                    # Higher frame rate
                     codec='libx264', 
                     audio_codec='aac', 
                     bitrate="2000k")           # Higher bitrate
```

## 🎨 Quality Improvement Suggestions

### For Image Backgrounds

1. **Higher Resolution Output**
   ```python
   image_clip = ImageClip(image_path).with_duration(10).resized(width=1080)  # Full HD
   ```

2. **Enhanced Text Effects**
   ```python
   # Add text shadow effect
   txt_clip = txt_clip.with_margin(20, color=(0,0,0), opacity=0.6)
   
   # Multiple text lines for long quotes
   lines = textwrap.wrap(proverb, width=40)
   ```

3. **Image Enhancement**
   ```python
   # Add subtle zoom effect
   image_clip = image_clip.resized(lambda t: 1 + 0.02*t)  # Slow zoom
   
   # Apply color filters
   image_clip = image_clip.with_fx(colorx, 1.2)  # Increase saturation
   ```

4. **Professional Transitions**
   ```python
   # Fade in/out effects
   txt_clip = txt_clip.with_fps(24).with_effects([fadein(1), fadeout(1)])
   ```

### For Video Backgrounds

1. **Audio Mixing Options**
   ```python
   # Mix original video audio with background music
   original_audio = background_clip.audio
   if original_audio:
       mixed_audio = CompositeAudioClip([
           original_audio.with_volume_scaled(0.3),    # Lower original volume
           audio_clip.with_volume_scaled(0.7)         # Higher music volume
       ])
       video = video.with_audio(mixed_audio)
   ```

2. **Video Effects**
   ```python
   # Slow motion effect
   background_clip = background_clip.with_speed_scaled(0.8)
   
   # Color grading
   background_clip = background_clip.with_fx(colorx, 0.8)  # Slightly desaturated
   ```

3. **Adaptive Text Positioning**
   ```python
   # Avoid text overlap with video content
   # Analyze video frames to find best text position
   txt_clip = txt_clip.with_position(('center', 0.8), relative=True)  # Bottom 20%
   ```

4. **Smart Duration Handling**
   ```python
   # Use full video length if under 15 seconds
   final_duration = min(15, background_clip.duration) if background_clip.duration < 15 else 10
   ```

## 🎵 Advanced Features to Implement

1. **Multiple Text Segments**: Break long quotes into multiple slides
2. **Music Synchronization**: Sync text appearance with music beats
3. **Logo/Watermark**: Add branding elements
4. **Batch Processing**: Generate multiple videos at once
5. **Template System**: Predefined styles for different moods
6. **Face Detection**: Ensure text doesn't cover faces in videos
7. **Color Palette Extraction**: Match text colors to image/video themes

## 🐛 Troubleshooting

### Common Issues

1. **"ModuleNotFoundError: No module named 'moviepy'"**
   ```bash
   source video_env/bin/activate
   pip install moviepy
   ```

2. **"OSError: [Errno 32] Broken pipe"**
   - Install FFmpeg: `sudo apt install ffmpeg`
   - Reduce video resolution or bitrate

3. **Text not visible**
   - Increase `stroke_width` parameter
   - Change text color or position

4. **Audio sync issues**
   - Ensure audio file is longer than video duration
   - Check audio format compatibility

## 📄 License

This project is for educational and personal use. Ensure you have proper licenses for any images, videos, or music files you use.

## 🤝 Contributing

Feel free to submit issues, fork the repository, and create pull requests for any improvements.

---

**Created by:** [Your Name]  
**Last Updated:** August 17, 2025
