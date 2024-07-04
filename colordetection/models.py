from django.db import models

class UploadedImage(models.Model):
    image = models.ImageField(upload_to='images/')

class UploadedVideo(models.Model):
    video = models.FileField(upload_to='videos/')
