from django import forms
from django.utils.translation import gettext_lazy as _
from . import models

class Create(forms.ModelForm):
    class Meta:
        model = models.Sentence
        fields = ['name', 'comment', 'user_sentence']
        
class Execute_Form(forms.Form):
    pass