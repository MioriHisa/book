from django.db import models
from django.contrib.auth.models import User
import datetime

class BookReserve(models.Model):
    title = models.CharField("書籍名", max_length=60)
    author = models.CharField("著者", max_length=60)
    publication_date = models.DateField("出版日", default=datetime.date.today)
    picture = models.ImageField(upload_to='images/', default='')
    reservation_availability = models.BooleanField("予約可否", default=True,)
    reserver = models.CharField("予約者", max_length=30, blank=True, null=True)
    return_date = models.DateField("返却日", blank=True, null=True)

    def __str__(self):
        return self.title

class BookRequest(models.Model):
    # ユーザーが入力する情報
    title = models.CharField(max_length=200, verbose_name="書籍タイトル")
    author = models.CharField(max_length=100, verbose_name="著者名")
    url = models.URLField(max_length=200, blank=True, null=True, verbose_name="商品URL") # リクエストにのみ存在
    
    # 管理者が使用する情報
    requested_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="リクエスト者") 
    
    # リクエストのステータス
    STATUS_CHOICES = [
        ('Pending', '処理中'),
        ('Approved', '承認済み'),
        ('Rejected', '却下'),
    ]
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='Pending', verbose_name="ステータス")
    requested_at = models.DateTimeField(auto_now_add=True, verbose_name="リクエスト日時")
    
    def __str__(self):
        return f"リクエスト: {self.title} (Status: {self.status})"

    class Meta:
        verbose_name = "書籍リクエスト"
        verbose_name_plural = "書籍リクエスト"
        ordering = ['-requested_at']
