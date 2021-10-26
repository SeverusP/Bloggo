from django.contrib.auth.models import AbstractUser
from django.db import models
from django.conf import settings
from django.utils import timezone


class User(AbstractUser):
    pass
    ip = models.GenericIPAddressField(null=True)

class Post(models.Model):
    user =  models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    title = models.CharField(max_length=200, default="", editable=True)
    datetime = models.DateTimeField(auto_now_add=True)
    created_date = models.DateTimeField(default=timezone.now)
    content = models.TextField()
    published_date = models.DateTimeField(blank=True, null=True)
    def publish(self):
        self.published_date = timezone.now()
        self.save()

    def __str__(self):
        return self.title
