from django.db import models
from uuid import uuid4

class MetaData(models.Model):
    id = models.UUIDField(default=uuid4, editable=False, primary_key=True)
    num_files = models.IntegerField(default=0)  # Provide a default value
    created_at = models.DateTimeField(auto_now_add=True)
