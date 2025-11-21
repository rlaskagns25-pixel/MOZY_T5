from django.db import models
from django.contrib.auth.models import User

class MoodEntry(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    date = models.DateField()
    emotion = models.CharField(max_length=20)
    note = models.TextField()

    def __str__(self):
        return f"{self.date} - {self.emotion}"