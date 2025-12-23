# 🔥 Django 프로젝트 - 실행 예제 (복사-붙여넣기)

## 📌 처음부터 끝까지 실행하기

### 1️⃣ 명령어 실행 (터미널)

```powershell
# Step 1: 프로젝트 생성
django-admin startproject myproject
cd myproject

# Step 2: 앱 생성
python manage.py startapp blog

# Step 3: 마이그레이션 및 서버 실행은 아래에서...
```

---

## 2️⃣ 파일 수정 (복사-붙여넣기)

### 파일 1️⃣: myproject/settings.py

찾을 내용 (약 30-50줄):
```python
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
]
```

**변경**: 'blog' 추가
```python
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'blog',  # ← 추가
]
```

또한 TEMPLATES 설정 찾아서 (약 55-70줄):
```python
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],  # ← 이 줄 수정
```

**변경**:
```python
import os  # 맨 위에 추가

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],  # ← 변경
```

---

### 파일 2️⃣: blog/models.py

**전체 코드 (모두 지우고 복사-붙여넣기)**:
```python
from django.db import models
from django.contrib.auth.models import User

class Post(models.Model):
    """블로그 포스트"""
    title = models.CharField(max_length=200)
    content = models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return self.title
```

---

### 파일 3️⃣: blog/views.py

**전체 코드 (모두 지우고 복사-붙여넣기)**:
```python
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from .models import Post

# ===== 포스트 =====

def post_list(request):
    """포스트 목록"""
    posts = Post.objects.all()
    return render(request, 'blog/post_list.html', {'posts': posts})

def post_detail(request, pk):
    """포스트 상세"""
    post = get_object_or_404(Post, pk=pk)
    return render(request, 'blog/post_detail.html', {'post': post})

@login_required
def post_create(request):
    """포스트 작성"""
    if request.method == 'POST':
        title = request.POST.get('title')
        content = request.POST.get('content')
        post = Post.objects.create(
            title=title,
            content=content,
            author=request.user
        )
        return redirect('post_detail', pk=post.pk)
    
    return render(request, 'blog/post_form.html')

@login_required
def post_update(request, pk):
    """포스트 수정"""
    post = get_object_or_404(Post, pk=pk)
    
    # 소유자만 수정 가능
    if post.author != request.user:
        return redirect('post_detail', pk=pk)
    
    if request.method == 'POST':
        post.title = request.POST.get('title')
        post.content = request.POST.get('content')
        post.save()
        return redirect('post_detail', pk=post.pk)
    
    return render(request, 'blog/post_form.html', {'post': post})

@login_required
def post_delete(request, pk):
    """포스트 삭제"""
    post = get_object_or_404(Post, pk=pk)
    
    # 소유자만 삭제 가능
    if post.author != request.user:
        return redirect('post_detail', pk=pk)
    
    if request.method == 'POST':
        post.delete()
        return redirect('post_list')
    
    return render(request, 'blog/post_confirm_delete.html', {'post': post})

# ===== 사용자 =====

def home(request):
    """홈페이지"""
    return render(request, 'blog/home.html')

def register(request):
    """회원가입"""
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        password_confirm = request.POST.get('password_confirm')
        
        if password != password_confirm:
            return render(request, 'blog/register.html', {'error': '비밀번호가 다릅니다'})
        
        if User.objects.filter(username=username).exists():
            return render(request, 'blog/register.html', {'error': '이미 존재하는 사용자입니다'})
        
        user = User.objects.create_user(username=username, email=email, password=password)
        return redirect('login')
    
    return render(request, 'blog/register.html')

def login_view(request):
    """로그인"""
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('post_list')
        else:
            return render(request, 'blog/login.html', {'error': '사용자명 또는 비밀번호가 잘못되었습니다'})
    
    return render(request, 'blog/login.html')

def logout_view(request):
    """로그아웃"""
    logout(request)
    return redirect('post_list')

def dashboard(request):
    """대시보드"""
    if not request.user.is_authenticated:
        return redirect('login')
    
    my_posts = Post.objects.filter(author=request.user)
    return render(request, 'blog/dashboard.html', {'posts': my_posts})
```

