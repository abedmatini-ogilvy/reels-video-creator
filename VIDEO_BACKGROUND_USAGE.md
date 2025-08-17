# Video Background Creator - Usage Instructions

## How to use the video background script:

### 1. Upload your video file(s):
   - Put your video files (like `4434150-hd_1080_1920_30fps.mp4`) in the `videos/` folder
   - Supported formats: .mp4, .mov, .avi, .mkv

### 2. Run the script:
   ```bash
   # Activate virtual environment
   source video_env/bin/activate
   
   # Run the video background script
   python create_video_with_video_bg.py
   ```

### 3. Key differences from image version:
   - Uses `VideoFileClip` instead of `ImageClip`
   - Can handle original video audio
   - Option to mix original audio with background music
   - Automatically handles video duration
   - Supports video cropping/resizing

### 4. Customization options:

#### Duration:
- Change `final_duration = min(10, background_clip.duration)` to adjust length

#### Audio mixing:
- **Option 1**: Use only background music (current setting)
- **Option 2**: Mix original video audio with background music (uncomment the mixing code)

#### Text positioning:
- Change `with_position('center')` to:
  - `with_position(('center', 'top'))` - centered at top
  - `with_position(('center', 'bottom'))` - centered at bottom
  - `with_position((50, 100))` - specific pixel coordinates

#### Video effects:
- Add `.with_opacity(0.8)` to make background video semi-transparent
- Add `.with_speed_scaled(0.5)` to slow down the video
- Add `.cropped(x1=100, y1=100, x2=500, y2=400)` to crop video

### 5. Example with your video:
Once you upload `4434150-hd_1080_1920_30fps.mp4` to the `videos/` folder, 
the script will automatically use it as a background and create a video with:
- Your uploaded video as background
- Random motivational quote overlay
- Random background music
- 10-second duration (or original video length if shorter)

The output will be saved as: `motivational_video_with_video_bg.mp4`
