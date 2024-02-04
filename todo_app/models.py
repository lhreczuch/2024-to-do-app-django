from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Task(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE) # 'on_delete' usuwa zadanie jeśli autor zostanie usunięty
    title = models.CharField(max_length = 50)
    description = models.TextField()
    assigned_user = models.ForeignKey(User, on_delete=models.DO_NOTHING,related_name='tasks_assigned')
    is_done = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

class Comment(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE) # 'on_delete' usuwa komentarz jeśli autor zostanie usunięty
    task = models.ForeignKey(Task, on_delete=models.CASCADE) # jak wyżej, tylko usuwa komentarz gdy zadanie zostanie usuniete
    value = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)