# -*- coding: utf-8 -*-
"""
테스트 데이터 생성 스크립트
인코딩 문제 방지를 위해 UTF-8로 저장
"""

from django.contrib.auth.models import User
from blog.models import Category, Tag, Post

# 기존 데이터 확인
existing_categories = Category.objects.count()
existing_tags = Tag.objects.count()
existing_posts = Post.objects.count()

print(f'[기존 데이터]')
print(f'카테고리: {existing_categories}개')
print(f'태그: {existing_tags}개')
print(f'포스트: {existing_posts}개')
print()

# 관리자 가져오기
try:
    admin = User.objects.get(username='admin')
    print('[확인] admin 사용자 존재')
except User.DoesNotExist:
    print('[오류] admin 사용자가 없습니다. 먼저 관리자를 생성하세요.')
    exit()

# 카테고리 생성 (중복 방지)
categories_to_create = [
    ('기술', '기술 관련 포스트'),
    ('일상', '일상 관련 포스트'),
    ('공부', '공부 관련 포스트'),
]

created_categories = 0
for name, desc in categories_to_create:
    cat, created = Category.objects.get_or_create(name=name, defaults={'description': desc})
    if created:
        created_categories += 1
        print(f'[생성] 카테고리: {name}')
    else:
        print(f'[존재] 카테고리: {name}')

# 태그 생성 (중복 방지)
tags_to_create = ['Django', 'Python', '웹개발', '백엔드']

created_tags = 0
for tag_name in tags_to_create:
    tag, created = Tag.objects.get_or_create(name=tag_name)
    if created:
        created_tags += 1
        print(f'[생성] 태그: {tag_name}')
    else:
        print(f'[존재] 태그: {tag_name}')

print()
print('[완료] 카테고리와 태그 준비 완료')
print(f'총 카테고리: {Category.objects.count()}개')
print(f'총 태그: {Tag.objects.count()}개')

# 포스트 생성 예제 (선택적)
# 필요시 주석 해제하여 실행
"""
tech = Category.objects.get(name='기술')
post = Post.objects.create(
    title='Django로 블로그 만들기',
    content='Django는 강력한 웹 프레임워크입니다.',
    author=admin,
    category=tech,
    published=True
)
post.tags.add(Tag.objects.get(name='Django'))
print('[생성] 포스트: Django로 블로그 만들기')
"""
