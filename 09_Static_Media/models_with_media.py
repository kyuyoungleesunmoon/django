# 09: Blog 앱의 업데이트된 models.py (미디어 필드 추가)

from django.db import models
from django.contrib.auth.models import User
from django.utils.text import slugify
from PIL import Image
import os


class Post(models.Model):
    """블로그 포스트 모델 (미디어 필드 포함)"""
    
    title = models.CharField(
        max_length=200,
        verbose_name='제목',
        unique=True
    )
    slug = models.SlugField(
        unique=True,
        verbose_name='슬러그',
        blank=True
    )
    content = models.TextField(
        verbose_name='내용'
    )
    excerpt = models.CharField(
        max_length=300,
        blank=True,
        verbose_name='요약'
    )
    
    # 이미지 필드 추가
    image = models.ImageField(
        upload_to='blog/posts/%Y/%m/',  # 년/월 폴더로 자동 구성
        blank=True,
        null=True,
        verbose_name='대표 이미지'
    )
    
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='작성자',
        related_name='blog_posts'
    )
    
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='작성일'
    )
    updated_at = models.DateTimeField(
        auto_now=True,
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
        ordering = ['-created_at']
        verbose_name = '블로그 포스트'
        verbose_name_plural = '블로그 포스트'
        indexes = [
            models.Index(fields=['slug']),
            models.Index(fields=['-created_at']),
        ]
    
    def __str__(self):
        return self.title
    
    def save(self, *args, **kwargs):
        """저장 시 자동으로 slug 생성 및 이미지 최적화"""
        
        # slug 자동 생성
        if not self.slug:
            self.slug = slugify(self.title)
        
        super().save(*args, **kwargs)
        
        # 이미지 최적화 (저장 후에 수행)
        if self.image:
            try:
                img = Image.open(self.image.path)
                
                # 이미지 크기 제한 (최대 1000px)
                max_size = (1000, 1000)
                img.thumbnail(max_size, Image.Resampling.LANCZOS)
                
                # 이미지 품질 설정하여 저장
                img.save(self.image.path, quality=85, optimize=True)
            except Exception as e:
                print(f"이미지 최적화 실패: {e}")
    
    @property
    def get_image_url(self):
        """이미지 URL 또는 기본 이미지 반환"""
        if self.image:
            return self.image.url
        return '/static/blog/images/default-post.png'


class Comment(models.Model):
    """블로그 포스트에 대한 댓글 모델"""
    
    post = models.ForeignKey(
        Post,
        on_delete=models.CASCADE,
        related_name='comments',
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
    
    # 카테고리 아이콘 이미지
    icon = models.ImageField(
        upload_to='blog/category_icons/',
        blank=True,
        null=True,
        verbose_name='카테고리 아이콘'
    )
    
    class Meta:
        verbose_name = '카테고리'
        verbose_name_plural = '카테고리'
    
    def __str__(self):
        return self.name
