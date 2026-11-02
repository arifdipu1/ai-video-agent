import streamlit as st
import subprocess
from pathlib import Path

BASE = Path.home() / "ai-video-agent"
OUTPUT = BASE / "output"
OUTPUT.mkdir(parents=True, exist_ok=True)

st.set_page_config(
    page_title="My AI Video Studio",
    page_icon="🎬",
    layout="wide"
)

st.title("🎬 My AI Video Studio")
st.write("Create videos with AI voiceover.")

topic = st.text_area(
    "What video do you want to create?",
    placeholder="A beautiful morning in nature"
)

duration = st.selectbox(
    "Video duration",
    ["10 seconds", "30 seconds", "1 minute"]
)

voice = st.selectbox(
    "Voice",
    ["American Female", "American Male"]
)

if st.button("Create My Video", type="primary"):

    if not topic.strip():
        st.warning("Please enter a video topic.")

    else:
        audio = OUTPUT / "voice.mp3"
        video = OUTPUT / "ai_video.mp4"

        voice_name = (
            "en-US-AriaNeural"
            if voice == "American Female"
            else "en-US-GuyNeural"
        )

        seconds = {
            "10 seconds": 10,
            "30 seconds": 30,
            "1 minute": 60
        }[duration]

        with st.spinner("Creating voice and video..."):

            script = f"Welcome! Today we are talking about {topic}."

            subprocess.run([
                "edge-tts",
                "--voice", voice_name,
                "--text", script,
                "--write-media", str(audio)
            ], check=True)

            subprocess.run([
                "ffmpeg", "-y",
                "-f", "lavfi",
                "-i", f"color=c=skyblue:s=1920x1080:d={seconds}",
                "-i", str(audio),
                "-vf",
                "drawtext=text='My AI Video':fontcolor=white:fontsize=70:x=(w-text_w)/2:y=(h-text_h)/2",
                "-c:v", "libx264",
                "-c:a", "aac",
                "-shortest",
                "-pix_fmt", "yuv420p",
                str(video)
            ], check=True)

        st.success("Your video is ready!")

        st.video(str(video))

        with open(video, "rb") as file:
            st.download_button(
                "Download MP4 Video",
                file,
                file_name="ai_video.mp4",
                mime="video/mp4"
            )
