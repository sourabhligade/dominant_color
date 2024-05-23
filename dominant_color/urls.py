from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from colordetection import views

urlpatterns = [
    path('', views.upload_image, name='home'),  # Mapping root URL to upload_image view
    path('admin/', admin.site.urls),
]

# Serve media files during development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
