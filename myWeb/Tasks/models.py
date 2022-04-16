from pickle import FALSE
from django.db import models
from datetime import datetime
from uuid import uuid4


# Create your models here.
class Account(models.Model):
    username        = models.CharField(max_length=20)
    password        = models.CharField(max_length=200)
    creation_date   = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.username
class Session(models.Model):
    session_id      = models.UUIDField(default=uuid4().hex, max_length=20, primary_key=True)
    account_id      = models.ForeignKey(Account, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.session_id} - {self.account_id}'

class Task(models.Model):
    account_id      = models.ForeignKey(Account, on_delete=models.CASCADE)
    task_text       = models.CharField(max_length=255)
    completed       = models.BooleanField(default=False)
    completion_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.task_text}'

    def changeTaskCompletionState(self):
        if not self.completed:
            self.completed = not self.completed

    def set_completion_date(self):
        self.completion_date = datetime.now()