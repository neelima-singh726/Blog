from django import forms
from django.forms import ModelForm, ValidationError

from blog.models import Post


class PostForm(ModelForm):
    post_code = forms.CharField(max_length=6, widget=forms.TextInput(attrs={'pattern': '[A-Za-z0-9]{6}'}))

    
    class Meta:
        model = Post
        fields = ['post_code','title','content','post_image','media']

    def clean_media(self):
        media = self.cleaned_data.get('media')
        if media:
            max_size = 5242880  # 5MB in bytes
            if media.size > max_size:
                raise ValidationError(f"File size must be no more than {max_size/1024/1024} MB.")
        return media
