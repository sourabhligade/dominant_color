# myproject/urls.py

from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from colordetection import views

urlpatterns = [
    path('', views.upload_image, name='home'),  # Home page
    path('admin/', admin.site.urls),  # Admin site
    path('upload-video/', views.upload_video, name='upload_video'),  # Video upload page
    path('upload-image/', views.upload_image, name='upload_image'),  # Image upload page
]

# Serve media files during development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
