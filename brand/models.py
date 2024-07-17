from django.db import models
from django.contrib.auth.models import User

class Brand(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    description = models.TextField()
    question_1 = models.TextField()
    question_2 = models.TextField()
    # Add more fields as needed

    def __str__(self):
        return self.name
