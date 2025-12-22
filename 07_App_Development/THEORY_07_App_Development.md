# 07. Django 프로젝트에서 앱 개발하기

## 개요
이 단계에서는 Django 프로젝트에서 실제로 사용할 수 있는 앱을 만드는 방법을 배웁니다. Blog 앱과 Pages 앱을 만들어 기본적인 구조를 이해합니다.

## 07-1. 블로그 앱과 페이지 앱 만들기

### 개념
Django 프로젝트는 여러 개의 앱(애플리케이션)으로 구성됩니다. 각 앱은:
- **Blog 앱**: 블로그 포스트 관리 (Create, Read, Update, Delete)
- **Pages 앱**: 정적 페이지 (About, Contact 등)

### 앱 생성 명령어

```bash
# blog 앱 생성
python manage.py startapp blog

# pages 앱 생성
python manage.py startapp pages
```

### 생성된 앱 구조

```
blog/
├── __init__.py
├── admin.py          # Admin 페이지에 모델 등록
├── apps.py           # 앱 설정
├── migrations/       # 데이터베이스 마이그레이션 파일
│   └── __init__.py
├── models.py         # 데이터 모델 정의
├── tests.py          # 테스트 코드
├── urls.py           # URL 패턴 (직접 생성 필요)
└── views.py          # 뷰 함수/클래스

pages/
├── (blog과 동일한 구조)
```

### 앱을 프로젝트에 등록

**simpleblog/settings.py**에서 INSTALLED_APPS에 앱 등록:

```python
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    
    # 우리의 앱
    'blog.apps.BlogConfig',      # 또는 'blog'
    'pages.apps.PagesConfig',    # 또는 'pages'
]
```

### 앱 초기화 확인

각 앱의 구조가 제대로 생성되었는지 확인하세요.

---

## 07-2. 데이터베이스 개념 이해하기

### 관계형 데이터베이스(RDBMS)란?

데이터를 표(Table) 형태로 저장하고 관리하는 데이터베이스 시스템입니다.

### 데이터베이스 기본 개념

#### 테이블(Table)
```
Post 테이블:
┌────┬───────────┬──────────────┬─────────────┬────────────┐
│ id │  title    │   content    │ author_id   │ created_at │
├────┼───────────┼──────────────┼─────────────┼────────────┤
│ 1  │ 첫 글     │ 내용...      │ 1           │ 2024-01-01 │
│ 2  │ 두 번째   │ 내용...      │ 1           │ 2024-01-02 │
└────┴───────────┴──────────────┴─────────────┴────────────┘
```

#### 행(Row) vs 열(Column)
- **행(Row)**: 하나의 데이터 레코드 (예: 하나의 블로그 포스트)
- **열(Column)**: 데이터의 속성 (예: title, content, author)

#### 기본키(Primary Key)
- 각 행을 고유하게 식별하는 열
- Django에서는 자동으로 `id` 필드를 기본키로 생성

#### 외래키(Foreign Key)
- 다른 테이블의 기본키를 참조하는 열
- 테이블 간의 관계를 정의
- 예: Post의 author_id는 User의 id를 참조

### Django의 ORM (Object-Relational Mapping)

ORM은 데이터베이스 테이블을 Python 클래스와 매핑합니다.

```
데이터베이스 구조         →    Python 클래스
┌─────────────────┐           ┌──────────────┐
│ Post 테이블    │           │ Post 클래스  │
├─────────────────┤           ├──────────────┤
│ id (정수)       │   →       │ id (필드)    │
│ title (문자)    │   →       │ title (필드) │
│ content (문자)  │   →       │ content      │
│ created_at (날짜) →        │ created_at   │
└─────────────────┘           └──────────────┘
```

### ORM의 장점
1. **SQL 쓰지 않아도 됨**: Python 코드로 데이터베이스 조작
2. **코드 가독성**: 더 직관적이고 유지보수하기 쉬움
3. **데이터베이스 독립성**: SQLite, MySQL, PostgreSQL 등을 쉽게 변경 가능
4. **보안**: SQL Injection 공격 방지

### 데이터베이스 동작 예시

