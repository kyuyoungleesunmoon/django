#!/usr/bin/env python
"""
Django 모델 테스트 스크립트
모든 모델이 제대로 동작하는지 확인
"""

import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'simpleblog.settings')
django.setup()

from django.contrib.auth.models import User
from blog.models import Post, Comment, Category
from pages.models import Page, About, Contact

print("=" * 50)
print("Django 모델 테스트 시작")
print("=" * 50)

# 테스트 사용자 생성
user, created = User.objects.get_or_create(
    username='testuser',
    defaults={
        'email': 'test@example.com',
        'first_name': 'Test',
        'last_name': 'User'
    }
)
print(f"✓ 사용자 생성/조회: {user.username} (created={created})")

# 카테고리 생성
cat1, _ = Category.objects.get_or_create(
    name='Django',
    defaults={'description': 'Django 웹 프레임워크'}
)
cat2, _ = Category.objects.get_or_create(
    name='Python',
    defaults={'description': 'Python 프로그래밍'}
)
print(f"✓ 카테고리 생성: {cat1.name}, {cat2.name}")

# 포스트 생성
post1, _ = Post.objects.get_or_create(
    title='Django ORM 학습하기',
    defaults={
        'slug': 'django-orm-learning',
        'content': 'Django ORM은 데이터베이스를 객체지향적으로 다룰 수 있게 해주는 훌륭한 도구입니다.',
        'excerpt': 'Django ORM 기초 가이드',
        'author': user,
        'is_published': True,
        'views': 100
    }
)
print(f"✓ 포스트 생성: {post1.title}")

post2, _ = Post.objects.get_or_create(
    title='Django 템플릿 심화',
    defaults={
        'slug': 'django-template-advanced',
        'content': '장고 템플릿의 필터, 태그, 상속을 깊이있게 학습합니다.',
        'excerpt': '장고 템플릿 고급 기능',
        'author': user,
        'is_published': True,
        'views': 50
    }
)
print(f"✓ 포스트 생성: {post2.title}")

# 댓글 생성
comment1, _ = Comment.objects.get_or_create(
    post=post1,
    author='김철수',
    email='kim@example.com',
    defaults={
        'content': '좋은 포스트 감사합니다!',
        'is_approved': True
    }
)
print(f"✓ 댓글 생성: {comment1.author}")

# 페이지 생성
page1, _ = Page.objects.get_or_create(
    title='소개',
    defaults={
        'slug': 'about',
        'content': '우리 사이트에 오신 것을 환영합니다.',
        'is_active': True,
        'order': 1
    }
)
print(f"✓ 페이지 생성: {page1.title}")

# About 정보 생성
about, _ = About.objects.get_or_create(
    title='우리에 대해',
    defaults={
        'description': 'Django와 Python을 사랑하는 개발자들의 커뮤니티입니다.'
    }
)
print(f"✓ About 생성: {about.title}")

# Contact 정보 생성
contact, _ = Contact.objects.get_or_create(
    email='contact@example.com',
    defaults={
        'phone': '02-1234-5678',
        'address': '서울시 강남구'
    }
)
print(f"✓ Contact 생성: {contact.email}")

# 통계 출력
print("\n" + "=" * 50)
print("데이터 통계")
print("=" * 50)
print(f"총 사용자: {User.objects.count()}")
print(f"총 포스트: {Post.objects.count()}")
print(f"총 댓글: {Comment.objects.count()}")
print(f"총 카테고리: {Category.objects.count()}")
print(f"총 페이지: {Page.objects.count()}")

# 쿼리 테스트
print("\n" + "=" * 50)
print("ORM 쿼리 테스트")
print("=" * 50)

# 모든 포스트 출력
print("\n[발행된 포스트 목록]")
for post in Post.objects.filter(is_published=True):
    print(f"  - {post.title} (조회수: {post.views})")

# 포스트별 댓글 수
print("\n[포스트별 댓글 수]")
for post in Post.objects.all():
    comment_count = post.comments.count()
    print(f"  - {post.title}: {comment_count}개")

# 사용자별 포스트 수
print("\n[사용자별 포스트 수]")
for user_obj in User.objects.all():
    post_count = user_obj.blog_posts.count()
    if post_count > 0:
        print(f"  - {user_obj.username}: {post_count}개")

print("\n" + "=" * 50)
print("✅ 모든 모델 테스트 완료!")
print("=" * 50)
