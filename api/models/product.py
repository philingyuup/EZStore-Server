from django.db import models

from .user import User

# Create your models here.
class Product(models.Model):
  # define fields
  # https://docs.djangoproject.com/en/3.0/ref/models/fields/
  name = models.CharField(max_length=100)
  img = models.TextField(blank=True)
  short_description = models.TextField(blank=True)
  long_description = models.TextField(blank=True)
  price = models.DecimalField(max_digits=9, decimal_places=2, default=0)
  owner = models.ForeignKey(
      User,
      on_delete=models.CASCADE
  )
  created_at = models.DateTimeField(auto_now_add=True)
  updated_at = models.DateTimeField(auto_now=True)


  def __str__(self):
    # This must return a string
    return f"{self.name}: ${self.price}"

  def as_dict(self):
    """Returns dictionary version of product models"""
    return {
        'id': self.id,
        'name': self.name,
        'img': self.img,
        'short_description': self.short_description,
        'long_description': self.long_description,
        'price': self.price,
        'owner': self.owner,
        'created_at': self.created_at,
        'updated_at': self.updated_at
    }
