from django.db import models

class Dataset(models.Model):
    filename = models.CharField(max_length=255)
    date = models.DateTimeField()

    def __str__(self):
        return f"{self.filename} ({self.date})"
