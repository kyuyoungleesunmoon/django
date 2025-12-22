# 07 레벨 - Django 앱 개발 및 데이터베이스

## 목차
1. Django 앱의 개념과 구조
2. 모델(Model) 상세 학습
3. 데이터베이스와 ORM
4. 마이그레이션(Migration)
5. 쿼리셋(QuerySet) API
6. 관계형 필드
7. 실전 모델 작성 가이드

---

## 1. Django 앱의 개념과 구조

### 1.1 프로젝트 vs 앱
Django에서는 **프로젝트(Project)**와 **앱(App)**을 구분합니다.

- **프로젝트**: 전체 웹사이트. 여러 앱을 포함하는 컨테이너
- **앱**: 특정 기능을 담당하는 모듈. 예: 블로그, 사용자 관리, 댓글 기능

```
simpleblog (프로젝트)
├── blog (앱: 블로그 관련)
│   ├── models.py       # 데이터 모델
│   ├── views.py        # 비즈니스 로직
│   ├── urls.py         # URL 라우팅
│   ├── forms.py        # 입력 양식
│   ├── admin.py        # 관리자 인터페이스
│   └── tests.py        # 테스트 코드
├── pages (앱: 페이지 관련)
│   ├── models.py
│   ├── views.py
│   └── ...
├── simpleblog (프로젝트 설정)
│   ├── settings.py     # 전역 설정
│   ├── urls.py         # 메인 URL 설정
│   └── wsgi.py         # 웹 서버 진입점
└── manage.py          # Django 관리 도구
```

### 1.2 앱 생성 절차

```bash
# 1. 앱 생성
python manage.py startapp blog

# 2. INSTALLED_APPS에 등록 (settings.py)
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'blog',  # <- 여기에 추가
    'pages',
]

# 3. 모델 정의 (blog/models.py)
# 4. 마이그레이션 생성 및 적용
python manage.py makemigrations
python manage.py migrate
```

---

## 2. 모델(Model) 상세 학습

### 2.1 모델이란?
모델은 데이터의 **구조를 정의**하는 Python 클래스입니다. 각 모델은 데이터베이스의 **한 개의 테이블**에 대응됩니다.

### 2.2 기본 모델 구조

```python
from django.db import models
from django.contrib.auth.models import User

class Post(models.Model):
    """블로그 포스트 모델"""
    
    # 필드 정의
    title = models.CharField(max_length=200)
    content = models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        # 메타 옵션 (테이블 이름, 정렬 등)
        verbose_name = '블로그 포스트'
        ordering = ['-created_at']
    
    def __str__(self):
        # 모델의 문자열 표현
        return self.title
    
    def save(self, *args, **kwargs):
        # 저장 전 처리
        super().save(*args, **kwargs)
```

### 2.3 필드 타입

#### 주요 필드
| 필드 타입 | 설명 | 데이터베이스 타입 |
|---------|------|----------------|
| `CharField` | 짧은 텍스트 (최대길이 필수) | VARCHAR |
| `TextField` | 긴 텍스트 | TEXT |
| `IntegerField` | 정수 | INTEGER |
| `FloatField` | 실수 | FLOAT |
| `DecimalField` | 정확한 소수 | DECIMAL |
| `BooleanField` | 참/거짓 | BOOLEAN |
| `DateField` | 날짜 (YYYY-MM-DD) | DATE |
| `TimeField` | 시간 (HH:MM:SS) | TIME |
| `DateTimeField` | 날짜+시간 | DATETIME |
| `EmailField` | 이메일 주소 | VARCHAR (검증 포함) |
| `URLField` | URL | VARCHAR (검증 포함) |
| `FileField` | 파일 업로드 | VARCHAR (경로 저장) |
| `ImageField` | 이미지 파일 | VARCHAR (Pillow 필요) |

### 2.4 필드 옵션

