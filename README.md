# Football Vision Analyzer

An AI-powered football analysis system using computer vision, deep learning, and tracking to extract insights from match footage.

## Features
- Player, referee, and ball detection with YOLOv8
- Player tracking across frames
- Team identification using KMeans clustering on jersey colors
- Camera movement estimation with optical flow
- Perspective transformation for real-world measurements
- Speed and distance calculation for players

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/your-username/football-vision-analyzer.git
   cd football-vision-analyzer

2. (Optional but recommended) Create and activate a virtual environment:
    python -m venv venv
    source venv/bin/activate      # On Linux/Mac
    .\venv\Scripts\activate       # On Windows PowerShell

3. Install dependencies:

    pip install -r requirements.txt


## Usage:

Please run the program using Streamlit:

    streamlit run app.py


## Notes

    Large model files (e.g., YOLO weights) are managed via Git LFS.

    Ensure you have git-lfs installed to clone the repo properly.

    