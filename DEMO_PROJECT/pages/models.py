# 07-1: Pages 앱의 models.py

from django.db import models
from django.utils.text import slugify


class Page(models.Model):
    """정적 페이지 모델"""
    
    title = models.CharField(
        max_length=200,
        verbose_name='페이지 제목',
        unique=True
    )
    slug = models.SlugField(
        unique=True,
        verbose_name='슬러그',
        blank=True
    )
    content = models.TextField(
        verbose_name='페이지 내용'
    )
    is_active = models.BooleanField(
        default=True,
        verbose_name='활성화'
    )
    order = models.IntegerField(
        default=0,
        verbose_name='순서'
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='작성일'
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name='수정일'
    )
    
    class Meta:
        verbose_name = '페이지'
        verbose_name_plural = '페이지'
        ordering = ['order', 'title']
    
    def __str__(self):
        return self.title
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)


class About(models.Model):
    """About 페이지 정보"""
    
    title = models.CharField(
        max_length=200,
        verbose_name='제목'
    )
    description = models.TextField(
        verbose_name='설명'
    )
    image = models.ImageField(
        upload_to='about/',
        blank=True,
        verbose_name='이미지'
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name='수정일'
    )
    
    class Meta:
        verbose_name = 'About 페이지'
        verbose_name_plural = 'About 페이지'
    
    def __str__(self):
        return self.title


class Contact(models.Model):
    """Contact 페이지 정보"""
    
    email = models.EmailField(
        verbose_name='이메일'
    )
    phone = models.CharField(
        max_length=20,
        verbose_name='전화번호'
    )
    address = models.TextField(
        verbose_name='주소'
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name='수정일'
    )
    
    class Meta:
        verbose_name = 'Contact 페이지'
        verbose_name_plural = 'Contact 페이지'
    
    def __str__(self):
        return f"Contact: {self.email}"

