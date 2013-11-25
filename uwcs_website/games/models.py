from django.db import models

class Game(models.Model):
    name = models.CharField(max_length=255)
    version = models.CharField(max_length=255)
    maintainer = models.CharField(max_length=255)
    description = models.TextField()
    download = models.CharField(max_length=255)
    run = models.CharField(max_length=255)
    remove = models.CharField(max_length=255)

