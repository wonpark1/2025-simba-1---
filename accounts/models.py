from django.db import models
from django.contrib.auth.models import User

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    nickname = models.TextField(max_length=10, default='unknown')
    email = models.EmailField(null=True, blank=True)

    GENDER_CHOICES = [
        ('M', '남성'),
        ('F', '여성'),
    ]
    gender = models.CharField(
        max_length=1,
        choices=GENDER_CHOICES,
        default='F',  # 기본값을 여성으로 설정
    )

    def __str__(self):
        return self.nickname