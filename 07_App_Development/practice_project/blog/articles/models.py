from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class Category(models.Model):
    """게시글 카테고리"""
    name = models.CharField(max_length=50, unique=True)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = '카테고리'
        verbose_name_plural = '카테고리들'
        ordering = ['name']
    
    def __str__(self):
        return self.name


class Article(models.Model):
    """블로그 게시글"""
    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='articles')
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True, related_name='articles')
    content = models.TextField()
    excerpt = models.CharField(max_length=200, blank=True, help_text="블로그 목록에 표시될 짧은 설명")
    
    # 메타 데이터
    view_count = models.IntegerField(default=0)
    is_published = models.BooleanField(default=False)
    published_at = models.DateTimeField(null=True, blank=True)
    
    # 타임스탐프
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = '게시글'
        verbose_name_plural = '게시글들'
        ordering = ['-published_at', '-created_at']
        indexes = [
            models.Index(fields=['-published_at']),
            models.Index(fields=['slug']),
        ]
    
    def __str__(self):
        return self.title
    
    def publish(self):
        """게시글 발행"""
        self.is_published = True
        self.published_at = timezone.now()
        self.save()
    
    def unpublish(self):
        """게시글 발행 취소"""
        self.is_published = False
        self.published_at = None
        self.save()
    
    @property
    def is_recent(self):
        """최근 게시글인지 확인 (7일 이내)"""
        from datetime import timedelta
        return timezone.now() - self.published_at < timedelta(days=7)


class Comment(models.Model):
    """게시글 댓글"""
    article = models.ForeignKey(Article, on_delete=models.CASCADE, related_name='comments')
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comments')
    content = models.TextField()
    
    is_approved = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = '댓글'
        verbose_name_plural = '댓글들'
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.author.username}의 댓글 - {self.article.title}"


class Tag(models.Model):
    """게시글 태그"""
    name = models.CharField(max_length=50, unique=True)
    articles = models.ManyToManyField(Article, related_name='tags', blank=True)
    
    class Meta:
        verbose_name = '태그'
        verbose_name_plural = '태그들'
        ordering = ['name']
    
    def __str__(self):
        return self.name
