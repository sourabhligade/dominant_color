from django.shortcuts import render
from .forms import ImageUploadForm
import cv2
import numpy as np
import pandas as pd

color_data = pd.read_csv('colordetection/data/colors.csv')

index = ["color", "color_name", "hex", "R", "G", "B"]
csv = pd.read_csv('colordetection/data/colors.csv', names=index, header=None)


def find_dominant_color(image_path):
    # Load the image
    image = cv2.imread(image_path)

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
    for i in range(len(csv)):
        d = abs(R - int(csv.loc[i, "R"])) + abs(G - int(csv.loc[i, "G"])) + abs(B - int(csv.loc[i, "B"]))
        if d <= minimum:
            minimum = d
            cname = csv.loc[i, "color_name"]
    return cname

def upload_image(request):
    if request.method == 'POST':
        form = ImageUploadForm(request.POST, request.FILES)
        if form.is_valid():
            # Save the uploaded image
            form.save()

            # Get the path of the uploaded image
            image_path = form.instance.image.path

            # Find the dominant color
            dominant_color_rgb = find_dominant_color(image_path)
            
            # Find the nearest color name
            nearest_color_name = get_color_name(*dominant_color_rgb)

            return render(request, 'colordetection/result.html', {'dominant_color': dominant_color_rgb, 'color_name': nearest_color_name})
    else:
        form = ImageUploadForm()
    return render(request, 'colordetection/upload.html', {'form': form})