---

### 파일 4️⃣: blog/urls.py (새로 생성!)

**새 파일 생성**: `blog/urls.py`
```python
from django.urls import path
from . import views

urlpatterns = [
    # 홈
    path('', views.home, name='home'),
    
    # 포스트
    path('posts/', views.post_list, name='post_list'),
    path('post/<int:pk>/', views.post_detail, name='post_detail'),
    path('post/create/', views.post_create, name='post_create'),
    path('post/<int:pk>/edit/', views.post_update, name='post_update'),
    path('post/<int:pk>/delete/', views.post_delete, name='post_delete'),
    
    # 사용자
    path('register/', views.register, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('dashboard/', views.dashboard, name='dashboard'),
]
```

---

### 파일 5️⃣: myproject/urls.py

찾을 내용:
```python
from django.contrib import admin
from django.urls import path

urlpatterns = [
    path('admin/', admin.site.urls),
]
```

**변경**:
```python
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('blog.urls')),  # ← 추가
]
```

---

### 파일 6️⃣: blog/admin.py

**전체 코드 (모두 지우고 복사-붙여넣기)**:
```python
from django.contrib import admin
from .models import Post

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ['title', 'author', 'created_at']
    search_fields = ['title', 'content']
    list_filter = ['created_at']
    readonly_fields = ['created_at', 'updated_at']
```

---

### 파일 7️⃣: templates/blog/base.html

**새 폴더 생성**: 
- `templates` 폴더
- `templates/blog` 폴더

**파일**: `templates/blog/base.html`
```html
<!DOCTYPE html>
<html lang="ko">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{% block title %}Django 블로그{% endblock %}</title>
    <style>
        * { margin: 0; padding: 0; }
        body { font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; background: #f5f5f5; }
        
        header {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 20px;
            box-shadow: 0 2px 5px rgba(0,0,0,0.1);
        }
        
        nav a {
            color: white;
            margin: 0 15px;
            text-decoration: none;
            font-weight: 500;
            transition: 0.3s;
        }
        
        nav a:hover { opacity: 0.8; }
        
        .container {
            max-width: 1000px;
            margin: 30px auto;
            padding: 0 20px;
        }
        
        footer {
            background: #333;
            color: #999;
            text-align: center;
            padding: 20px;
            margin-top: 50px;
        }
        
        .alert { padding: 10px; margin: 10px 0; border-radius: 5px; }
        .alert-error { background: #fee; color: #c33; }
        .alert-success { background: #efe; color: #3c3; }
        
        button {
            background: #667eea;
            color: white;
            border: none;
            padding: 10px 20px;
            border-radius: 5px;
            cursor: pointer;
            font-weight: bold;
            transition: 0.3s;
        }
        
        button:hover { background: #764ba2; }
        
        input, textarea {
            padding: 8px;
            margin: 5px 0;
            border: 1px solid #ddd;
            border-radius: 4px;
            font-family: inherit;
        }
        
        input[type="text"],
        input[type="email"],
        input[type="password"],
        textarea {
            width: 100%;
            box-sizing: border-box;
        }
    </style>
</head>
<body>
    <header>
        <h1>📝 Django 블로그</h1>
        <nav>
            <a href="{% url 'home' %}">홈</a>
            <a href="{% url 'post_list' %}">포스트</a>
            {% if user.is_authenticated %}
                <a href="{% url 'post_create' %}">✏️ 글쓰기</a>
                <a href="{% url 'dashboard' %}">대시보드</a>
                <a href="{% url 'logout' %}">로그아웃 ({{ user }})</a>
            {% else %}
                <a href="{% url 'register' %}">회원가입</a>
                <a href="{% url 'login' %}">로그인</a>
            {% endif %}
        </nav>
    </header>
    
    <div class="container">
        {% if messages %}
            {% for message in messages %}
                <div class="alert alert-{{ message.tags }}">{{ message }}</div>
            {% endfor %}
        {% endif %}
        
        {% block content %}{% endblock %}
    </div>
    
    <footer>
        &copy; 2025 Django 블로그
    </footer>
</body>
</html>
```