```python
# ORM 사용
Post.objects.create(title="첫 글", content="내용...")

# SQL 쿼리 (ORM 없이)
INSERT INTO blog_post (title, content) VALUES ('첫 글', '내용...');
```

---

## 07-3. 모델 만들기

### 모델이란?
Django 앱의 데이터 구조를 정의하는 Python 클래스입니다.

### 필드 타입

| 필드 타입 | 설명 | 데이터베이스 타입 |
|----------|------|------------------|
| CharField | 짧은 문자 | VARCHAR |
| TextField | 긴 문자 | TEXT |
| IntegerField | 정수 | INTEGER |
| DecimalField | 소수점 숫자 | DECIMAL |
| DateField | 날짜 | DATE |
| DateTimeField | 날짜와 시간 | DATETIME |
| BooleanField | True/False | BOOLEAN |
| EmailField | 이메일 | VARCHAR |
| URLField | URL | VARCHAR |
| ImageField | 이미지 | VARCHAR |
| FileField | 파일 | VARCHAR |
| ForeignKey | 외래키 (관계) | INTEGER |
| ManyToManyField | 다대다 관계 | 별도 테이블 |

### 필드 옵션

```python
title = models.CharField(
    max_length=200,           # 최대 길이
    null=False,               # NULL 허용 여부
    blank=False,              # 폼에서 비어있을 수 있는지
    default='',               # 기본값
    unique=False,             # 유일성
    db_index=False,           # 인덱스 생성
    help_text='제목을 입력하세요',  # 도움말
    verbose_name='포스트 제목'     # 관리자 페이지에 표시되는 이름
)
```

### Blog 앱의 Post 모델 만들기

```python
# blog/models.py

from django.db import models
from django.contrib.auth.models import User

class Post(models.Model):
    """블로그 포스트 모델"""
    
    # 필드 정의
    title = models.CharField(
        max_length=200,
        verbose_name='제목'
    )
    content = models.TextField(
        verbose_name='내용'
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='작성자'
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
        ordering = ['-created_at']  # 최신순 정렬
        verbose_name = '블로그 포스트'
        verbose_name_plural = '블로그 포스트'
    
    def __str__(self):
        return self.title
```

### Pages 앱의 Page 모델 만들기

```python
# pages/models.py

from django.db import models

class Page(models.Model):
    """정적 페이지 모델"""
    
    title = models.CharField(
        max_length=200,
        verbose_name='페이지 제목'
    )
    slug = models.SlugField(
        unique=True,
        verbose_name='슬러그'
    )
    content = models.TextField(
        verbose_name='페이지 내용'
    )
    is_active = models.BooleanField(
        default=True,
        verbose_name='활성화'
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='작성일'
    )
    
    class Meta:
        verbose_name = '페이지'
        verbose_name_plural = '페이지'
    
    def __str__(self):
        return self.title
```

### 모델 마이그레이션

```bash
# 마이그레이션 파일 생성 (변경사항 감지)
python manage.py makemigrations

# 마이그레이션 실행 (데이터베이스 적용)
python manage.py migrate

# 마이그레이션 상태 확인
python manage.py showmigrations
```

### Admin 페이지에 모델 등록

```python
# blog/admin.py

from django.contrib import admin
from .models import Post

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ['title', 'author', 'created_at']
    list_filter = ['created_at', 'author']
    search_fields = ['title', 'content']
    prepopulated_fields = {'slug': ('title',)}
```

```python
# pages/admin.py

from django.contrib import admin
from .models import Page

@admin.register(Page)
class PageAdmin(admin.ModelAdmin):
    list_display = ['title', 'slug', 'is_active']
    list_filter = ['is_active', 'created_at']
    search_fields = ['title', 'content']
    prepopulated_fields = {'slug': ('title',)}
```

### 확인하기
1. 관리자 페이지 접속: `http://127.0.0.1:8000/admin/`
2. Post와 Page 모델이 등록되어 있는지 확인
3. 데이터 추가, 수정, 삭제 기능이 자동으로 생성됨

---

## 요약

- **07-1**: 앱은 프로젝트의 기능별 모듈 (blog, pages)
- **07-2**: ORM은 데이터베이스를 Python 객체로 사용하게 해줌
- **07-3**: 모델은 데이터의 구조를 정의하는 가장 중요한 부분
