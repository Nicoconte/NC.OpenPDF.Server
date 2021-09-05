from django.contrib.auth.models import User

from django.db import models

# Create your models here.
class DiskSpace(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    limit = models.IntegerField(default=500)
    space_used = models.IntegerField(default=0)     


    def __str__(self):
        return f"User {self.user.username} | Space used {self.space_used} mb | Remaining {self.limit - self.space_used} mb"