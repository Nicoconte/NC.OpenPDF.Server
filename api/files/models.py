from django.db import models

from django.contrib.auth.models import User

from datetime import datetime

# Create your models here.
class File(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    filename = models.CharField(max_length=100)
    path = models.CharField(max_length=100)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"ID { self.id } | Usuario { self.user.username } | Archivo { self.filename }"


