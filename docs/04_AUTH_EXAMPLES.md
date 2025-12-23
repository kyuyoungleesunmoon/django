# Django 인증 & 권한 - 실전 예제

## 1. 기본 로그인/로그아웃

### views.py
```python
from django.contrib.auth import authenticate, login, logout

def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            return render(request, 'login.html', {'error': 'Invalid credentials'})
    
    return render(request, 'login.html')

def logout_view(request):
    logout(request)
    return redirect('home')
```

---

## 2. 권한 확인 데코레이터

### 로그인 필수
```python
from django.contrib.auth.decorators import login_required

@login_required(login_url='login')
def create_post(request):
    # 로그인한 사용자만 접근
    return render(request, 'create_post.html')
```

### 특정 권한 필요
```python
from django.contrib.auth.decorators import permission_required

@permission_required('blog.add_post')
def create_post(request):
    # blog.add_post 권한이 있는 사용자만 접근
    return render(request, 'create_post.html')

@permission_required(['blog.add_post', 'blog.change_post'])
def manage_posts(request):
    # 두 권한 모두 필요 (AND)
    pass

@permission_required('blog.delete_post', raise_exception=True)
def delete_post(request):
    # 권한 없으면 403 Forbidden
    pass
```

---

## 3. 소유권 확인

### 자신의 포스트만 수정
```python
from django.shortcuts import get_object_or_404, redirect
from django.http import HttpResponseForbidden

def edit_post(request, pk):
    post = get_object_or_404(Post, pk=pk)
    
    # 소유자만 수정 가능
    if post.author != request.user:
        return HttpResponseForbidden("You don't have permission")
    
    if request.method == 'POST':
        post.title = request.POST['title']
        post.save()
        return redirect('post_detail', pk=pk)
    
    return render(request, 'edit_post.html', {'post': post})
```

### 데코레이터로 간편하게
```python
from functools import wraps

def owner_required(view_func):
    @wraps(view_func)
    def wrapped(request, *args, **kwargs):
        pk = kwargs.get('pk')
        post = get_object_or_404(Post, pk=pk)
        
        if post.author != request.user:
            return HttpResponseForbidden()
        
        return view_func(request, *args, **kwargs)
    return wrapped

@login_required
@owner_required
def delete_post(request, pk):
    post = Post.objects.get(pk=pk)
    post.delete()
    return redirect('post_list')
```

---

## 4. 클래스형 뷰에서의 권한 제어

### LoginRequiredMixin
```python
from django.contrib.auth.mixins import LoginRequiredMixin

class DashboardView(LoginRequiredMixin, TemplateView):
    template_name = 'dashboard.html'
    login_url = 'login'  # 미로그인 시 리다이렉트
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user'] = self.request.user
        return context
```

### PermissionRequiredMixin
```python
from django.contrib.auth.mixins import PermissionRequiredMixin

class CreatePostView(PermissionRequiredMixin, CreateView):
    permission_required = 'blog.add_post'
    raise_exception = True  # 권한 없으면 403
    
    model = Post
    fields = ['title', 'content']
```

### 조건부 권한
```python
class UpdatePostView(LoginRequiredMixin, UpdateView):
    model = Post
    
    def get_object(self):
        obj = super().get_object()
        if obj.author != self.request.user:
            raise PermissionDenied()
        return obj
```

---

## 5. 권한 할당하기

### 단일 권한 할당
```python
from django.contrib.auth.models import User, Permission
from django.contrib.contenttypes.models import ContentType

# 권한 객체 조회
permission = Permission.objects.get(codename='add_post')

# 사용자에게 권한 할당
user = User.objects.get(username='john')
user.user_permissions.add(permission)
```

### 여러 권한 할당
```python
permissions = Permission.objects.filter(
    content_type__app_label='blog',
    codename__in=['add_post', 'change_post', 'delete_post']
)
user.user_permissions.add(*permissions)
```

### 권한 제거
```python
user.user_permissions.remove(permission)
user.user_permissions.clear()
```

---

## 6. 그룹 관리

### 그룹 생성 및 권한 할당
```python
from django.contrib.auth.models import Group

# 그룹 생성
editors = Group.objects.create(name='Editors')

# 권한 할당
permissions = Permission.objects.filter(
    codename__in=['add_post', 'change_post', 'delete_post']
)
editors.permissions.add(*permissions)
```

### 사용자를 그룹에 추가
```python
user = User.objects.get(username='john')
user.groups.add(editors)

# 그룹 확인
user.groups.all()  # [<Group: Editors>]
```