---

### 파일 8️⃣: templates/blog/home.html

```html
{% extends 'blog/base.html' %}

{% block title %}홈{% endblock %}

{% block content %}
<h2>환영합니다! 👋</h2>
<p>Django 블로그에 오신 것을 환영합니다.</p>

{% if user.is_authenticated %}
    <h3>{{ user }}님, 안녕하세요!</h3>
    <p><a href="{% url 'post_create' %}"><button>새 포스트 작성</button></a></p>
{% else %}
    <p><a href="{% url 'register' %}"><button>회원가입하기</button></a></p>
{% endif %}
{% endblock %}
```

---

### 파일 9️⃣: templates/blog/post_list.html

```html
{% extends 'blog/base.html' %}

{% block title %}포스트 목록{% endblock %}

{% block content %}
<h2>📚 전체 포스트</h2>

{% if user.is_authenticated %}
    <p><a href="{% url 'post_create' %}"><button>✏️ 새 포스트</button></a></p>
{% endif %}

{% if posts %}
    <div style="margin-top: 20px;">
    {% for post in posts %}
        <div style="background: white; padding: 20px; margin: 15px 0; border-radius: 8px; box-shadow: 0 2px 5px rgba(0,0,0,0.1);">
            <h3><a href="{% url 'post_detail' post.pk %}" style="color: #667eea; text-decoration: none;">{{ post.title }}</a></h3>
            <p style="color: #666; font-size: 0.9em; margin: 10px 0;">
                👤 {{ post.author }} | 📅 {{ post.created_at|date:"Y-m-d H:i" }}
            </p>
            <p>{{ post.content|truncatewords:30 }}</p>
            <div style="margin-top: 10px;">
                <a href="{% url 'post_detail' post.pk %}"><button style="background: #667eea;">자세히</button></a>
                {% if post.author == user %}
                    <a href="{% url 'post_update' post.pk %}"><button style="background: #48bb78;">수정</button></a>
                    <a href="{% url 'post_delete' post.pk %}"><button style="background: #f56565;">삭제</button></a>
                {% endif %}
            </div>
        </div>
    {% endfor %}
    </div>
{% else %}
    <p>포스트가 없습니다.</p>
{% endif %}
{% endblock %}
```

---

### 파일 🔟: templates/blog/post_detail.html

```html
{% extends 'blog/base.html' %}

{% block title %}{{ post.title }}{% endblock %}

{% block content %}
<article style="background: white; padding: 30px; border-radius: 8px;">
    <h1>{{ post.title }}</h1>
    
    <div style="color: #666; font-size: 0.9em; margin: 15px 0; padding-bottom: 15px; border-bottom: 1px solid #eee;">
        👤 <strong>{{ post.author }}</strong> | 
        📅 {{ post.created_at|date:"Y-m-d H:i" }} |
        ✏️ {{ post.updated_at|date:"Y-m-d H:i" }}
    </div>
    
    <div style="line-height: 1.8; font-size: 1.1em; margin: 30px 0;">
        {{ post.content|linebreaks }}
    </div>
    
    <div style="margin-top: 30px; padding-top: 15px; border-top: 1px solid #eee;">
        <a href="{% url 'post_list' %}"><button>← 목록으로</button></a>
        {% if post.author == user %}
            <a href="{% url 'post_update' post.pk %}"><button style="background: #48bb78;">✏️ 수정</button></a>
            <a href="{% url 'post_delete' post.pk %}"><button style="background: #f56565;">🗑️ 삭제</button></a>
        {% endif %}
    </div>
</article>
{% endblock %}
```

---

### 파일 1️⃣1️⃣: templates/blog/post_form.html

