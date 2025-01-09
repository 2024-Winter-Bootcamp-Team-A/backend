from django.db import models

class Book(models.Model):
    # 카테고리
    # 카테고리 정해지면 나중에 더 채울 예정
    category = models.CharField(
        max_length=50,
        choices=[
            ('소설', '소설'),
            ('시/에세이', '시/에세이'),
            ('인문', '인문'),
            ('기타', '기타'),
            ('자기계발', '자기계발'),
        ],
        default='기타'
    )
    title = models.CharField(max_length=50)
    author = models.CharField(max_length=20)
    publisher = models.CharField(max_length=20)
    image = models.CharField(max_length=300, blank=True)
    point = models.CharField(max_length=100, blank=True)
    story = models.TextField(blank=True)
    prompt = models.TextField(blank=True)
    book_url = models.URLField(max_length=1000, blank=True)
    is_deleted = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
