import cv2
import os
from django.conf import settings


def process_video_and_generate_result(video_path):
    cap = cv2.VideoCapture(video_path)
    frame_count = 0
    frames_results = []

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        # Process each frame here (e.g., perform object detection, etc.)
        # Example: Perform object detection on 'frame'

        # Save processed frame result
        
        result_image_path = os.path.join(settings.MEDIA_ROOT, 'results', f'frame_{frame_count}.jpg')
        cv2.imwrite(result_image_path, frame)

        # Example: Assuming you have some results to store
        detection_results = [
            {'label': 'Person', 'box': (100, 100, 200, 200)},
            {'label': 'Car', 'box': (300, 300, 400, 400)},
        ]

        frames_results.append({
            'frame': frame_count,
            'detection_results': detection_results,
            'result_image_url': result_image_path,
        })

        frame_count += 1

    cap.release()

    # Generate video from processed frames
    video_output_path = os.path.join(settings.MEDIA_ROOT, 'results', 'output_video.mp4')
    convert_frames_to_video(frames_results, video_output_path)

    return frames_results, video_output_path

def convert_frames_to_video(frames_results, output_path):
    try:
        # Read dimensions from the first frame (assuming at least one frame exists)
        first_frame_path = frames_results[0]['result_image_url']
        first_frame = cv2.imread(first_frame_path)
        if first_frame is None:
            raise ValueError(f"Failed to read image at {first_frame_path}")

        frame_height, frame_width, _ = first_frame.shape

        # Initialize video writer
        out = cv2.VideoWriter(output_path, cv2.VideoWriter_fourcc(*'mp4v'), 30, (frame_width, frame_height))

        # Write frames to video
        for frame_result in frames_results:
            img_path = frame_result['result_image_url']
            img = cv2.imread(img_path)
            if img is None:
                print(f"Failed to read image at {img_path}. Skipping this frame.")
                continue
            out.write(img)

        out.release()
        print(f"Video saved successfully to {output_path}")
    except Exception as e:
        print(f"Error converting frames to video: {e}")
