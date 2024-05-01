from django.db import models

class Product(models.Model):
    name = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(upload_to='', blank=True, null=True)
    evaluation = models.FloatField()

    def __str__(self):
        return self.name
    """
    def image_url(self):
        if self.image:
            return f'/frontend/img/{self.image.name}'
        return None
    """
