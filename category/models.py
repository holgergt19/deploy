from django.db import models
from django.urls import reverse

class Category(models.Model):
    category_name = models.CharField(max_length=20, unique = True)
    descripcion = models.CharField(max_length=255, blank = True)
    slug = models.CharField(max_length=20, unique = True)
    cat_image = models.ImageField(upload_to = 'photos/category', blank = True)
    
    class Meta:
        verbose_name = 'category'
        verbose_name_plural = 'categories'
        
    
    def get_url(self):
        return reverse('servicios_by_category', args=[self.slug])
           
    def __str__(self):
        return self.category_name