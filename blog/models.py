from django.utils import timezone
from django.db import models
from django.contrib.auth.models import User
from django.core.validators import FileExtensionValidator


# Create your models here.
class Post(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=120)
    content = models.TextField()
    published_at = models.DateTimeField(default=timezone.now)
    post_code = models.CharField(max_length=6, unique=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    # media = models.ImageField(upload_to='post_media/', blank=True, null=True)

    media = models.FileField(upload_to='post_media/', blank=True, null=True, validators=[
        FileExtensionValidator(allowed_extensions=['jpg', 'jpeg', 'png', 'gif', 'pdf'])
    ])
    post_image = models.ImageField(upload_to="postimg")

    # To specify table name the to use default name
    class Meta:
        # db_table = 'posts'
        ordering = ['-published_at']   #ordering in descending order of publishedst date

    def __str__(self):
        return self.title