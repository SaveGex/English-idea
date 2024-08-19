from django.db import models
from django.utils import timezone

# Create your models here.
class Task_Model(models.Model):
    name = models.CharField(verbose_name='name_post',  max_length=50, default=None)
    comment = models.CharField(max_length=500, null=True)
    sentence = models.TextField(default=None)
    publish_date = models.DateTimeField(default=timezone.now)
    def __str__(self: str) -> str:
        return self.name


class Answer_Model(models.Model):
    task = models.ForeignKey(Task_Model, on_delete=models.CASCADE, related_name='answers')
    will_showed = models.TextField(default=None)
    correct_word = models.TextField(default=None)
    position_wrong = models.IntegerField(default=None)
    position_correct = models.IntegerField(default=None)
    def __str__(self):
        return f"{self.correct_word} at position_wrong {self.position_wrong} and position_correct {self.position_correct} in {self.task.name}"