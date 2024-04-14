"""rom django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include

from colordetection import views


urlpatterns = [
    path('', views.upload_image, name='home'),  # Mapping root URL to upload_image view

    path('admin/', admin.site.urls),
]
