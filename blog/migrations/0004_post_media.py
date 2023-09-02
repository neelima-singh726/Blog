# Generated by Django 4.2.4 on 2023-09-02 04:28

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0003_post_post_image'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='media',
            field=models.FileField(blank=True, null=True, upload_to='post_media/', validators=[django.core.validators.FileExtensionValidator(allowed_extensions=['jpg', 'jpeg', 'png', 'gif', 'pdf'])]),
        ),
    ]
