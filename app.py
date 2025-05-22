import streamlit as st
import tempfile
import time
import numpy as np
from main import main as run_analysis  # Make sure run_analysis returns team_ball_control or saves it to a file
import os
os.environ["STREAMLIT_SERVER_ENABLE_FILE_WATCHER"] = "false"  # Disables problematic inspection

# Page setup
st.set_page_config(
    page_title="Football Vision Analyzer",
    page_icon="⚽",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Sidebar Navigation
st.sidebar.title("⚙️ Navigation")
page = st.sidebar.radio("Go to", ["🏠 Home", "ℹ️ About Project"], label_visibility="collapsed")

st.sidebar.markdown("---")
st.sidebar.write("Made with ❤️ by Harish")

# -----------------------------------
# 🏠 HOME PAGE
# -----------------------------------
if page == "🏠 Home":
    st.title("🎥 Football Vision Analyzer")
    st.subheader("⚽ AI-powered match analysis using computer vision")

    st.markdown("Upload a short football match clip (up to 30 seconds) to analyze player movement, team control, and more. (since the model is still in development, you are restricted to use only the sample video)")

    video_path = "input_videos/input_video.mp4"
    video_ready = True
    st.markdown("### 📊 Input Video")
    st.video(video_path)


    if video_ready:
        if st.button("🚀 Run Football Analysis"):
            progress = st.progress(0)
            status = st.empty()

            try:
                for i in range(0, 6, 2):
                    progress.progress(i)
                    status.info(f"🔍 Processing... {i}%")
                    time.sleep(1)

                # Run analysis: Make sure this returns team_ball_control numpy array
                run_analysis()

                progress.progress(100)
                status.success("✅ Analysis complete!")

                st.markdown("### 📊 Output Video")
                st.video("output_videos/output_video.mp4")

            except Exception as e:
                st.error(f"❌ Failed to analyze: {e}")

# -----------------------------------
# ℹ️ ABOUT SECTION
# -----------------------------------
elif page == "ℹ️ About Project":
    st.title("ℹ️ About the Project")
    st.markdown("""
    ### Objective
    The **Football Vision Analyzer** is an AI-powered tool that analyzes football match footage using computer vision and deep learning. It extracts insights like:
    - Player movements and positions
    - Team control zones
    - Speed and distances
    - Ball possession percentage
                
    ###  Technologies Used
    - **YOLOv8** for player and ball detection
    - **OpenCV** and **ffmpeg**
    - **Optical Flow** to measure the camera movement
    - **K-Means clustering** for team color detection
    - **Streamlit** for the interactive dashboard

    ### Future Features
    - Detailed statistics (heat-maps, passing network)
    - Real-time commentary insights
    - Performance ratings

    ###  Developer
    Built with ❤️ by Harish — a computer science student with a love for AI and football.
    """)

