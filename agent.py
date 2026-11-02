import subprocess
from pathlib import Path

BASE = Path.home() / "ai-video-agent"
OUTPUT = BASE / "output"
OUTPUT.mkdir(exist_ok=True)

def make_video():
    print("\nAI Video Agent")
    topic = input("Video topic: ")

    if not topic.strip():
        print("Please enter a topic.")
        return

    voice_text = f"Welcome! Today we are talking about {topic}."

    audio_file = OUTPUT / "voice.mp3"
    video_file = OUTPUT / "ai_video.mp4"

    print("\nCreating American female voice...")

    subprocess.run([
        "edge-tts",
        "--voice", "en-US-AriaNeural",
        "--text", voice_text,
        "--write-media", str(audio_file)
    ], check=True)

    print("Creating video...")

    subprocess.run([
        "ffmpeg", "-y",
        "-f", "lavfi",
        "-i", "color=c=skyblue:s=1920x1080:d=10",
        "-i", str(audio_file),
        "-vf",
        "drawtext=text='My AI Video':fontcolor=white:fontsize=70:x=(w-text_w)/2:y=(h-text_h)/2",
        "-c:v", "libx264",
        "-c:a", "aac",
        "-shortest",
        "-pix_fmt", "yuv420p",
        str(video_file)
    ], check=True)

    print("\nVideo created successfully!")
    print(f"Video: {video_file}")

if __name__ == "__main__":
    make_video()
