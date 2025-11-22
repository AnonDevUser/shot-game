from django.db import models

# Create your models here
class Question(models.Model):
    human = models.TextField()  
    options = models.JSONField()  
    correct_option_index = models.IntegerField()  # 0–3
    created_at = models.DateTimeField(auto_now_add=True)


    source = models.CharField(max_length=20, default="LLM")
    difficulty = models.CharField(max_length=20, default="medium")

    def __str__(self):
        return f"Question {self.id}"

class Player(models.Model):
    username = models.CharField(max_length=100, unique=True)
    score = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.username

