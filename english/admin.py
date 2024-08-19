from django.contrib import admin

from . import models
# Register your models here.
admin.site.register(models.Task_Model)
admin.site.register(models.Answer_Correct_Model)
admin.site.register(models.Answer_Wrong_Model)