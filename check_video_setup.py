import os
from moviepy import VideoFileClip

def check_video_setup():
    videos_folder = "videos"
    
    # Check if videos folder exists
    if not os.path.exists(videos_folder):
        print("❌ Videos folder doesn't exist yet")
        return False
    
    # Check for video files
    video_files = [f for f in os.listdir(videos_folder) if f.endswith(('.mp4', '.mov', '.avi', '.mkv'))]
    
    if not video_files:
        print("❌ No video files found in 'videos' folder")
        print("📁 Please upload your video file (like 4434150-hd_1080_1920_30fps.mp4) to the videos/ folder")
        return False
    
    print(f"✅ Found {len(video_files)} video file(s):")
    for video in video_files:
        video_path = os.path.join(videos_folder, video)
        try:
            # Try to load video to check if it's valid
            with VideoFileClip(video_path) as clip:
                duration = clip.duration
                size = clip.size
            print(f"   📹 {video} - Duration: {duration:.1f}s, Size: {size[0]}x{size[1]}")
        except Exception as e:
            print(f"   ❌ {video} - Error: {str(e)}")
    
    return True

if __name__ == "__main__":
    print("🎬 Video Background Setup Checker")
    print("=" * 40)
    
    if check_video_setup():
        print("\n✅ Ready to create videos with video backgrounds!")
        print("Run: python create_video_with_video_bg.py")
    else:
        print("\n📋 Next steps:")
        print("1. Upload your video file to the videos/ folder")
        print("2. Run this checker again to verify")
        print("3. Then run: python create_video_with_video_bg.py")