```python
class Post(models.Model):
    # verbose_name: 관리자 인터페이스에서 표시될 이름
    title = models.CharField(max_length=200, verbose_name='제목')
    
    # null: 데이터베이스에 NULL 허용 (기본값: False)
    # blank: 폼에서 빈 값 허용 (기본값: False)
    excerpt = models.CharField(max_length=300, null=True, blank=True)
    
    # default: 기본값
    is_published = models.BooleanField(default=False)
    
    # unique: 중복되지 않는 값 (같은 값이 두 개 이상 불가)
    slug = models.SlugField(unique=True)
    
    # help_text: 폼에서 도움말 표시
    views = models.IntegerField(default=0, help_text='조회수')
    
    # db_index: 데이터베이스 인덱스 생성 (검색 성능 향상)
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)
    
    # auto_now_add: 생성 시에만 현재 시간 저장
    # auto_now: 저장할 때마다 현재 시간으로 업데이트
    updated_at = models.DateTimeField(auto_now=True)
```

### 2.5 관계형 필드

#### ForeignKey (일대다 관계)
```python
class Comment(models.Model):
    """포스트에 달린 댓글"""
    post = models.ForeignKey(
        Post,                      # 관련된 모델
        on_delete=models.CASCADE,  # 포스트 삭제 시 댓글도 삭제
        related_name='comments'    # 역방향 접근: post.comments.all()
    )
    content = models.TextField()

# 사용 예
post = Post.objects.get(id=1)
comments = post.comments.all()  # 역방향 접근
```

#### ManyToMany (다대다 관계)
```python
class Post(models.Model):
    categories = models.ManyToManyField(
        'Category',
        related_name='posts'
    )

# 사용 예
post.categories.add(category1, category2)
post.categories.all()  # 모든 카테고리
```

#### OneToOne (일대일 관계)
```python
class UserProfile(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        primary_key=True
    )

# 사용 예
profile = user.userprofile
```

---

## 3. 데이터베이스와 ORM

### 3.1 ORM(Object-Relational Mapping)이란?
ORM은 **객체와 데이터베이스의 데이터를 매핑**하는 기술입니다.

```
Python 객체 ←→ ORM (Django) ←→ SQL ←→ 데이터베이스
```

### 3.2 Django ORM의 장점
- SQL을 직접 쓸 필요 없음
- 데이터베이스 변경이 쉬움 (SQLite → PostgreSQL)
- 보안성 높음 (SQL Injection 방지)
- Python다운 객체지향 코드

### 3.3 쿼리셋(QuerySet)

쿼리셋은 데이터베이스에서 **여러 개의 객체**를 가져오는 방식입니다.

```python
# 모든 포스트 조회
posts = Post.objects.all()

# 조건에 맞는 포스트 조회
published = Post.objects.filter(is_published=True)

# 하나의 포스트만 조회
post = Post.objects.get(id=1)

# 첫 번째 포스트 조회
first_post = Post.objects.first()

# 마지막 포스트 조회
last_post = Post.objects.last()

# 개수 세기
count = Post.objects.count()

# 존재 여부 확인
exists = Post.objects.filter(title='Django').exists()
```

---

## 4. 마이그레이션(Migration)

### 4.1 마이그레이션이란?
마이그레이션은 **모델 변화를 데이터베이스에 적용**하는 방법입니다.

### 4.2 마이그레이션 절차

```bash
# 1단계: 마이그레이션 파일 생성
python manage.py makemigrations
# 결과: blog/migrations/0001_initial.py 생성

# 2단계: 마이그레이션 내용 확인
python manage.py sqlmigrate blog 0001
# 결과: 생성될 SQL 쿼리 출력

# 3단계: 마이그레이션 적용
python manage.py migrate
# 결과: 데이터베이스에 테이블 생성

# 4단계: 마이그레이션 상태 확인
python manage.py showmigrations
```

### 4.3 일반적인 마이그레이션 시나리오

