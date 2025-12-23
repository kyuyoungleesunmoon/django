# Django 블로그 프로젝트 - 단계별 학습 가이드

## 개요
이 튜토리얼은 Django 블로그 애플리케이션을 처음부터 끝까지 만드는 과정을 안내합니다. 각 단계는 이전 단계를 기반으로 하며, 전체 프로젝트를 점진적으로 이해하고 구현할 수 있습니다.

**최종 결과:** 포스트, 댓글, 좋아요, 북마크, 카테고리, 태그 기능을 갖춘 완전한 블로그

**예상 소요 시간:** 4-6시간

---

## 목차

1. [1단계: 환경 설정](#1단계-환경-설정)
2. [2단계: Django 프로젝트 생성](#2단계-django-프로젝트-생성)
3. [3단계: 블로그 앱 생성](#3단계-블로그-앱-생성)
4. [4단계: 모델 설계 및 생성](#4단계-모델-설계-및-생성)
5. [5단계: Admin 패널 설정](#5단계-admin-패널-설정)
6. [6단계: URL 라우팅 설정](#6단계-url-라우팅-설정)
7. [7단계: 뷰 작성](#7단계-뷰-작성)
8. [8단계: 템플릿 작성](#8단계-템플릿-작성)
9. [9단계: 폼 작성](#9단계-폼-작성)
10. [10단계: 테스트 및 마무리](#10단계-테스트-및-마무리)

---

## 학습 방법

### 권장 학습 순서
1. 각 단계를 순서대로 진행
2. 코드를 직접 타이핑 (복사 붙여넣기 지양)
3. 각 단계마다 서버를 실행해서 결과 확인
4. 체크포인트에서 스스로 점검

### 실습 팁
- 에러가 나면 메시지를 천천히 읽어보기
- 이해가 안 되면 해당 부분을 다시 읽기
- 각 코드 블록의 "코드 이해하기" 참고

---

## 1단계: 환경 설정

### 배울 내용
- Django 설치
- 가상 환경 이해
- 개발 환경 준비

### 이론
Django는 빠른 개발을 지원하는 고수준 Python 웹 프레임워크입니다. 시작하기 전에 Python이 설치되어 있어야 하며, 프로젝트 종속성을 격리하기 위해 가상 환경을 만들어야 합니다.

### 실습

**1.1 Python 설치 확인**
```powershell
python --version
# Python 3.8 이상이어야 함
```

**1.2 Django 설치**
```powershell
pip install django==4.2.8
```

**1.3 설치 확인**
```powershell
python -m django --version
# 4.2.8 출력되어야 함
```

### 체크포인트
- [ ] Python 3.8+ 설치됨
- [ ] Django 4.2.8 설치됨
- [ ] 버전 확인 성공

**다음:** Django 프로젝트 생성

---

## 2단계: Django 프로젝트 생성

### 배울 내용
- Django 프로젝트 구조
- 프로젝트와 앱의 차이
- 기본 프로젝트 설정

### 이론
Django **프로젝트**는 설정과 앱의 모음입니다. **앱**은 특정 기능을 수행하는 모듈입니다(예: 블로그). 하나의 프로젝트는 여러 앱을 가질 수 있습니다.

### 실습

**2.1 프로젝트 디렉토리 생성**
```powershell
mkdir DJangGo
cd DJangGo
```

**2.2 Django 프로젝트 생성**
```powershell
django-admin startproject myproject .
```

**주의:** 마지막 점(.)은 현재 디렉토리에 프로젝트를 생성합니다.

**2.3 프로젝트 구조 이해**
```
DJangGo/
├── manage.py          # 명령줄 유틸리티
└── myproject/         # 프로젝트 패키지
    ├── __init__.py    # Python 패키지 마커
    ├── settings.py    # 프로젝트 설정
    ├── urls.py        # URL 선언
    └── wsgi.py        # 웹 서버 게이트웨이
```

**2.4 프로젝트 테스트**
```powershell
python manage.py runserver
```

http://127.0.0.1:8000/ 방문 - Django 환영 페이지가 보여야 합니다!

**2.5 서버 중지**
터미널에서 `Ctrl+C` 누르기

### 체크포인트
- [ ] 프로젝트 생성 성공
- [ ] 서버 실행 오류 없음
- [ ] 환영 페이지 표시됨

**다음:** 블로그 애플리케이션 생성

---

## 3단계: 블로그 앱 생성

### 배울 내용
- Django 앱 생성
- settings에 앱 등록
- 앱 구조

### 이론
앱은 Django 프로젝트의 모듈식 구성 요소입니다. 각 앱은 한 가지 일을 잘 수행해야 합니다. 우리의 블로그 앱은 모든 블로그 관련 기능을 처리합니다.

### 실습

**3.1 블로그 앱 생성**
```powershell
python manage.py startapp blog
```

**3.2 생성된 앱 구조**
```
blog/
├── __init__.py
├── admin.py       # Admin 설정
├── apps.py        # 앱 설정
├── models.py      # 데이터 모델
├── tests.py       # 테스트
├── views.py       # 뷰 함수
└── migrations/    # 데이터베이스 마이그레이션
```

**3.3 settings에 앱 등록**

`myproject/settings.py` 파일을 열고 INSTALLED_APPS에 'blog' 추가:

```python
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'blog',  # 이 줄 추가
]
```

**3.4 템플릿 디렉토리 설정**

같은 파일에서 TEMPLATES를 찾아 DIRS 업데이트:

```python
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],  # 이 부분 추가
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]
```

### 체크포인트
- [ ] 블로그 앱 생성됨
- [ ] INSTALLED_APPS에 등록됨
- [ ] 템플릿 디렉토리 설정됨

**다음:** 데이터 모델 설계

---

## 4단계: 모델 설계 및 생성

### 배울 내용
- Django ORM (Object-Relational Mapping)
- 모델 필드와 관계
- 데이터베이스 마이그레이션

### 이론
모델은 데이터 구조를 정의합니다. 각 모델은 데이터베이스 테이블을 나타내는 Python 클래스입니다. Django의 ORM은 자동으로 모델을 데이터베이스 테이블로 변환합니다.

**핵심 개념:**
- **필드 타입:** CharField, TextField, DateTimeField 등
- **관계:** ForeignKey (다대일), ManyToManyField (다대다)
- **Meta 옵션:** ordering, verbose_name_plural 등

### 실습

**4.1 기본 모델 생성**

`blog/models.py` 파일을 열고 모든 내용을 다음으로 교체:

```python
from django.db import models
from django.contrib.auth.models import User


# 카테고리 모델
class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name_plural = "categories"
    
    def __str__(self):
        return self.name


# 태그 모델
class Tag(models.Model):
    name = models.CharField(max_length=50, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.name


# 포스트 모델
class Post(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='posts')
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True, related_name='posts')
    tags = models.ManyToManyField(Tag, related_name='posts', blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    published = models.BooleanField(default=True)
    views = models.IntegerField(default=0)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return self.title
```

**코드 이해하기:**

- `User`는 Django 인증 시스템에서 가져옴
- `CharField`: 짧은 텍스트용 (제목, 이름)
- `TextField`: 긴 텍스트용 (내용, 설명)
- `ForeignKey`: 일대다 관계
- `ManyToManyField`: 다대다 관계
- `auto_now_add=True`: 생성 시 현재 시간으로 설정
- `auto_now=True`: 저장할 때마다 업데이트
- `on_delete=models.CASCADE`: 작성자 삭제 시 포스트도 삭제
- `related_name`: 역방향 관계 이름

**4.2 마이그레이션 생성**
```powershell
python manage.py makemigrations
```

다음과 같이 표시되어야 합니다:
```
Migrations for 'blog':
  blog\migrations\0001_initial.py
    - Create model Category
    - Create model Tag
    - Create model Post
```

**4.3 마이그레이션 적용**
```powershell
python manage.py migrate
```

이것은 데이터베이스 테이블을 생성합니다.

**4.4 추가 모델 작성 (Comment, Like, Bookmark)**

`blog/models.py`에 추가:

```python
# 댓글 모델
class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comments')
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.author.username}'s comment"


# 좋아요 모델
class Like(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='likes')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='likes')
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ('post', 'user')
    
    def __str__(self):
        return f"{self.user.username} - {self.post.title}"


# 북마크 모델
class Bookmark(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='bookmarks')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='bookmarks')
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ('post', 'user')
    
    def __str__(self):
        return f"{self.user.username} - {self.post.title}"
```

**4.5 새 마이그레이션 생성 및 적용**
```powershell
python manage.py makemigrations
python manage.py migrate
```

### 체크포인트
- [ ] 6개 모델 모두 생성됨
- [ ] 마이그레이션 생성 및 적용됨
- [ ] 마이그레이션 중 오류 없음

**연습 문제:** 각 모델의 필드를 이해해보세요. `unique_together`는 무엇을 하나요?

**다음:** Admin 패널 설정

---

## 5단계: Admin 패널 설정

### 배울 내용
- Django admin 인터페이스
- 모델 등록
- Admin 표시 커스터마이징

### 이론
Django는 데이터 관리를 위한 내장 admin 인터페이스를 제공합니다. 모델을 등록하고 선택적으로 표시 방법을 커스터마이징해야 합니다.

### 실습

**5.1 슈퍼유저 생성**
```powershell
python manage.py createsuperuser
```

입력:
- Username: `admin`
- Email: `admin@example.com` (또는 Enter)
- Password: `admin123`
- Password (again): `admin123`

**5.2 Admin에 모델 등록**

`blog/admin.py` 파일을 열고 다음으로 교체:

```python
from django.contrib import admin
from .models import Category, Tag, Post, Comment, Like, Bookmark


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'created_at']
    search_fields = ['name']


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ['name', 'created_at']
    search_fields = ['name']


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ['title', 'author', 'category', 'views', 'published', 'created_at']
    list_filter = ['published', 'category', 'created_at']
    search_fields = ['title', 'author__username', 'content']
    filter_horizontal = ['tags']
    readonly_fields = ['created_at', 'updated_at', 'views']
    
    fieldsets = (
        ('기본 정보', {
            'fields': ('title', 'author', 'category')
        }),
        ('내용', {
            'fields': ('content', 'tags')
        }),
        ('상태', {
            'fields': ('published', 'views')
        }),
        ('날짜', {
            'fields': ('created_at', 'updated_at')
        }),
    )


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ['author', 'post', 'created_at']
    list_filter = ['created_at']
    search_fields = ['author__username', 'post__title', 'content']
    readonly_fields = ['created_at', 'updated_at']


@admin.register(Like)
class LikeAdmin(admin.ModelAdmin):
    list_display = ['user', 'post', 'created_at']
    list_filter = ['created_at']
    search_fields = ['user__username', 'post__title']


@admin.register(Bookmark)
class BookmarkAdmin(admin.ModelAdmin):
    list_display = ['user', 'post', 'created_at']
    list_filter = ['created_at']
    search_fields = ['user__username', 'post__title']
```

**코드 이해하기:**

- `@admin.register()`: 모델 등록 데코레이터
- `list_display`: 목록 뷰에 표시할 필드
- `list_filter`: 필터 사이드바 추가
- `search_fields`: 검색 활성화
- `filter_horizontal`: 다대다 관계 더 나은 UI
- `readonly_fields`: 편집 불가 필드
- `fieldsets`: 폼에서 필드 그룹화

**5.3 Admin 패널 테스트**

```powershell
python manage.py runserver
```

http://127.0.0.1:8000/admin/ 방문

로그인:
- Username: `admin`
- Password: `admin123`

모든 모델이 보여야 합니다!

**5.4 테스트 데이터 생성**

Admin 패널에서:

1. **카테고리 생성:**
   - "Categories" 클릭 → "Add Category"
   - Name: "Technology", Description: "Tech posts"
   - 2개 더 추가: "Tutorial", "Lifestyle"

2. **태그 생성:**
   - "Tags" 클릭 → "Add Tag"
   - 생성: "Django", "Python", "WebDev"

3. **포스트 생성:**
   - "Posts" 클릭 → "Add Post"
   - Title: "Getting Started with Django"
   - Content: "Django is a powerful web framework..."
   - Author: admin
   - Category: Technology
   - Tags: Django, Python
   - Published: ✓
   - "Save" 클릭

### 체크포인트
- [ ] 슈퍼유저 생성됨
- [ ] Admin 패널 접근 가능
- [ ] 모든 모델이 admin에 보임
- [ ] 테스트 데이터 생성됨

**다음:** URL 라우팅 설정

---

## 6단계: URL 라우팅 설정

### 배울 내용
- URL 패턴
- URL 네임스페이싱
- Path 변환기

### 이론
URL은 웹 주소를 뷰 함수에 연결합니다. Django는 URLconf를 사용하여 URL을 뷰에 매핑합니다.

### 실습

**6.1 블로그 URL 생성**

`blog/urls.py` 파일 생성:

```python
from django.urls import path
from . import views

app_name = 'blog'

urlpatterns = [
    # 포스트 URL
    path('', views.post_list, name='post_list'),
    path('post/<int:pk>/', views.post_detail, name='post_detail'),
    path('post/create/', views.PostCreateView.as_view(), name='post_create'),
    path('post/<int:pk>/edit/', views.PostUpdateView.as_view(), name='post_edit'),
    path('post/<int:pk>/delete/', views.PostDeleteView.as_view(), name='post_delete'),
    
    # 댓글 URL
    path('post/<int:pk>/comment/', views.add_comment, name='add_comment'),
    
    # 좋아요 & 북마크 URL
    path('post/<int:pk>/like/', views.toggle_like, name='toggle_like'),
    path('post/<int:pk>/bookmark/', views.toggle_bookmark, name='toggle_bookmark'),
    
    # 카테고리 & 검색 URL
    path('category/<int:pk>/', views.category_posts, name='category_posts'),
    path('search/', views.search, name='search'),
    
    # 대시보드 URL
    path('dashboard/', views.dashboard, name='dashboard'),
]
```

**6.2 프로젝트에 블로그 URL 포함**

`myproject/urls.py` 파일을 열고 업데이트:

```python
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('blog.urls')),  # 이 줄 추가
]
```

### 체크포인트
- [ ] blog/urls.py 생성됨
- [ ] 프로젝트에 URL 포함됨
- [ ] URL 패턴 정의됨

**주의:** 뷰가 아직 없어서 URL이 작동하지 않습니다. 괜찮습니다 - 다음에 만들겠습니다!

**다음:** 뷰 함수 작성

---

## 7단계부터는 영문 가이드 참조

7단계부터는 `STEP_BY_STEP_TUTORIAL.md` 파일을 참조하세요. 

코드는 동일하며, 설명이 영문으로 되어 있습니다.

---

## 빠른 참조

### 자주 사용하는 명령어

```powershell
# 서버 실행
python manage.py runserver

# 마이그레이션 생성
python manage.py makemigrations

# 마이그레이션 적용
python manage.py migrate

# 슈퍼유저 생성
python manage.py createsuperuser

# 앱 생성
python manage.py startapp <app_name>

# Python shell 실행
python manage.py shell
```

### 주요 파일 경로

```
DJangGo/
├── manage.py
├── myproject/
│   ├── settings.py      # 프로젝트 설정
│   └── urls.py          # 메인 URL
├── blog/
│   ├── models.py        # 데이터 모델
│   ├── views.py         # 뷰 로직
│   ├── urls.py          # 앱 URL
│   ├── admin.py         # Admin 설정
│   └── forms.py         # 폼
└── templates/blog/      # 템플릿
```

---

## 학습 체크리스트

### 기본 개념
- [ ] Django 프로젝트 vs 앱 이해
- [ ] MTV 패턴 이해
- [ ] ORM 개념 이해

### 실습 완료
- [ ] 프로젝트 생성
- [ ] 앱 생성 및 등록
- [ ] 모델 설계 및 마이그레이션
- [ ] Admin 패널 설정
- [ ] URL 라우팅
- [ ] 뷰 작성
- [ ] 템플릿 작성
- [ ] 폼 작성

### 기능 테스트
- [ ] 포스트 목록 조회
- [ ] 포스트 상세 조회
- [ ] 포스트 작성
- [ ] 포스트 수정
- [ ] 포스트 삭제
- [ ] 댓글 작성
- [ ] 좋아요/북마크
- [ ] 검색 기능
- [ ] 대시보드

---

## 추가 학습 자료

### Django 공식 문서
- https://docs.djangoproject.com/ko/

### 추천 튜토리얼
- Django Girls Tutorial (한글): https://tutorial.djangogirls.org/ko/
- 점프 투 장고: https://wikidocs.net/book/4223

### 연습 프로젝트
1. 사용자 등록 기능 추가
2. 페이지네이션 구현
3. 이미지 업로드 기능
4. REST API 추가
5. 프로덕션 배포

---

## 마무리

축하합니다! Django 블로그 프로젝트를 완성했습니다.

이 튜토리얼을 통해:
- Django 기본 구조 이해
- 데이터베이스 모델링
- URL-View-Template 연결
- 사용자 인증
- CRUD 작업
- 데이터 관계 설정

등을 학습했습니다.

계속해서 기능을 추가하고 개선하면서 실력을 향상시키세요!
