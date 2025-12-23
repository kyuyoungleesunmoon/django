# Django 인증 & 권한 가이드

## 1. Django 인증 시스템 개요

### 1.1 기본 개념
- **Authentication**: 사용자가 본인이 맞는지 확인 (로그인)
- **Authorization**: 인증된 사용자가 무엇을 할 수 있는지 제어 (권한)
- **Permission**: 특정 작업을 수행할 수 있는 권한
- **Group**: 여러 Permission을 묶은 그룹

### 1.2 Django User 모델
```python
from django.contrib.auth.models import User

# 기본 필드
user.username      # 사용자명
user.email         # 이메일
user.first_name    # 이름
user.last_name     # 성
user.password      # 암호화된 비밀번호
user.is_active     # 활성화 여부
user.is_staff      # 관리자 여부
user.is_superuser  # 슈퍼유저 여부
```

---

## 2. 사용자 생성 및 관리

### 2.1 사용자 생성
```python
from django.contrib.auth.models import User

# 일반 사용자
user = User.objects.create_user(
    username='john',
    email='john@example.com',
    password='password123'
)

# 관리자
admin = User.objects.create_superuser(
    username='admin',
    email='admin@example.com',
    password='admin123'
)
```

### 2.2 비밀번호 관리
```python
# 비밀번호 변경
user.set_password('new_password')
user.save()

# 비밀번호 확인
user.check_password('some_password')  # True/False

# 임의의 비밀번호 생성
from django.contrib.auth.models import User
User.objects.make_random_password()
```

---

## 3. 권한(Permission) 시스템

### 3.1 권한 종류
```python
# Django가 자동으로 생성하는 권한
- add_<modelname>      # 추가 권한
- change_<modelname>   # 수정 권한
- delete_<modelname>   # 삭제 권한
- view_<modelname>     # 조회 권한
```

### 3.2 권한 할당
```python
from django.contrib.auth.models import Permission, User
from django.contrib.contenttypes.models import ContentType
from myapp.models import Post

# 권한 객체 조회
permission = Permission.objects.get(codename='add_post')

# 사용자에게 권한 할당
user.user_permissions.add(permission)

# 여러 권한 할당
permissions = Permission.objects.filter(
    content_type__app_label='myapp',
    codename__in=['add_post', 'change_post']
)
user.user_permissions.add(*permissions)

# 권한 제거
user.user_permissions.remove(permission)

# 모든 권한 제거
user.user_permissions.clear()
```

### 3.3 권한 확인
```python
# 단일 권한 확인
user.has_perm('myapp.add_post')
user.has_perm('myapp.change_post')

# 여러 권한 확인 (AND)
user.has_perms(['myapp.add_post', 'myapp.change_post'])

# 모듈 권한 확인
user.has_module_perms('myapp')
```

---

## 4. 그룹(Group) 관리

### 4.1 그룹 생성
```python
from django.contrib.auth.models import Group, Permission

# 그룹 생성
editors = Group.objects.create(name='Editors')

# 권한 할당
permissions = Permission.objects.filter(
    codename__in=['add_post', 'change_post', 'delete_post']
)
editors.permissions.add(*permissions)
```

### 4.2 사용자를 그룹에 추가
```python
user.groups.add(editors)
user.groups.remove(editors)
user.groups.clear()
```

### 4.3 그룹의 모든 권한 확인
```python
# 사용자가 속한 그룹의 권한
user.groups.all()
for group in user.groups.all():
    print(group.permissions.all())
```

---

## 5. 뷰에서 인증/권한 제어

### 5.1 로그인/로그아웃
```python
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import redirect

def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
    return render(request, 'login.html')

def logout_view(request):
    logout(request)
    return redirect('home')
```

### 5.2 인증 확인
```python
from django.contrib.auth.decorators import login_required

@login_required
def dashboard(request):
    # request.user: 현재 사용자
    return render(request, 'dashboard.html')

# 클래스형 뷰
from django.contrib.auth.mixins import LoginRequiredMixin

class DashboardView(LoginRequiredMixin, TemplateView):
    template_name = 'dashboard.html'
    login_url = 'login'
```

### 5.3 권한 확인
```python
from django.contrib.auth.decorators import permission_required

@permission_required('myapp.add_post')
def create_post(request):
    return render(request, 'create_post.html')

# 여러 권한 확인 (AND)
@permission_required(['myapp.add_post', 'myapp.change_post'])
def manage_posts(request):
    pass

# OR 연산
@permission_required('myapp.add_post', raise_exception=True)
def create_post(request):
    pass
```

### 5.4 클래스형 뷰에서 권한 제어
```python
from django.contrib.auth.mixins import PermissionRequiredMixin

class CreatePostView(PermissionRequiredMixin, CreateView):
    permission_required = 'myapp.add_post'
    raise_exception = True
    
    model = Post
    fields = ['title', 'content']
```

---

## 6. 커스텀 User 모델

### 6.1 커스텀 User 모델 생성
```python
from django.contrib.auth.models import AbstractUser

class CustomUser(AbstractUser):
    phone = models.CharField(max_length=15, blank=True)
    avatar = models.ImageField(upload_to='avatars/', blank=True)
    bio = models.TextField(blank=True)
    
    class Meta:
        db_table = 'custom_user'
```

### 6.2 settings.py에 설정
```python
AUTH_USER_MODEL = 'myapp.CustomUser'
```

---

## 7. 권한 데코레이터 패턴

### 7.1 사용자 소유 객체만 수정
```python
from django.shortcuts import get_object_or_404
from django.http import HttpResponseForbidden

def edit_post(request, pk):
    post = get_object_or_404(Post, pk=pk)
    
    # 소유자 확인
    if post.author != request.user:
        return HttpResponseForbidden("You don't have permission")
    
    # 수정 처리
    if request.method == 'POST':
        post.title = request.POST['title']
        post.save()
        return redirect('post_detail', pk=pk)
    
    return render(request, 'edit_post.html', {'post': post})
```

### 7.2 커스텀 권한 데코레이터
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
    post = get_object_or_404(Post, pk=pk)
    post.delete()
    return redirect('post_list')
```

---

## 8. 세션 및 토큰 인증

### 8.1 세션 기반 인증
```python
# Django 기본값 - 쿠키 기반 세션
SESSION_COOKIE_AGE = 1209600  # 2주
SESSION_COOKIE_SECURE = True  # HTTPS만
SESSION_COOKIE_HTTPONLY = True  # JS 접근 방지
CSRF_COOKIE_SECURE = True
```

### 8.2 토큰 기반 인증 (REST API)
```python
from rest_framework.authtoken.models import Token

# 사용자 생성 시 자동으로 토큰 생성
from django.db.models.signals import post_save
from django.dispatch import receiver

@receiver(post_save, sender=User)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)
```

---

## 9. 권한 체크리스트

- ✅ 민감한 페이지는 `@login_required`로 보호
- ✅ 특정 권한 필요 시 `@permission_required` 사용
- ✅ 사용자 소유 객체는 소유권 확인 필수
- ✅ 비밀번호는 평문 저장 금지
- ✅ CSRF 토큰 사용
- ✅ HTTPS 사용 (프로덕션)
- ✅ 권한 레벨 최소화 원칙 적용
