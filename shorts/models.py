from django.db import models
from books.models import Book

class Short(models.Model):
    book = models.OneToOneField(Book, on_delete=models.CASCADE)
    title = models.CharField(max_length=50)
    share_count = models.IntegerField(default=0)
    book_visit_count = models.IntegerField(default=0)
    storage_url = models.URLField(max_length=1000)
    is_deleted = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)