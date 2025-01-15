from django.db import models
from shorts.models import Short
from users.models import User

class TodaysShorts(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)   # 사용자 ID
    book_id = models.ForeignKey(Short, on_delete=models.CASCADE)   # 책 ID
    is_deleted = models.BooleanField(default=False)  # 삭제 여부
    created_at = models.DateTimeField(auto_now_add=True)  # 생성 시간

    def __str__(self):
        return f"Today's Shorts {self.id} - User {self.user_id}" # 가독성을 위해 추가
