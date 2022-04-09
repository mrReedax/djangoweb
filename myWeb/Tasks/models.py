from pickle import FALSE
from django.db import models


# Create your models here.
class Account(models.Model):
    username        = models.CharField(max_length=20)
    password        = models.CharField(max_length=200)
    creation_date   = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.username

class Task(models.Model):
    account_id = models.ForeignKey(Account, on_delete=models.CASCADE)
    task_text = models.CharField(max_length=255)
    completed = models.BooleanField(default=False)

    def __str__(self):
        return self.task_text