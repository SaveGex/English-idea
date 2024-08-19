from django import forms
from django.utils.translation import gettext_lazy as _
from . import models

class Create(forms.ModelForm):
    class Meta:
        model = models.Task_Model
        fields = ['name', 'sentence']
        
class Execute_Form(forms.Form):
    pass