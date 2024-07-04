from django import forms
from .models import UploadedImage, UploadedVideo

class ImageUploadForm(forms.ModelForm):
    class Meta:
        model = UploadedImage
        fields = ['image']

from django import forms
from .models import UploadedVideo

class VideoUploadForm(forms.ModelForm):
    class Meta:
        model = UploadedVideo
        fields = ['video']
    
    video = forms.FileField(widget=forms.ClearableFileInput(attrs={'accept': 'video/*'}))
