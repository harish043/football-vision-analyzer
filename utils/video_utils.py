
import cv2
import subprocess
import os


def read_video(video_path):
    cap = cv2.VideoCapture(video_path)
    frames = []
    while True:
        ret, frame = cap.read()
        if not ret:
            break
        frames.append(frame)
    return frames

def save_video(frames, output_path):
    temp_path = "temp_output.avi"
    fourcc = cv2.VideoWriter_fourcc(*'XVID')  # Save as AVI first
    out = cv2.VideoWriter(temp_path, fourcc, 24, (frames[0].shape[1], frames[0].shape[0]))

    for frame in frames:
        out.write(frame)
    out.release()

    # Convert AVI to proper MP4 with H.264
    output_dir = os.path.dirname(output_path)
    os.makedirs(output_dir, exist_ok=True)

    fixed_path = output_path
    subprocess.run([
        "ffmpeg",
        "-y",  # Overwrite if exists
        "-i", temp_path,
        "-vcodec", "libx264",
        "-crf", "23",
        "-preset", "fast",
        "-pix_fmt", "yuv420p",
        fixed_path
    ])

    os.remove(temp_path)  # Cleanup temp file
