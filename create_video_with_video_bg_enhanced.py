import random
import textwrap
from moviepy import VideoFileClip, AudioFileClip, TextClip, CompositeVideoClip, ColorClip, CompositeAudioClip
import os

# Paths
videos_folder = "videos"
music_folder = "music"
proverbs_file = "proverbs.txt"

# Pick random background video, music, and proverb
video_files = [f for f in os.listdir(videos_folder) if f.endswith(('.mp4', '.mov', '.avi', '.mkv'))]
if not video_files:
    print("No video files found in 'videos' folder!")
    exit(1)

background_video_path = os.path.join(videos_folder, random.choice(video_files))

# Use different music files for variety (skip the first one used in image version)
music_files = [f for f in os.listdir(music_folder) if f.endswith('.mp3')]
if len(music_files) > 1:
    # Use a different music file than the image version typically uses
    preferred_music = [f for f in music_files if 'marketing' not in f.lower()]
    music_path = os.path.join(music_folder, random.choice(preferred_music if preferred_music else music_files))
else:
    music_path = os.path.join(music_folder, random.choice(music_files))

with open(proverbs_file, "r", encoding="utf-8") as f:
    proverbs = [line.strip() for line in f if line.strip()]

# Use a different proverb selection strategy for variety
if len(proverbs) > 1:
    # Prefer longer, more impactful quotes for video backgrounds
    longer_proverbs = [p for p in proverbs if len(p) > 20]
    proverb = random.choice(longer_proverbs if longer_proverbs else proverbs)
else:
    proverb = random.choice(proverbs)

print(f"Using background video: {background_video_path}")
print(f"Using music: {music_path}")
print(f"Using proverb: {proverb}")

# Load the background video with enhanced settings
background_clip = VideoFileClip(background_video_path)

# Enhanced duration handling - use more of the video if it's good quality
final_duration = min(15, background_clip.duration)  # Up to 15 seconds instead of 10
background_clip = background_clip.subclipped(0, final_duration)

# Smart resizing for better quality - maintain aspect ratio
def smart_resize_video(clip, target_width=1080):
    """Resize video while maintaining aspect ratio and ensuring good quality"""
    original_width, original_height = clip.size
    
    # Calculate new dimensions maintaining aspect ratio
    if original_width > target_width:
        # Only downscale if original is larger
        scale_factor = target_width / original_width
        new_height = int(original_height * scale_factor)
        return clip.resized(width=target_width, height=new_height)
    else:
        # Keep original size if it's already smaller
        return clip

background_clip = smart_resize_video(background_clip, target_width=1080)

def create_enhanced_video_text(text, max_width=35, video_size=None):
    """Create enhanced multi-line text optimized for video backgrounds"""
    # Break text into lines with appropriate width for video
    lines = textwrap.wrap(text, width=max_width)
    text_clips = []
    
    # Enhanced styling for video backgrounds
    font_size = 50 if video_size and video_size[0] >= 1080 else 40
    stroke_width = 4 if video_size and video_size[0] >= 1080 else 3
    
    for i, line in enumerate(lines):
        line_clip = TextClip(text=line, 
                           color='white', 
                           font_size=font_size,
                           stroke_color='black', 
                           stroke_width=stroke_width)
        
        # FIXED: Simple center positioning for all text
        line_clip = line_clip.with_duration(final_duration)
        text_clips.append(line_clip)
    
    return text_clips

def create_dynamic_text_background(text_clips, bg_style='gradient'):
    """Create text with dark background for better visibility"""
    combined_clips = []
    
    for text_clip in text_clips:
        # Create a semi-transparent black background
        bg_width = text_clip.size[0] + 40  # Add padding
        bg_height = text_clip.size[1] + 20  # Add padding
        
        # Create black background
        bg_color = ColorClip(size=(bg_width, bg_height), color=(0, 0, 0))
        bg_with_opacity = bg_color.with_opacity(0.6).with_duration(text_clip.duration)
        
        # Create composite with background and text, both centered
        composite = CompositeVideoClip([
            bg_with_opacity.with_position('center'),
            text_clip.with_position('center')
        ], size=text_clip.size)
        
        combined_clips.append(composite)
    
    return combined_clips

