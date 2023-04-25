from django.db import models

class MetaData(models.Model):
    filename_prefix = models.CharField(max_length=255)
    date = models.DateTimeField(auto_now_add=True)
    num_files = models.PositiveIntegerField()
