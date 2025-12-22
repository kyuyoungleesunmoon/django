from django.db import models
from django.contrib.auth.models import User

class Article(models.Model):
    PRIORITY_CHOICES = [
        ('high', '높음'),
        ('medium', '보통'),
        ('low', '낮음'),
    ]
    
    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    summary = models.CharField(max_length=200, blank=True)
    
    priority = models.CharField(max_length=10, choices=PRIORITY_CHOICES, default='medium')
    view_count = models.IntegerField(default=0)
    is_featured = models.BooleanField(default=False)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return self.title
    
    @property
    def word_count(self):
        """단어 수"""
        return len(self.content.split())
    
    @property
    def reading_time(self):
        """읽는 시간 (분)"""
        return max(1, self.word_count // 200)
