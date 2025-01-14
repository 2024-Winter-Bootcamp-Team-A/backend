from django.db import models
from users.models import User
from books.models import Book

class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE) 
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name='comments') 
    content = models.CharField(max_length=200) 
    is_deleted = models.BooleanField(default=False)  
    created_at = models.DateTimeField(auto_now_add=True)  
    updated_at = models.DateTimeField(auto_now=True)  

    def __str__(self):
        return f"Comment by {self.user.name} on {self.book.title}"

