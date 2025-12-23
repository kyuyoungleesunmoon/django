# 🎯 Django 프로젝트 생성부터 코딩까지 - 완전 가이드

## 📌 목차
1. Django 설치
2. 프로젝트 생성
3. 앱 생성
4. 코딩 순서 (MVC 패턴)
5. 접속 URL
6. 전체 흐름 요약

---

## 1️⃣ Django 설치

### 패키지 설치
```bash
pip install django==4.2.8
```

### 설치 확인
```bash
python -m django --version
# 출력: 4.2.8
```

---

## 2️⃣ Django 프로젝트 생성

### 프로젝트 생성 (최상위)
```bash
# 새 폴더에서
django-admin startproject myproject

# 폴더 구조 확인
myproject/
├── manage.py              # Django 관리 스크립트 (중요!)
├── myproject/             # 프로젝트 설정 폴더
│   ├── __init__.py
│   ├── settings.py        # 설정 파일 (데이터베이스, 앱 등록 등)
│   ├── urls.py            # 메인 URL 라우팅
│   ├── asgi.py
│   └── wsgi.py
└── db.sqlite3             # 데이터베이스 (마이그레이션 후 생성)
```

### 프로젝트 폴더로 이동
```bash
cd myproject
```

---

## 3️⃣ Django 앱 생성

### 앱이란?
- **프로젝트**: 전체 웹사이트 (예: myproject)
- **앱**: 프로젝트 내 기능 단위 (예: blog, accounts, shop)

### 앱 생성
```bash
python manage.py startapp blog
# 또는
python manage.py startapp accounts
python manage.py startapp shop
```

### 생성된 앱 폴더 구조
```bash
blog/
├── migrations/            # 마이그레이션 파일 저장
│   └── __init__.py
├── __init__.py
├── admin.py               # 관리자 페이지 (필수 수정)
├── apps.py                # 앱 설정
├── models.py              # 데이터베이스 모델 (필수 수정) ⭐
├── tests.py               # 테스트
├── urls.py                # 앱 URL (직접 생성) ⭐
└── views.py               # 뷰 로직 (필수 수정) ⭐
```

### 프로젝트 설정에 앱 등록
**myproject/settings.py** 파일을 열고:

```python
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'blog',  # ← 여기에 추가!
]
```

---

## 4️⃣ 코딩 순서 (중요!)

### 🔴 **잘못된 순서**
❌ views.py → models.py → urls.py → templates

### 🟢 **올바른 순서 (MVC 패턴)**

```
Step 1: models.py     (데이터 정의)
    ↓
Step 2: views.py      (로직 작성)
    ↓
Step 3: urls.py       (URL 라우팅)
    ↓
Step 4: templates/    (화면 표시)
    ↓
Step 5: admin.py      (관리자 페이지)
    ↓
Step 6: 마이그레이션 (데이터베이스 생성)
    ↓
Step 7: 서버 실행 & 테스트
```

---

## 📝 **Step 1: 모델 정의 (models.py)**

### 예제: 블로그 포스트 모델

**blog/models.py**
```python
from django.db import models
from django.contrib.auth.models import User

class Post(models.Model):
    """블로그 포스트 모델"""
    title = models.CharField(max_length=200)           # 제목
    content = models.TextField()                       # 본문
    author = models.ForeignKey(User, on_delete=models.CASCADE)  # 작성자
    created_at = models.DateTimeField(auto_now_add=True)       # 생성 시간
    updated_at = models.DateTimeField(auto_now=True)           # 수정 시간
    
    class Meta:
        ordering = ['-created_at']  # 최신순 정렬
    
    def __str__(self):
        return self.title
```

### 필드 타입 정리
```python
models.CharField(max_length=100)      # 짧은 텍스트
models.TextField()                     # 긴 텍스트
models.IntegerField()                  # 정수
models.FloatField()                    # 소수점
models.BooleanField(default=False)    # True/False
models.DateTimeField(auto_now_add=True)  # 자동 시간 기록
models.ForeignKey(User, on_delete=models.CASCADE)  # 다른 모델 참조
```

---

