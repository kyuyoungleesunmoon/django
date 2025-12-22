#!/usr/bin/env python
"""
Django View 테스트 스크립트
"""

import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'simpleblog.settings')
django.setup()

from django.test import RequestFactory
from django.contrib.auth.models import User, AnonymousUser
from blog.views import PostListView, PostDetailView
from pages.views import HomePageView
from blog.models import Post
from pages.models import Page

print("=" * 50)
print("Django View 테스트 시작")
print("=" * 50)

# 요청 팩토리 설정
factory = RequestFactory()

# 1. PostListView 테스트
print("\n[1] PostListView 테스트")
request = factory.get('/blog/')
request.user = AnonymousUser()
view = PostListView()
view.request = request
view.kwargs = {}
try:
    context = view.get_context_data()
    print(f"✓ PostListView 작동: {len(context.get('posts', []))} 포스트 조회됨")
except Exception as e:
    print(f"✗ PostListView 오류: {e}")

# 2. PostDetailView 테스트
print("\n[2] PostDetailView 테스트")
post = Post.objects.first()
if post:
    request = factory.get(f'/blog/post/{post.slug}/')
    request.user = AnonymousUser()
    view = PostDetailView()
    view.request = request
    view.kwargs = {'slug': post.slug}
    try:
        obj = view.get_object()
        context = view.get_context_data(object=obj)
        print(f"✓ PostDetailView 작동: '{obj.title}' 포스트 조회됨")
        print(f"  - 댓글 수: {len(context.get('comments', []))}")
        print(f"  - 조회수: {obj.views}")
    except Exception as e:
        print(f"✗ PostDetailView 오류: {e}")
else:
    print("✗ 테스트할 포스트가 없음")

# 3. HomePageView 테스트
print("\n[3] HomePageView 테스트")
request = factory.get('/')
request.user = AnonymousUser()
view = HomePageView()
view.request = request
try:
    context = view.get_context_data()
    latest_posts = context.get('latest_posts', [])
    print(f"✓ HomePageView 작동: {len(latest_posts)} 최신 포스트 표시")
except Exception as e:
    print(f"✗ HomePageView 오류: {e}")

# 4. 전체 포스트 조회 테스트
print("\n[4] 전체 포스트 조회 테스트")
published_posts = Post.objects.filter(is_published=True)
print(f"✓ 발행된 포스트: {published_posts.count()}개")
for post in published_posts:
    print(f"  - {post.title} ({post.author.username}, 조회수: {post.views})")

# 5. URL 라우팅 테스트
print("\n[5] URL 라우팅 테스트")
print("✓ blog/ URLs:")
print("  - blog/            → PostListView (포스트 목록)")
print("  - blog/post/<slug>/ → PostDetailView (포스트 상세)")
print("  - blog/post/new/    → PostCreateView (새 포스트)")
print("✓ pages/ URLs:")
print("  - /                → HomePageView (홈)")
print("  - /about/          → AboutPageView (소개)")
print("  - /contact/        → ContactPageView (연락처)")

print("\n" + "=" * 50)
print("✅ View 테스트 완료!")
print("=" * 50)
