import cv2
import sys
import numpy as np
sys.path.append('../')
from utils import measure_distance, get_foot_position

class SpeedAndDistance_Estimator():
    def __init__(self):
        self.frame_window = 5
        self.frame_rate = 24
        self.heatmap_positions = {}  # NEW: store positions for heatmaps

    def add_speed_and_distance_to_tracks(self, tracks):
        total_distance = {}

        for obj_class, obj_tracks in tracks.items():
            if obj_class in ["ball", "referees"]:
                continue

            number_of_frames = len(obj_tracks)

            for frame_num in range(0, number_of_frames, self.frame_window):
                last_frame = min(frame_num + self.frame_window, number_of_frames - 1)

                for track_id, _ in obj_tracks[frame_num].items():
                    if track_id not in obj_tracks[last_frame]:
                        continue

                    start_pos = obj_tracks[frame_num][track_id]['position_transformed']
                    end_pos = obj_tracks[last_frame][track_id]['position_transformed']

                    if start_pos is None or end_pos is None:
                        continue

                    # Distance & Speed
                    distance_covered = measure_distance(start_pos, end_pos)
                    time_elapsed = (last_frame - frame_num) / self.frame_rate
                    speed_mps = distance_covered / time_elapsed
                    speed_kph = speed_mps * 3.6

                    # Distance aggregation
                    if obj_class not in total_distance:
                        total_distance[obj_class] = {}
                    if track_id not in total_distance[obj_class]:
                        total_distance[obj_class][track_id] = 0
                    total_distance[obj_class][track_id] += distance_covered

                    # Add to track info
                    for i in range(frame_num, last_frame):
                        if track_id not in tracks[obj_class][i]:
                            continue
                        tracks[obj_class][i][track_id]['speed'] = speed_kph
                        tracks[obj_class][i][track_id]['distance'] = total_distance[obj_class][track_id]

                        # --- NEW: Collect positions for heatmap ---
                        pos = tracks[obj_class][i][track_id].get('position_transformed')
                        if pos is not None:
                            self.heatmap_positions.setdefault(obj_class, {}).setdefault(track_id, []).append(pos)

    def draw_speed_and_distance(self, frames, tracks):
        output_frames = []
        for frame_num, frame in enumerate(frames):
            for obj_class, obj_tracks in tracks.items():
                if obj_class in ["ball", "referees"]:
                    continue

                for _, track_info in obj_tracks[frame_num].items():
                    if "speed" in track_info:
                        speed = track_info.get('speed')
                        distance = track_info.get('distance')
                        if speed is None or distance is None:
                            continue

                        bbox = track_info['bbox']
                        position = get_foot_position(bbox)
                        position = list(position)
                        position[1] += 40
                        position = tuple(map(int, position))

                        cv2.putText(frame, f"{speed:.2f} km/h", position, cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 2)
                        cv2.putText(frame, f"{distance:.2f} m", (position[0], position[1] + 20), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 2)
            output_frames.append(frame)

        return output_frames

    def generate_team_heatmaps(self, pitch_size=(100, 100), field_dimensions=(23.32, 68)):
        heatmaps = {'team1': np.zeros(pitch_size, dtype=np.float32),
                    'team2': np.zeros(pitch_size, dtype=np.float32)}

        # Map team color to heatmap keys, for example:
        color_to_team = {
            (0, 0, 255): 'team1',  # BGR Red
            (255, 0, 0): 'team2'   # BGR Blue (or whatever colors you use)
        }

        for frame_tracks in self.heatmap_positions.get('players', []):
            for track_id, track_info in frame_tracks.items():
                pos = track_info.get('position_transformed')
                team_color = tuple(track_info.get('team_color', (0, 0, 0)))

                if pos is None or team_color not in color_to_team:
                    continue

                x_norm = int((pos[0] / field_dimensions[0]) * pitch_size[1])
                y_norm = int((pos[1] / field_dimensions[1]) * pitch_size[0])

                # Clamp values
                x_norm = np.clip(x_norm, 0, pitch_size[1] - 1)
                y_norm = np.clip(y_norm, 0, pitch_size[0] - 1)

                heatmaps[color_to_team[team_color]][y_norm, x_norm] += 1

        return heatmaps

