from django.db import models

# 여기에 모델을 정의하세요 (07단계에서 자세히 배웁니다)
class Message(models.Model):
    """학습용 메시지 모델"""
    title = models.CharField(max_length=100)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = "메시지"
        verbose_name_plural = "메시지들"
        ordering = ['-created_at']
    
    def __str__(self):
        return self.title
