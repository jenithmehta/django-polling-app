# pylint: disable=missing-function-docstring, missing-class-docstring, missing-module-docstring
import datetime
from django.db import models
from django.utils import timezone
# Create your models here.

class Question(models.Model):
    question_text= models.CharField(max_length=200)
    pub_date = models.DateTimeField(verbose_name="date_published")
    def __str__(self):
        return f"{self.question_text}"
    def was_published_recently(self):
        now = timezone.now()
        one_day_before = timezone.now() - datetime.timedelta(days=1)
        return one_day_before <= self.pub_date <= now

class Choice(models.Model):
    question = models.ForeignKey(to=Question,on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)
    def __str__(self):
        return f"{self.choice_text}"