def analyze_video_for_text_placement(video_clip, sample_points=5):
    """Analyze video content to determine optimal text placement"""
    try:
        # Sample frames at different points in the video
        sample_times = [i * video_clip.duration / sample_points for i in range(sample_points)]
        
        # Simple analysis: check brightness in different regions
        regions_brightness = {'top': 0, 'center': 0, 'bottom': 0}
        
        for t in sample_times:
            if t < video_clip.duration:
                frame = video_clip.get_frame(t)
                h, w = frame.shape[:2]
                
                # Calculate average brightness for each region
                top_region = frame[:h//3, :]
                center_region = frame[h//3:2*h//3, :]
                bottom_region = frame[2*h//3:, :]
                
                regions_brightness['top'] += top_region.mean()
                regions_brightness['center'] += center_region.mean()
                regions_brightness['bottom'] += bottom_region.mean()
        
        # Find the region with medium brightness (best for text visibility)
        avg_brightness = {k: v/len(sample_times) for k, v in regions_brightness.items()}
        
        # Sort by how close to medium brightness (128)
        optimal_region = min(avg_brightness.items(), 
                           key=lambda x: abs(x[1] - 128))
        
        print(f"Optimal text placement: {optimal_region[0]} (brightness: {optimal_region[1]:.1f})")
        
        position_map = {
            'top': ('center', 0.2),      # 20% from top
            'center': ('center', 0.5),   # Center
            'bottom': ('center', 0.8)    # 20% from bottom
        }
        
        return position_map[optimal_region[0]]
        
    except Exception as e:
        print(f"Text placement analysis failed: {e}")
        return ('center', 0.8)  # Default to bottom center

# Create enhanced text with intelligent positioning
optimal_position = analyze_video_for_text_placement(background_clip)
# Force center positioning for now to ensure it works
optimal_position = ('center', 0.5)  # Always center
print(f"Text will be positioned at: center")
text_clips = create_enhanced_video_text(proverb, max_width=35, video_size=background_clip.size)

# Apply center positioning to all text clips with proper duration
positioned_text_clips = []
for clip in text_clips:
    # Force center positioning
    positioned_clip = clip.with_position('center').with_duration(final_duration)
    positioned_text_clips.append(positioned_clip)

# Create text with enhanced background
text_with_bg = create_dynamic_text_background(positioned_text_clips, bg_style='gradient')

# Ensure all text clips have center positioning for the final composition
final_text_clips = []
for clip in text_with_bg:
    final_clip = clip.with_position('center').with_duration(final_duration)
    final_text_clips.append(final_clip)

# Enhanced audio processing
def process_audio_for_video(music_path, video_duration, video_audio=None):
    """Process audio with advanced mixing and enhancement"""
    
    # Load background music
    background_music = AudioFileClip(music_path).subclipped(0, video_duration)
    
    # Simple volume normalization
    def normalize_volume(audio_clip, target_volume=0.7):
        """Normalize audio to target volume level"""
        return audio_clip.with_volume_scaled(target_volume)
    
    background_music = normalize_volume(background_music, target_volume=0.8)
    
    if video_audio and video_audio.duration > 0:
        # Mix original video audio with background music
        try:
            original_audio = video_audio.subclipped(0, video_duration)
            original_audio = normalize_volume(original_audio, target_volume=0.3)
            
            # Create composite audio
            final_audio = CompositeAudioClip([original_audio, background_music])
            print("Mixed original video audio with background music")
            return final_audio
        except Exception as e:
            print(f"Audio mixing failed: {e}, using background music only")
            return background_music
    else:
        print("Using background music only")
        return background_music

# Process audio
final_audio = process_audio_for_video(music_path, final_duration, background_clip.audio)

# Create the final composite video with centered text
video = CompositeVideoClip([background_clip] + final_text_clips)
video = video.with_audio(final_audio)

# Enhanced export settings for high quality
output_path = "motivational_video_with_video_bg_enhanced.mp4"

# Quality settings based on video resolution
video_width = background_clip.size[0]
if video_width >= 1080:
    # High quality settings for HD content
    export_settings = {
        'fps': 30,
        'codec': 'libx264',
        'audio_codec': 'aac',
        'bitrate': '3000k',
        'preset': 'medium'  # Balance between quality and encoding speed
    }
elif video_width >= 720:
    # Medium quality settings
    export_settings = {
        'fps': 30,
        'codec': 'libx264',
        'audio_codec': 'aac',
        'bitrate': '2000k'
    }
else:
    # Standard quality settings
    export_settings = {
        'fps': 24,
        'codec': 'libx264',
        'audio_codec': 'aac',
        'bitrate': '1500k'
    }

print(f"Exporting with settings: {export_settings}")

try:
    video.write_videofile(output_path, **export_settings)
    print(f"Enhanced video with video background saved as {output_path}")
    
    # Display final video info
    print(f"\n📊 Final Video Stats:")
    print(f"   Duration: {final_duration:.1f} seconds")
    print(f"   Resolution: {background_clip.size[0]}x{background_clip.size[1]}")
    print(f"   Text lines: {len(final_text_clips)}")
    print(f"   Audio: {'Mixed' if background_clip.audio else 'Background music only'}")
    
except Exception as e:
    print(f"Export failed: {e}")
    # Try with lower quality settings as fallback
    fallback_settings = {
        'fps': 24,
        'codec': 'libx264',
        'audio_codec': 'aac',
        'bitrate': '1000k'
    }
    print("Trying with fallback settings...")
    video.write_videofile(output_path, **fallback_settings)
    print(f"Video saved with fallback settings as {output_path}")

finally:
    # Clean up resources
    background_clip.close()
    if final_audio:
        final_audio.close()
    video.close()
    print("Resources cleaned up successfully")
