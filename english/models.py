from django.db import models
from django.utils import timezone

# Create your models here.
class Model_Post(models.Model):
    name = models.CharField(verbose_name='name_post',  max_length=50, default=None)
    comment = models.CharField(max_length=500)
    sentence = models.TextField(default=None)
    publish_date = models.DateTimeField(default=timezone.now())
    def __str__(self: str) -> str:
        return self.name
