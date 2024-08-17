from django import forms
from django.utils.translation import gettext_lazy as _
from . import models

class Create(forms.ModelForm):
    class Meta:
        model = models.Model_Post
        exclude = ['publish_date']
        
        