## 👁️ **Step 2: 뷰 작성 (views.py)**

### 뷰란?
- 데이터를 처리하고 화면에 표시하는 로직
- **함수형 뷰** 또는 **클래스형 뷰** 사용

### 함수형 뷰 (간단함)

**blog/views.py**
```python
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from .models import Post

# 1️⃣ 포스트 목록 표시
def post_list(request):
    """모든 포스트 조회"""
    posts = Post.objects.all()  # 데이터베이스에서 모든 포스트 조회
    return render(request, 'blog/post_list.html', {'posts': posts})

# 2️⃣ 포스트 상세 표시
def post_detail(request, pk):
    """특정 포스트 조회"""
    post = get_object_or_404(Post, pk=pk)  # pk가 없으면 404 에러
    return render(request, 'blog/post_detail.html', {'post': post})

# 3️⃣ 포스트 생성
def post_create(request):
    """포스트 생성 폼"""
    if request.method == 'POST':
        # 폼 데이터 처리
        title = request.POST.get('title')
        content = request.POST.get('content')
        post = Post.objects.create(
            title=title,
            content=content,
            author=request.user
        )
        return redirect('post_detail', pk=post.pk)
    
    return render(request, 'blog/post_form.html')

# 4️⃣ 포스트 수정
def post_update(request, pk):
    """포스트 수정"""
    post = get_object_or_404(Post, pk=pk)
    
    if request.method == 'POST':
        post.title = request.POST.get('title')
        post.content = request.POST.get('content')
        post.save()
        return redirect('post_detail', pk=post.pk)
    
    return render(request, 'blog/post_form.html', {'post': post})

# 5️⃣ 포스트 삭제
def post_delete(request, pk):
    """포스트 삭제"""
    post = get_object_or_404(Post, pk=pk)
    
    if request.method == 'POST':
        post.delete()
        return redirect('post_list')
    
    return render(request, 'blog/post_confirm_delete.html', {'post': post})
```

### 클래스형 뷰 (더 강력함)

```python
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from .models import Post

class PostListView(ListView):
    """포스트 목록"""
    model = Post
    template_name = 'blog/post_list.html'
    context_object_name = 'posts'
    paginate_by = 10  # 페이지당 10개

class PostDetailView(DetailView):
    """포스트 상세"""
    model = Post
    template_name = 'blog/post_detail.html'
    context_object_name = 'post'

class PostCreateView(CreateView):
    """포스트 생성"""
    model = Post
    template_name = 'blog/post_form.html'
    fields = ['title', 'content']
    
    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

class PostUpdateView(UpdateView):
    """포스트 수정"""
    model = Post
    template_name = 'blog/post_form.html'
    fields = ['title', 'content']

class PostDeleteView(DeleteView):
    """포스트 삭제"""
    model = Post
    template_name = 'blog/post_confirm_delete.html'
    success_url = reverse_lazy('post_list')
```

---

## 🌐 **Step 3: URL 라우팅 (urls.py)**

### 앱 URL 설정 (새로 생성)

**blog/urls.py** (직접 생성)
```python
from django.urls import path
from . import views

urlpatterns = [
    # 함수형 뷰
    path('', views.post_list, name='post_list'),              # /
    path('post/<int:pk>/', views.post_detail, name='post_detail'),     # /post/1/
    path('post/create/', views.post_create, name='post_create'),       # /post/create/
    path('post/<int:pk>/edit/', views.post_update, name='post_update'),  # /post/1/edit/
    path('post/<int:pk>/delete/', views.post_delete, name='post_delete'),  # /post/1/delete/
    
    # 또는 클래스형 뷰
    # path('', views.PostListView.as_view(), name='post_list'),
    # path('post/<int:pk>/', views.PostDetailView.as_view(), name='post_detail'),
    # path('post/create/', views.PostCreateView.as_view(), name='post_create'),
]
```

### 프로젝트 메인 URL 설정

**myproject/urls.py** (수정)
```python
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('blog.urls')),  # ← blog 앱 URL 포함
    # 또는
    # path('blog/', include('blog.urls')),  # /blog/로 시작
]
```

---

