# 07-1: Blog 앱의 models.py

from django.db import models
from django.contrib.auth.models import User
from django.utils.text import slugify

class Post(models.Model):
    """블로그 포스트 모델"""
    
    # 필드 정의
    title = models.CharField(
        max_length=200,
        verbose_name='제목',
        unique=True
    )
    slug = models.SlugField(
        unique=True,
        verbose_name='슬러그',
        blank=True  # 자동으로 생성됨
    )
    content = models.TextField(
        verbose_name='내용'
    )
    excerpt = models.CharField(
        max_length=300,
        blank=True,
        verbose_name='요약'
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='작성자',
        related_name='blog_posts'  # 역방향 접근: user.blog_posts.all()
    )
    created_at = models.DateTimeField(
        auto_now_add=True,  # 생성 시에만 현재 시간으로 설정
        verbose_name='작성일'
    )
    updated_at = models.DateTimeField(
        auto_now=True,  # 수정할 때마다 현재 시간으로 업데이트
        verbose_name='수정일'
    )
    is_published = models.BooleanField(
        default=False,
        verbose_name='발행됨'
    )
    views = models.IntegerField(
        default=0,
        verbose_name='조회수'
    )
    
    class Meta:
        ordering = ['-created_at']  # 최신순 정렬
        verbose_name = '블로그 포스트'
        verbose_name_plural = '블로그 포스트'
        indexes = [
            models.Index(fields=['slug']),
            models.Index(fields=['-created_at']),
        ]
    
    def __str__(self):
        """모델의 문자열 표현"""
        return self.title
    
    def save(self, *args, **kwargs):
        """저장 시 자동으로 slug 생성"""
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)


class Comment(models.Model):
    """블로그 포스트에 대한 댓글 모델"""
    
    post = models.ForeignKey(
        Post,
        on_delete=models.CASCADE,
        related_name='comments',  # 역방향 접근: post.comments.all()
        verbose_name='포스트'
    )
    author = models.CharField(
        max_length=100,
        verbose_name='댓글 작성자'
    )
    email = models.EmailField(
        verbose_name='이메일'
    )
    content = models.TextField(
        verbose_name='댓글 내용'
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='작성일'
    )
    is_approved = models.BooleanField(
        default=True,
        verbose_name='승인됨'
    )
    
    class Meta:
        ordering = ['created_at']
        verbose_name = '댓글'
        verbose_name_plural = '댓글'
    
    def __str__(self):
        return f"{self.author}의 댓글: {self.post.title}"


class Category(models.Model):
    """블로그 카테고리 모델"""
    
    name = models.CharField(
        max_length=50,
        unique=True,
        verbose_name='카테고리명'
    )
    slug = models.SlugField(
        unique=True,
        verbose_name='슬러그'
    )
    description = models.TextField(
        blank=True,
        verbose_name='설명'
    )
    
    class Meta:
        verbose_name = '카테고리'
        verbose_name_plural = '카테고리'
    
    def __str__(self):
        return self.name
