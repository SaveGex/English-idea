from django.contrib import admin

from . import models
# Register your models here.
admin.site.register(models.Sentence)
admin.site.register(models.Correct_Answer)
admin.site.register(models.Wrong_Answer)