## 🎨 **Step 4: 템플릿 작성 (templates/)**

### 폴더 생성
```bash
blog/
├── templates/
│   └── blog/
│       ├── base.html              # 기본 템플릿
│       ├── post_list.html         # 포스트 목록
│       ├── post_detail.html       # 포스트 상세
│       ├── post_form.html         # 작성/수정 폼
│       └── post_confirm_delete.html  # 삭제 확인
```

### settings.py에 템플릿 경로 설정

**myproject/settings.py**
```python
import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],  # ← 추가
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

### 기본 템플릿

**blog/templates/blog/base.html**
```html
<!DOCTYPE html>
<html lang="ko">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{% block title %}Django 블로그{% endblock %}</title>
    <style>
        body { font-family: Arial, sans-serif; margin: 20px; }
        header { border-bottom: 2px solid #333; padding-bottom: 10px; margin-bottom: 20px; }
        a { color: blue; text-decoration: none; margin-right: 10px; }
        a:hover { text-decoration: underline; }
    </style>
</head>
<body>
    <header>
        <h1>📝 Django 블로그</h1>
        <nav>
            <a href="{% url 'post_list' %}">전체 포스트</a>
            <a href="{% url 'post_create' %}">글쓰기</a>
        </nav>
    </header>
    
    <main>
        {% block content %}{% endblock %}
    </main>
    
    <footer style="margin-top: 50px; border-top: 1px solid #ccc; padding-top: 10px; color: gray;">
        <p>&copy; 2025 Django Blog</p>
    </footer>
</body>
</html>
```

### 포스트 목록 템플릿

**blog/templates/blog/post_list.html**
```html
{% extends 'blog/base.html' %}

{% block title %}포스트 목록{% endblock %}

{% block content %}
<h2>📚 전체 포스트</h2>

{% if posts %}
    <ul style="list-style: none; padding: 0;">
    {% for post in posts %}
        <li style="border: 1px solid #ddd; padding: 10px; margin-bottom: 10px;">
            <h3>
                <a href="{% url 'post_detail' post.pk %}">{{ post.title }}</a>
            </h3>
            <p>{{ post.content|truncatewords:30 }}</p>
            <small>
                작성자: {{ post.author }} | 
                작성일: {{ post.created_at|date:"Y-m-d H:i" }}
            </small>
            <br><br>
            <a href="{% url 'post_update' post.pk %}">✏️ 수정</a>
            <a href="{% url 'post_delete' post.pk %}">🗑️ 삭제</a>
        </li>
    {% endfor %}
    </ul>
{% else %}
    <p>포스트가 없습니다.</p>
{% endif %}
{% endblock %}
```

### 포스트 상세 템플릿

**blog/templates/blog/post_detail.html**
```html
{% extends 'blog/base.html' %}

{% block title %}{{ post.title }}{% endblock %}

{% block content %}
<h1>{{ post.title }}</h1>

<div style="color: gray; font-size: 0.9em; margin-bottom: 20px;">
    작성자: <strong>{{ post.author }}</strong> | 
    작성일: {{ post.created_at|date:"Y-m-d H:i" }} |
    수정일: {{ post.updated_at|date:"Y-m-d H:i" }}
</div>

<div style="line-height: 1.8; margin-bottom: 30px;">
    {{ post.content|linebreaks }}
</div>

<hr>

<a href="{% url 'post_list' %}">← 목록으로</a>
<a href="{% url 'post_update' post.pk %}">✏️ 수정</a>
<a href="{% url 'post_delete' post.pk %}">🗑️ 삭제</a>
{% endblock %}
```

### 포스트 작성/수정 폼 템플릿

**blog/templates/blog/post_form.html**
```html
{% extends 'blog/base.html' %}

{% block title %}포스트 {% if post %}수정{% else %}작성{% endif %}{% endblock %}

{% block content %}
<h2>{% if post %}포스트 수정{% else %}새 포스트 작성{% endif %}</h2>

<form method="post" style="max-width: 600px;">
    {% csrf_token %}
    
    <div style="margin-bottom: 15px;">
        <label for="title">제목:</label><br>
        <input 
            type="text" 
            id="title" 
            name="title" 
            value="{% if post %}{{ post.title }}{% endif %}" 
            required
            style="width: 100%; padding: 8px; font-size: 16px;"
        >
    </div>
    
    <div style="margin-bottom: 15px;">
        <label for="content">내용:</label><br>
        <textarea 
            id="content" 
            name="content" 
            rows="10" 
            required
            style="width: 100%; padding: 8px; font-size: 16px;"
        >{% if post %}{{ post.content }}{% endif %}</textarea>
    </div>
    
    <div>
        <button type="submit" style="padding: 10px 20px; font-size: 16px; cursor: pointer;">
            {% if post %}수정 완료{% else %}작성{% endif %}
        </button>
        <a href="{% url 'post_list' %}">취소</a>
    </div>
</form>
{% endblock %}
```

### 삭제 확인 템플릿

**blog/templates/blog/post_confirm_delete.html**
```html
{% extends 'blog/base.html' %}

{% block title %}포스트 삭제{% endblock %}

{% block content %}
<h2>정말로 삭제하시겠습니까?</h2>

<p><strong>{{ post.title }}</strong></p>

<form method="post" style="display: inline;">
    {% csrf_token %}
    <button type="submit" style="padding: 10px 20px; background-color: red; color: white; cursor: pointer;">
        삭제
    </button>
    <a href="{% url 'post_detail' post.pk %}" style="padding: 10px 20px; background-color: gray; color: white; text-decoration: none;">
        취소
    </a>
</form>
{% endblock %}
```

---

## 👨‍💼 **Step 5: 관리자 페이지 설정 (admin.py)**

**blog/admin.py**
```python
from django.contrib import admin
from .models import Post

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ['title', 'author', 'created_at']  # 목록에 표시할 필드
    search_fields = ['title', 'content']              # 검색 가능한 필드
    list_filter = ['created_at', 'author']            # 필터 옵션
    readonly_fields = ['created_at', 'updated_at']    # 읽기 전용
```

---

## 🗄️ **Step 6: 마이그레이션 (데이터베이스 생성)**

### 마이그레이션 파일 생성
```bash
python manage.py makemigrations
# 출력: Migrations for 'blog':
#   blog/migrations/0001_initial.py
#     - Create model Post
```

### 마이그레이션 실행 (데이터베이스에 적용)
```bash
python manage.py migrate
# 출력: Running migrations:
#   Applying blog.0001_initial... OK
```

### 확인
```bash
python manage.py showmigrations
# blog
#  [X] 0001_initial
```

---

## 🚀 **Step 7: 서버 실행 및 테스트**

### 관리자 계정 생성 (필수!)
```bash
python manage.py createsuperuser
# Username: admin
# Email: admin@example.com
# Password: ****
```

### 서버 실행
```bash
python manage.py runserver
# Quit the server with CTRL-BREAK.
# Starting development server at http://127.0.0.1:8000/
```

---

## 🌐 **접속 URL 정리**

### URL 구조

| 기능 | URL | HTTP 메서드 | 뷰 |
|---|---|---|---|
| **홈페이지** | http://127.0.0.1:8000/ | GET | post_list |
| **포스트 상세** | http://127.0.0.1:8000/post/1/ | GET | post_detail |
| **포스트 작성** | http://127.0.0.1:8000/post/create/ | GET/POST | post_create |
| **포스트 수정** | http://127.0.0.1:8000/post/1/edit/ | GET/POST | post_update |
| **포스트 삭제** | http://127.0.0.1:8000/post/1/delete/ | GET/POST | post_delete |
| **관리자 페이지** | http://127.0.0.1:8000/admin/ | GET | admin panel |

### 동작 흐름

```
사용자가 URL 입력
    ↓
urls.py에서 매칭되는 패턴 찾음
    ↓
해당 뷰 함수/클래스 실행
    ↓
모델에서 데이터 조회/생성/수정/삭제
    ↓
템플릿에 데이터 전달
    ↓
HTML 렌더링
    ↓
브라우저에 표시
```

---

## 📊 **전체 파일 생성 순서 요약**

### 1. 프로젝트/앱 생성
```bash
django-admin startproject myproject
cd myproject
python manage.py startapp blog
```

### 2. 파일 수정 순서
```
① myproject/settings.py
   - INSTALLED_APPS에 'blog' 추가

② blog/models.py ⭐ (가장 중요!)
   - 데이터베이스 모델 정의

③ blog/views.py
   - 데이터 처리 로직

④ blog/urls.py (새로 생성)
   - URL 패턴 정의

⑤ myproject/urls.py
   - blog.urls 포함

⑥ blog/templates/blog/*.html
   - HTML 템플릿 작성

⑦ blog/admin.py
   - 관리자 페이지 설정

⑧ 마이그레이션
   - python manage.py makemigrations
   - python manage.py migrate

⑨ 테스트
   - python manage.py runserver
```

---

## 🎯 **최소한의 코드 (기본 블로그)**

### Step 1: models.py
```python
from django.db import models

class Post(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.title
```

### Step 2: views.py
```python
from django.shortcuts import render
from .models import Post

def post_list(request):
    posts = Post.objects.all()
    return render(request, 'blog/post_list.html', {'posts': posts})
```

### Step 3: urls.py
```python
from django.urls import path
from . import views

urlpatterns = [
    path('', views.post_list, name='post_list'),
]
```

### Step 4: myproject/urls.py
```python
from django.urls import path, include

urlpatterns = [
    path('', include('blog.urls')),
]
```

### Step 5: templates/blog/post_list.html
```html
<h1>포스트 목록</h1>
{% for post in posts %}
    <h2>{{ post.title }}</h2>
    <p>{{ post.content }}</p>
{% endfor %}
```

### 마이그레이션
```bash
python manage.py makemigrations
python manage.py migrate
python manage.py runserver
```

### 접속
```
http://127.0.0.1:8000/
```

---

## 🎓 **핵심 개념 정리**

### MTV 패턴 (Model-Template-View)
```
Model       : 데이터 구조 (models.py)
Template    : 화면 표시 (templates/*.html)
View        : 데이터 처리 (views.py)
```

### URL 매핑
```
URL → urls.py → view → template → HTML
```

### 데이터 흐름
```
Browser → URL → View → Model → Database
                 ↓
            Template ← Context
                 ↓
              HTML
```

---

## ⚠️ **흔한 실수**

### ❌ 1. models.py 변경 후 마이그레이션 안 함
```bash
# ❌ 그냥 서버 실행
python manage.py runserver

# ✅ 마이그레이션 먼저!
python manage.py makemigrations
python manage.py migrate
python manage.py runserver
```

### ❌ 2. INSTALLED_APPS에 앱 등록 안 함
```python
# ❌
INSTALLED_APPS = [
    'django.contrib.admin',
    # blog가 없음!
]

# ✅
INSTALLED_APPS = [
    'django.contrib.admin',
    'blog',  # 추가!
]
```

### ❌ 3. urls.py 패턴 문법
```python
# ❌ 틀림
path('post/<pk>/', views.post_detail)  # 자료형 없음

# ✅ 맞음
path('post/<int:pk>/', views.post_detail)
```

### ❌ 4. templates 경로 설정 안 함
```python
# ❌ settings.py에 설정 안 함
# TEMPLATES 설정 필수!

# ✅
TEMPLATES = [
    {
        'DIRS': [BASE_DIR / 'templates'],
    }
]
```

---

## ✨ **시작 체크리스트**

- [ ] Django 설치 (`pip install django`)
- [ ] 프로젝트 생성 (`startproject`)
- [ ] 앱 생성 (`startapp blog`)
- [ ] settings.py에 앱 등록
- [ ] models.py 작성
- [ ] views.py 작성
- [ ] urls.py 생성 및 설정
- [ ] myproject/urls.py 수정 (include)
- [ ] templates 폴더 및 파일 생성
- [ ] 마이그레이션 실행
- [ ] 서버 실행
- [ ] 브라우저에서 확인

---

이제 Django 프로젝트를 **체계적으로** 만들 수 있습니다! 🚀