```html
{% extends 'blog/base.html' %}

{% block title %}{% if post %}수정{% else %}작성{% endif %}{% endblock %}

{% block content %}
<div style="background: white; padding: 30px; border-radius: 8px; max-width: 800px;">
    <h2>{% if post %}포스트 수정{% else %}새 포스트 작성{% endif %}</h2>
    
    <form method="post">
        {% csrf_token %}
        
        <div style="margin: 20px 0;">
            <label for="title">제목</label>
            <input 
                type="text" 
                id="title" 
                name="title" 
                value="{% if post %}{{ post.title }}{% endif %}"
                required
            >
        </div>
        
        <div style="margin: 20px 0;">
            <label for="content">내용</label>
            <textarea 
                id="content" 
                name="content" 
                rows="15"
                required
            >{% if post %}{{ post.content }}{% endif %}</textarea>
        </div>
        
        <div style="margin: 20px 0;">
            <button type="submit">{% if post %}수정 완료{% else %}작성{% endif %}</button>
            <a href="{% url 'post_list' %}"><button type="button">취소</button></a>
        </div>
    </form>
</div>
{% endblock %}
```

---

### 파일 1️⃣2️⃣: templates/blog/post_confirm_delete.html

```html
{% extends 'blog/base.html' %}

{% block title %}삭제{% endblock %}

{% block content %}
<div style="background: white; padding: 30px; border-radius: 8px; max-width: 500px;">
    <h2>⚠️ 정말로 삭제하시겠습니까?</h2>
    <p style="color: #666; margin: 20px 0;">
        이 작업은 되돌릴 수 없습니다.
    </p>
    
    <h3>{{ post.title }}</h3>
    
    <form method="post" style="margin-top: 30px;">
        {% csrf_token %}
        <button type="submit" style="background: #f56565; margin-right: 10px;">🗑️ 삭제</button>
        <a href="{% url 'post_detail' post.pk %}"><button type="button">취소</button></a>
    </form>
</div>
{% endblock %}
```

---

### 파일 1️⃣3️⃣: templates/blog/register.html

```html
{% extends 'blog/base.html' %}

{% block title %}회원가입{% endblock %}

{% block content %}
<div style="background: white; padding: 30px; border-radius: 8px; max-width: 500px; margin: auto;">
    <h2>회원가입</h2>
    
    {% if error %}
        <div class="alert alert-error">{{ error }}</div>
    {% endif %}
    
    <form method="post">
        {% csrf_token %}
        
        <div style="margin: 15px 0;">
            <label for="username">사용자명</label>
            <input type="text" id="username" name="username" required>
        </div>
        
        <div style="margin: 15px 0;">
            <label for="email">이메일</label>
            <input type="email" id="email" name="email" required>
        </div>
        
        <div style="margin: 15px 0;">
            <label for="password">비밀번호</label>
            <input type="password" id="password" name="password" required>
        </div>
        
        <div style="margin: 15px 0;">
            <label for="password_confirm">비밀번호 확인</label>
            <input type="password" id="password_confirm" name="password_confirm" required>
        </div>
        
        <button type="submit" style="width: 100%; margin-top: 20px;">회원가입</button>
    </form>
    
    <p style="margin-top: 20px; text-align: center;">
        이미 계정이 있으신가요? <a href="{% url 'login' %}" style="color: #667eea;">로그인</a>
    </p>
</div>
{% endblock %}
```

---

### 파일 1️⃣4️⃣: templates/blog/login.html

```html
{% extends 'blog/base.html' %}

{% block title %}로그인{% endblock %}

{% block content %}
<div style="background: white; padding: 30px; border-radius: 8px; max-width: 500px; margin: auto;">
    <h2>로그인</h2>
    
    {% if error %}
        <div class="alert alert-error">{{ error }}</div>
    {% endif %}
    
    <form method="post">
        {% csrf_token %}
        
        <div style="margin: 15px 0;">
            <label for="username">사용자명</label>
            <input type="text" id="username" name="username" required>
        </div>
        
        <div style="margin: 15px 0;">
            <label for="password">비밀번호</label>
            <input type="password" id="password" name="password" required>
        </div>
        
        <button type="submit" style="width: 100%; margin-top: 20px;">로그인</button>
    </form>
    
    <p style="margin-top: 20px; text-align: center;">
        계정이 없으신가요? <a href="{% url 'register' %}" style="color: #667eea;">회원가입</a>
    </p>
</div>
{% endblock %}
```

