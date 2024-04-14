from django.shortcuts import render
from .forms import ImageUploadForm
import cv2
import numpy as np

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

        return render(request, 'colordetection/result.html', {'dominant_color': dominant_color_rgb})
    else:
        form = ImageUploadForm()
    return render(request, 'colordetection/upload.html', {'form': form})