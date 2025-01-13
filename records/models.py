from django.db import models
from users.models import User 
from books.models import Book

class Record(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)  
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    is_deleted = models.BooleanField(default=False)  
    created_at = models.DateTimeField(auto_now_add=True) 

    def __str__(self):
        return f"Record({self.user.name} - {self.book.title})"

