# myapp/urls.py

from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from . import views

urlpatterns = [
    path('upload-video/', views.upload_video, name='upload_video'),
    path('upload-image/', views.upload_image, name='upload_image'),
]

# Add this to serve media files during development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
