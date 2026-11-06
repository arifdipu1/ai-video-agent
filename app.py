

import streamlit as st
import os
import asyncio
from pathlib import Path
from magic_hour import Client

BASE = Path.home() / "ai-video-agent"
OUTPUT = BASE / "output"
OUTPUT.mkdir(parents=True, exist_ok=True)

st.set_page_config(
    page_title="My AI Video Studio",
    page_icon="🎬",
    layout="wide"
)

st.title("🎬 My AI Video Studio")
st.write("Create realistic AI videos with voiceover.")

topic = st.text_area(
    "Describe your AI video",
    placeholder="A beautiful cinematic morning in a green forest, birds flying, sunlight moving through the trees."
)

st.info("First test: 5-second AI video, 480p.")

voice = st.selectbox(
    "Voice",
    ["American Female", "American Male"]
)

confirm = st.checkbox(
    "I understand that generating a video may use my free credits."
)

if st.button("Create 5-Second AI Video", type="primary"):

    if not topic.strip():
        st.warning("Please enter a video description.")

    elif not confirm:
        st.warning("Please confirm before generation.")

    elif not st.secrets.get("MAGIC_HOUR_API_KEY"):
        st.error("Magic Hour API key is missing.")

    else:
        try:
            with st.spinner("Creating your AI video..."):

                client = Client(
                    token=st.secrets["MAGIC_HOUR_API_KEY"]
                )

                result = client.v1.text_to_video.generate(
                    name="My First AI Video",
                    end_seconds=5,
                    aspect_ratio="16:9",
                    style={"prompt": topic},
                    model="ltx-2.5",
                    resolution="480p",
                    audio=True,
                    wait_for_completion=True,
                    download_outputs=True,
                    download_directory=str(OUTPUT)
                )

            st.success("AI video generation finished!")
            st.write(result)

            videos = list(OUTPUT.glob("*.mp4"))

            if videos:
                video = max(videos, key=lambda p: p.stat().st_mtime)
                st.video(str(video))

                with open(video, "rb") as f:
                    st.download_button(
                        "Download AI Video",
                        f,
                        file_name="my_ai_video.mp4",
                        mime="video/mp4"
                    )

        except Exception as e:
            st.error(f"Video generation failed: {e}")
