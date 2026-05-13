from django.db import models

# Create your models here.
class User(models.Model):
    username = models.CharField(max_length=150, unique=True)
    # flaw A02 -> cryptographic failures: plaintext password (fix in views.py)
    password = models.CharField(max_length=255)
    
class Note(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    content = models.TextField()