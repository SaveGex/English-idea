from django.db import models
from django.contrib.postgres.fields import ArrayField
from django.utils import timezone

# Create your models here.
class Sentence(models.Model):
    name = models.CharField(max_length=100)
    identifier = models.TextField(default = f"UniqueName_{name}_{timezone.now()}")
    # I think need to save and user sentence as what he wrote
    comment = models.TextField(null=True, blank=True)
    user_sentence = models.TextField()
    published_date = models.DateTimeField(default=timezone.now)
    
    #for show in html
    processed_sentence = models.TextField(null=True)
    # for comparing output and sentence
    correct_sentence = ArrayField(models.CharField(max_length=255), null=True)
    # i forgot
    fields = models.IntegerField(null=True)
    # how many answers can will be in sentence
    answers = models.IntegerField(null=True)
    
    def __str__(self) -> str:
        return f"name: {self.name}\nuser_sentence: {self.user_sentence}\n fields: {self.fields}\n answers: {self.answers}"



class Wrong_Answer(models.Model):
    index = models.IntegerField()
    key = models.ForeignKey(Sentence, on_delete=models.CASCADE)
    def __str__(self) -> str:
        return f"text: {self.key}\n index: {self.index}"
    
    
class Correct_Answer(models.Model):
    index = models.IntegerField(null=True)
    key = models.ForeignKey(Sentence, on_delete=models.CASCADE)
    phrase = models.CharField(max_length=301)
    def __str__(self) -> str:
        return f"text: {self.key}\n index: {self.index}\n phrase: {self.phrase}"