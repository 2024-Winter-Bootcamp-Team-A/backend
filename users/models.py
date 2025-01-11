from django.db import models

class User(models.Model):
    GENDER_CHOICES = [
        (0, '남자'),
        (1, '여자'),
    ]
    name = models.CharField(max_length=10)
    email = models.EmailField(unique=True, max_length=20)
    password = models.CharField(max_length=20)
    sex = models.IntegerField(choices=GENDER_CHOICES, null=True, blank=True)
    age = models.IntegerField(null=True, blank=True)
    is_deleted = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    def __str__(self):
        return self.name