from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

# Create your models here.

class Todo(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    is_done = models.BooleanField()
    peririty = models.IntegerField(default=1)
    user  = models.ForeignKey(User , on_delete=models.CASCADE , related_name='todo')


    class Meta:
        db_table = 'todos'
