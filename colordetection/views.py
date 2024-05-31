from django.shortcuts import render
from .forms import ImageUploadForm
import cv2
import numpy as np
import pandas as pd
from ultralytics import YOLO
import os
from django.conf import settings
import random

# Load color data
color_data = pd.read_csv('colordetection/data/colors.csv')
index = ["color", "color_name", "hex", "R", "G", "B"]
csv = pd.read_csv('colordetection/data/colors.csv', names=index, header=None)

# Load YOLO model
model = YOLO('yolov8n.pt')  # you can replace 'yolov8n.pt' with the appropriate model file

def find_dominant_color(image):
    # Reshape the image into a 2D array of pixels
    pixels = image.reshape((-1, 3))
    
    # Convert to float32
    pixels = np.float32(pixels)
    
    # Define criteria and apply kmeans()
    criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 100, 0.2)
    k = 5  # You can adjust this value based on your needs
    _, labels, centroids = cv2.kmeans(pixels, k, None, criteria, 10, cv2.KMEANS_RANDOM_CENTERS)
    
    # Convert centroids to integer
    centroids = np.uint8(centroids)
    
    # Find the dominant color
    counts = np.bincount(labels.flatten())
    dominant_color_bgr = centroids[np.argmax(counts)]
    
    # Convert BGR to RGB
    dominant_color_rgb = dominant_color_bgr[::-1]
    
    return dominant_color_rgb

def get_color_name(R, G, B):
    minimum = 10000
    cname = "Unknown"
    for i in range(len(csv)):
        d = abs(R - int(csv.loc[i, "R"])) + abs(G - int(csv.loc[i, "G"])) + abs(B - int(csv.loc[i, "B"]))
        if d <= minimum:
            minimum = d
            cname = csv.loc[i, "color_name"]
    return cname

def generate_colors(num_colors):
    """Generate distinct colors for the bounding boxes."""
    colors = []
    for i in range(num_colors):
        color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
        colors.append(color)
    return colors

def yolo_object_detection(image_path):
    # Perform YOLO object detection
    results = model(image_path)

    # Process the detection results
    detection_results = []
    image = cv2.imread(image_path)
    detection_count = 1  # Initialize a counter for the detection numbers
    colors = generate_colors(len(results[0].boxes))  # Generate a unique color for each detection

    for result in results:
        for idx, box in enumerate(result.boxes):
            x1, y1, x2, y2 = map(int, box.xyxy[0])  # bounding box coordinates
            conf = float(box.conf[0])  # confidence score
            cls = int(box.cls[0])  # class id
            label = model.names[cls]  # class label
            
            # Extract the region of interest (ROI) from the image
            roi = image[y1:y2, x1:x2]
            
            # Find the dominant color in the ROI
            dominant_color_rgb = find_dominant_color(roi)
            nearest_color_name = get_color_name(*dominant_color_rgb)
            
            detection_results.append({
                'number': detection_count,
                'label': label,
                'confidence': conf,
                'box': (x1, y1, x2 - x1, y2 - y1),  # (x, y, width, height)
                'dominant_color': dominant_color_rgb,
                'color_name': nearest_color_name
            })

            # Draw bounding boxes and numbers on the image
            color = colors[idx]  # Use the unique color for each bounding box
            cv2.rectangle(image, (x1, y1), (x2, y2), color, 2)
            cv2.putText(image, str(detection_count), (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, color, 2)
            detection_count += 1
    
    # Save the result image
    result_image_path = os.path.join(settings.MEDIA_ROOT, 'results', os.path.basename(image_path).replace(".jpg", "_yolo.jpg"))
    os.makedirs(os.path.dirname(result_image_path), exist_ok=True)  # Ensure the directory exists
    cv2.imwrite(result_image_path, image)
    result_image_url = os.path.join(settings.MEDIA_URL, 'results', os.path.basename(result_image_path))

    return result_image_url, detection_results

def upload_image(request):
    if request.method == 'POST':
        form = ImageUploadForm(request.POST, request.FILES)
        if form.is_valid():
            # Save the uploaded image
            form.save()
            
            # Get the path of the uploaded image
            image_path = form.instance.image.path
            
            # Perform YOLO object detection
            result_image_url, detection_results = yolo_object_detection(image_path)

            return render(request, 'colordetection/result.html', {
                'result_image_url': result_image_url,
                'detections': detection_results
            })
    else:
        form = ImageUploadForm()
    
    return render(request, 'colordetection/upload.html', {'form': form})
