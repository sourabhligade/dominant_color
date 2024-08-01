# Object Detection with YOLOv8 in Django

This project is a Django-based web application for object detection using the YOLOv8 model. The application allows users to upload images and videos, perform object detection, and display the results with bounding boxes and labels.

Upload an Image
<img width="1310" alt="Screenshot 2024-07-21 at 11 42 08 PM" src="https://github.com/user-attachments/assets/16609e50-e190-4ddc-abfe-10ca6adc1e4b">

Check out the detections 
<img width="1310" alt="Screenshot 2024-07-21 at 11 42 25 PM" src="https://github.com/user-attachments/assets/c9c9ff4a-770c-4c11-a869-8c8b11611409">
Shows Colors of the detected objects and other filters
<img width="1310" alt="Screenshot 2024-07-21 at 11 42 32 PM" src="https://github.com/user-attachments/assets/6df99041-cf8f-44c4-8aaf-e48aaee317b6">
<img width="1310" alt="Screenshot 2024-07-21 at 11 42 29 PM" src="https://github.com/user-attachments/assets/eb3eef83-6957-40b2-9b42-e8509dcc95b3">
## Features

- Image and video upload
- Object detection using YOLOv8
- Display detected objects with bounding boxes and labels
- Display dominant colors and color names for detected objects
- Save and display the results

## Prerequisites

- Python 3.x
- Django
- OpenCV
- NumPy
- Pandas
- UltraLytics YOLO

## Installation

1. **Clone the repository:**
    ```bash
    git clone https://github.com/sourabhligade/dominant_color.git
    cd yolo-django-object-detection
    ```

2. **Create and activate a virtual environment:**
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
    ```

3. **Install the required packages:**
    ```bash
    pip install -r requirements.txt
    ```

4. **Apply migrations:**
    ```bash
    python manage.py migrate
    ```

5. **Run the Django development server:**
    ```bash
    python manage.py runserver
    ```

## Usage

### Uploading an Image

1. Navigate to `http://127.0.0.1:8000/upload-image/` in your web browser.
2. Use the form to upload an image file.
3. Click the "Upload" button.
4. The object detection results will be displayed, including bounding boxes and labels.

### Uploading a Video

1. Navigate to `http://127.0.0.1:8000/upload-video/` in your web browser.
2. Use the form to upload a video file.
3. Click the "Upload" button.
4. The object detection results will be displayed for each frame of the video.