### 그룹의 모든 권한 확인
```python
for group in user.groups.all():
    print(f"Group: {group.name}")
    for perm in group.permissions.all():
        print(f"  - {perm.codename}")
```

---

## 7. 권한 확인하기

### 단일 권한 확인
```python
if user.has_perm('blog.add_post'):
    print("Can add post")
```

### 모듈 권한 확인
```python
if user.has_module_perms('blog'):
    print("Has any blog permission")
```

### 여러 권한 확인 (AND)
```python
if user.has_perms(['blog.add_post', 'blog.change_post']):
    print("Can add and change posts")
```

---

## 8. 템플릿에서의 권한 확인

```html
<!-- 로그인 여부 확인 -->
{% if user.is_authenticated %}
    <p>Welcome, {{ user.username }}!</p>
{% else %}
    <p><a href="{% url 'login' %}">Login</a></p>
{% endif %}

<!-- 특정 권한 확인 -->
{% if perms.blog.add_post %}
    <a href="{% url 'post_create' %}">Create Post</a>
{% endif %}

<!-- 관리자 확인 -->
{% if user.is_staff %}
    <a href="/admin/">Admin Panel</a>
{% endif %}

<!-- 슈퍼유저 확인 -->
{% if user.is_superuser %}
    <p>You have all permissions</p>
{% endif %}
```

---

## 9. 회원가입

### 함수형 뷰
```python
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login

def register(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password1 = request.POST['password1']
        password2 = request.POST['password2']
        
        if password1 != password2:
            return render(request, 'register.html', {'error': 'Passwords do not match'})
        
        if User.objects.filter(username=username).exists():
            return render(request, 'register.html', {'error': 'Username already exists'})
        
        user = User.objects.create_user(username, email, password1)
        
        # 자동 로그인
        login(request, user)
        return redirect('home')
    
    return render(request, 'register.html')
```

---

## 10. 비밀번호 변경

### 비밀번호 변경 뷰
```python
@login_required
def change_password(request):
    if request.method == 'POST':
        old_password = request.POST['old_password']
        new_password1 = request.POST['new_password1']
        new_password2 = request.POST['new_password2']
        
        # 기존 비밀번호 확인
        if not request.user.check_password(old_password):
            return render(request, 'change_password.html', {'error': 'Wrong password'})
        
        if new_password1 != new_password2:
            return render(request, 'change_password.html', {'error': 'Passwords do not match'})
        
        request.user.set_password(new_password1)
        request.user.save()
        
        # 재로그인 필요
        login(request, request.user)
        return redirect('home')
    
    return render(request, 'change_password.html')
```

---

## 11. 커스텀 User 모델

### models.py
```python
from django.contrib.auth.models import AbstractUser

class CustomUser(AbstractUser):
    phone = models.CharField(max_length=15, blank=True)
    avatar = models.ImageField(upload_to='avatars/', blank=True)
    bio = models.TextField(blank=True)
    
    class Meta:
        db_table = 'custom_user'
```

### settings.py
```python
AUTH_USER_MODEL = 'myapp.CustomUser'
```

---

## 12. 활성/비활성 사용자 관리

```python
# 사용자 비활성화
user.is_active = False
user.save()

# 비활성 사용자는 로그인 불가

# 활성 사용자만 필터링
active_users = User.objects.filter(is_active=True)
```

---

## 13. 마지막 로그인 추적

```python
from django.utils import timezone

def login_view(request):
    user = authenticate(request, username=username, password=password)
    if user is not None:
        login(request, user)
        user.last_login = timezone.now()
        user.save()
        return redirect('home')

# 마지막 로그인 시간 확인
print(user.last_login)
```

---

## 14. 세션 보안 설정

### settings.py
```python
# 세션 타임아웃 (1시간)
SESSION_COOKIE_AGE = 3600

# HTTPS만 세션 쿠키 전송
SESSION_COOKIE_SECURE = True

# JavaScript 접근 방지
SESSION_COOKIE_HTTPONLY = True

# CSRF 보호
CSRF_COOKIE_SECURE = True
CSRF_COOKIE_HTTPONLY = True

# SameSite 정책
SESSION_COOKIE_SAMESITE = 'Strict'
CSRF_COOKIE_SAMESITE = 'Strict'
```

---

## 15. 사용자 활동 로깅

```python
from django.contrib.admin.models import LogEntry
from django.contrib.contenttypes.models import ContentType

# 사용자의 모든 활동 조회
user_logs = LogEntry.objects.filter(user=request.user)

for log in user_logs:
    print(f"{log.user} - {log.action_time} - {log.get_change_message()}")
```
