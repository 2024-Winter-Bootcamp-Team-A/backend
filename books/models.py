from django.db import models

class Book(models.Model):

    title = models.CharField(max_length=200)
    author = models.CharField(max_length=100)
    publisher = models.CharField(max_length=100)
    category = models.CharField(max_length=50)
    image = models.CharField(max_length=300, blank=True)
    story = models.TextField(blank=True)
    point = models.CharField(max_length=100, blank=True)
    prompt = models.TextField(blank=True)
    book_url = models.URLField(max_length=1000, blank=True)
    is_deleted = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
