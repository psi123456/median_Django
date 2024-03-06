from django.db import models

# Create your models here.
from django.db import models
from django.core.validators import FileExtensionValidator
import os
from django.conf import settings

class ImageModel(models.Model):
    title = models.CharField(max_length=255, blank=True)
    image = models.ImageField(
        upload_to='uploads/',
        validators=[FileExtensionValidator(allowed_extensions=['jpg', 'jpeg', 'png'])]
    )

    class Meta:
        db_table = 'custom_image_table'
        ordering = ['-id']

    def __str__(self):
        return self.title or "No Title"

    def get_image_url(self):
        return self.image.url

class PredictionResult(models.Model):
    image_path = models.CharField(max_length=255)  # 이미지 경로 저장 필드
    x1 = models.IntegerField()
    y1 = models.IntegerField()
    x2 = models.IntegerField()
    y2 = models.IntegerField()
    class_label = models.CharField(max_length=255)

    class Meta:
        db_table = 'prediction_results'

    def __str__(self):
        return f'Result for {self.image_path} (ID: {self.id})'

    def get_image_url(self):
        return os.path.join(settings.MEDIA_URL, str(self.image_path))

