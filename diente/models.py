from django.db import models
from django.contrib.postgres.fields import ArrayField
from odontologo.models import Odontologo

class ImageDiente(models.Model):
    image = models.ImageField(upload_to='uploads/')
    resized_image = models.ImageField(upload_to='resized/',blank=True, null=True)
    mask = models.ImageField(upload_to='masks/',blank=True, null=True)
    edited_images = ArrayField(models.URLField(max_length=500, blank=True, null=True), size=5, blank=True, null=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)
    idOdontologo = models.ForeignKey(Odontologo, on_delete=models.CASCADE)

    def __str__(self):
        return f"Image {self.id} uploaded by {self.idOdontologo} at {self.uploaded_at}"