```python
# 1. 필드 추가
class Post(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    featured = models.BooleanField(default=False)  # 새로운 필드

# 명령어: makemigrations → migrate

# 2. 필드 삭제
# featured 필드 제거

# 3. 필드 이름 변경
# 필드명 변경 후 askname 옵션 사용

# 4. 필드 속성 변경
title = models.CharField(max_length=300)  # 200 → 300
```

---

## 5. 쿼리셋(QuerySet) API

### 5.1 생성(Create)
```python
# 방법 1: 객체 생성 후 저장
post = Post(title='Django ORM', content='매우 유용합니다')
post.save()

# 방법 2: create() 메서드
post = Post.objects.create(
    title='Django ORM',
    content='매우 유용합니다',
    author=request.user
)

# 방법 3: get_or_create() - 있으면 가져오고, 없으면 생성
post, created = Post.objects.get_or_create(
    title='Django ORM',
    defaults={'content': '매우 유용합니다'}
)
```

### 5.2 조회(Read)
```python
# 모든 객체 조회
all_posts = Post.objects.all()

# 필터링
published = Post.objects.filter(is_published=True)
recent = Post.objects.filter(created_at__gte='2024-01-01')

# 제외
unpublished = Post.objects.exclude(is_published=True)

# 하나만 조회
post = Post.objects.get(id=1)
post = Post.objects.get(slug='django-orm')

# 첫 번째/마지막
first = Post.objects.first()
last = Post.objects.last()

# 개수
count = Post.objects.count()

# 존재 여부
exists = Post.objects.filter(title='Django').exists()
```

### 5.3 수정(Update)
```python
# 방법 1: 객체 수정
post = Post.objects.get(id=1)
post.title = '수정된 제목'
post.save()

# 방법 2: 일괄 수정
Post.objects.filter(is_published=False).update(is_published=True)

# 값 증가
post.views += 1
post.save()

# 또는
Post.objects.filter(id=1).update(views=F('views') + 1)
```

### 5.4 삭제(Delete)
```python
# 방법 1: 개별 삭제
post = Post.objects.get(id=1)
post.delete()

# 방법 2: 조건부 삭제
Post.objects.filter(is_published=False).delete()

# 모든 객체 삭제 (주의!)
Post.objects.all().delete()
```

### 5.5 고급 쿼리

#### 정렬
```python
# 오름차순
posts = Post.objects.order_by('created_at')

# 내림차순 (- 붙이기)
posts = Post.objects.order_by('-created_at')

# 여러 필드로 정렬
posts = Post.objects.order_by('author', '-created_at')
```

#### 슬라이싱
```python
# 처음 10개
first_10 = Post.objects.all()[:10]

# 11번째부터 20번째
posts = Post.objects.all()[10:20]
```

#### 필드 제한
```python
# 특정 필드만 가져오기
titles = Post.objects.values_list('title', flat=True)

# 딕셔너리 형태로 가져오기
post_dicts = Post.objects.values('id', 'title', 'author')
```

---

## 6. 실전 예제

### 6.1 사용자별 포스트 수 계산
```python
from django.db.models import Count

# 각 사용자별 포스트 수
user_post_counts = (
    Post.objects.values('author__username')
    .annotate(post_count=Count('id'))
)
# 결과: [{'author__username': 'john', 'post_count': 5}, ...]
```

### 6.2 최근 7일 포스트
```python
from datetime import datetime, timedelta

last_week = datetime.now() - timedelta(days=7)
recent_posts = Post.objects.filter(created_at__gte=last_week)
```

### 6.3 발행된 포스트 중 조회수 100 이상
```python
popular = Post.objects.filter(
    is_published=True,
    views__gte=100
).order_by('-views')
```

---

## 요약

| 개념 | 설명 |
|-----|------|
| **모델** | 데이터 구조 정의 (테이블) |
| **필드** | 모델의 속성 (컬럼) |
| **마이그레이션** | 모델 변화를 DB에 적용 |
| **쿼리셋** | 데이터베이스 쿼리 (ORM) |
| **ORM** | 객체와 DB 데이터 매핑 |

다음 레벨: **08 - 웹페이지 (URLs와 Views)**
