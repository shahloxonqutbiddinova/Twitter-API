from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone
import uuid


NEW, VERIFIED, DONE = ("new", "verified", "done")

class User(AbstractUser):
    status_choices = [
        {"new", "NEW"},
        {"verified", "VERIFIED"},
        {"done", "DONE"}
    ]
    phone = models.CharField(max_length=15, null=True, blank=True, unique=True)
    status = models.CharField(max_length=20, choices=status_choices, default=NEW)
    bio = models.TextField(null=True, blank=True)
    image = models.ImageField(upload_to="images/")

    def __str__(self):
        return self.username

    def save(self, *args, **kwargs):
        if not self.username:
            user_uuid = uuid.uuid4().split("-")[-1]
            username = f"username-{user_uuid}"
            self.username = username
        if not self.password:
            random_uuid = uuid.uuid4().split("-")[-1]
            password = f"password-{random_uuid}"
            self.password = password
        super().save(*args, **kwargs)

class UserConfirmation(models.Model):
    code = models.CharField(max_length=6)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='confirmation')
    expired_at = models.DateTimeField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        self.expired_at = timezone.now()+timezone.timedelta(minutes=2)
        super().save(*args, **kwargs)

    def is_expired(self):
        return self.expired_at < timezone.now()