---

### 파일 1️⃣5️⃣: templates/blog/dashboard.html

```html
{% extends 'blog/base.html' %}

{% block title %}대시보드{% endblock %}

{% block content %}
<h2>👤 {{ user }}님의 대시보드</h2>

<h3>내 포스트 ({{ posts.count }})</h3>

{% if posts %}
    <div style="margin-top: 20px;">
    {% for post in posts %}
        <div style="background: white; padding: 15px; margin: 10px 0; border-radius: 5px;">
            <h4><a href="{% url 'post_detail' post.pk %}" style="color: #667eea;">{{ post.title }}</a></h4>
            <small>{{ post.created_at|date:"Y-m-d H:i" }}</small>
            <div style="margin-top: 10px;">
                <a href="{% url 'post_update' post.pk %}"><button style="background: #48bb78;">수정</button></a>
                <a href="{% url 'post_delete' post.pk %}"><button style="background: #f56565;">삭제</button></a>
            </div>
        </div>
    {% endfor %}
    </div>
{% else %}
    <p>아직 포스트가 없습니다.</p>
{% endif %}

<p style="margin-top: 30px;">
    <a href="{% url 'post_create' %}"><button>✏️ 새 포스트 작성</button></a>
</p>
{% endblock %}
```

---

## 3️⃣ 마이그레이션 및 실행

### 터미널 명령어
```powershell
# Step 1: 마이그레이션 파일 생성
python manage.py makemigrations

# Step 2: 데이터베이스에 적용
python manage.py migrate

# Step 3: 관리자 계정 생성
python manage.py createsuperuser
# Username: admin
# Email: admin@example.com
# Password: admin123

# Step 4: 서버 실행
python manage.py runserver
```

---

## 4️⃣ 접속 URL

브라우저에서:

| 기능 | URL |
|---|---|
| 홈 | http://127.0.0.1:8000/ |
| 포스트 목록 | http://127.0.0.1:8000/posts/ |
| 포스트 보기 | http://127.0.0.1:8000/post/1/ |
| 포스트 작성 | http://127.0.0.1:8000/post/create/ |
| 포스트 수정 | http://127.0.0.1:8000/post/1/edit/ |
| 포스트 삭제 | http://127.0.0.1:8000/post/1/delete/ |
| 회원가입 | http://127.0.0.1:8000/register/ |
| 로그인 | http://127.0.0.1:8000/login/ |
| 로그아웃 | http://127.0.0.1:8000/logout/ |
| 대시보드 | http://127.0.0.1:8000/dashboard/ |
| 관리자 | http://127.0.0.1:8000/admin/ |

---

## ✅ 파일 생성 체크리스트

- [ ] blog/models.py - 수정
- [ ] blog/views.py - 수정
- [ ] blog/urls.py - **새로 생성**
- [ ] myproject/urls.py - 수정
- [ ] myproject/settings.py - 수정
- [ ] blog/admin.py - 수정
- [ ] templates/blog/base.html - 새로 생성
- [ ] templates/blog/home.html - 새로 생성
- [ ] templates/blog/post_list.html - 새로 생성
- [ ] templates/blog/post_detail.html - 새로 생성
- [ ] templates/blog/post_form.html - 새로 생성
- [ ] templates/blog/post_confirm_delete.html - 새로 생성
- [ ] templates/blog/register.html - 새로 생성
- [ ] templates/blog/login.html - 새로 생성
- [ ] templates/blog/dashboard.html - 새로 생성

**모두 완료 후 마이그레이션 및 서버 실행!** 🚀
