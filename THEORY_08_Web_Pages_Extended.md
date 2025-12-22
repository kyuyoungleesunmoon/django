# 08 레벨 - 웹 페이지 구축 (URLs과 Views)

## 목차
1. URL 라우팅의 개념
2. URL 패턴 정의
3. 함수 기반 뷰(FBV)
4. 클래스 기반 뷰(CBV)
5. 뷰 기본 구조와 실전 예제
6. URL 리버싱과 네임스페이스

---

## 1. URL 라우팅의 개념

### 1.1 URL 라우팅이란?
사용자가 특정 URL을 방문하면, Django가 **적절한 뷰를 찾아 실행**하는 과정입니다.

```
사용자 요청 (URL)
    ↓
URL 패턴 매칭
    ↓
뷰 함수/클래스 실행
    ↓
템플릿 렌더링
    ↓
HTML 응답
```

### 1.2 URL 설정 계층

```
url 요청: /blog/post/django-orm/
    ↓
simpleblog/urls.py (메인 URL)
    ↓
blog/urls.py (앱 URL)
    ↓
해당 뷰 실행
```

---

## 2. URL 패턴 정의

### 2.1 메인 URL 설정 (simpleblog/urls.py)

```python
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('blog/', include('blog.urls')),      # blog 앱의 URL 포함
    path('pages/', include('pages.urls')),    # pages 앱의 URL 포함
    path('', include('pages.urls')),          # 루트 URL도 pages 사용
]
```

### 2.2 앱 URL 설정 (blog/urls.py)

```python
from django.urls import path
from . import views

app_name = 'blog'  # URL 네임스페이스

urlpatterns = [
    # blog/ → 포스트 목록
    path('', views.PostListView.as_view(), name='post-list'),
    
    # blog/post/<slug>/ → 포스트 상세
    path('post/<slug:slug>/', views.PostDetailView.as_view(), name='post-detail'),
    
    # blog/post/new/ → 새 포스트 작성
    path('post/new/', views.PostCreateView.as_view(), name='post-create'),
    
    # blog/post/<slug>/edit/ → 포스트 수정
    path('post/<slug:slug>/edit/', views.PostUpdateView.as_view(), name='post-update'),
    
    # blog/post/<slug>/delete/ → 포스트 삭제
    path('post/<slug:slug>/delete/', views.PostDeleteView.as_view(), name='post-delete'),
]
```

### 2.3 URL 패턴 문법

```python
# 경로만 (변수 없음)
path('', views.home, name='home')

# 문자열 변수 (슬래시 제외)
path('post/<slug>/', views.post_detail, name='post-detail')
path('user/<str:username>/', views.user_profile, name='user-profile')

# 정수 변수
path('post/<int:post_id>/', views.post_detail, name='post-detail')

# UUID 변수
path('post/<uuid:post_id>/', views.post_detail, name='post-detail')

# 슬러그 변수 (문자, 숫자, 하이픈, 언더스코어만)
path('post/<slug:slug>/', views.post_detail, name='post-detail')

# 경로 변수 (슬래시 포함)
path('files/<path:file_path>/', views.download_file, name='download')

# 정규식 (re_path 사용)
from django.urls import re_path
re_path(r'^post/(?P<year>\d{4})/$', views.posts_by_year, name='posts-by-year')
```

---

## 3. 함수 기반 뷰(FBV)

### 3.1 기본 구조

```python
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from .models import Post

def post_list(request):
    """모든 포스트 목록 표시"""
    posts = Post.objects.filter(is_published=True)
    
    return render(request, 'blog/post_list.html', {
        'posts': posts
    })

def post_detail(request, slug):
    """특정 포스트 상세 표시"""
    post = get_object_or_404(Post, slug=slug)
    
    # 조회수 증가
    post.views += 1
    post.save()
    
    return render(request, 'blog/post_detail.html', {
        'post': post
    })
```

### 3.2 FBV의 핵심 요소

```python
def my_view(request):
    """
    request: HttpRequest 객체
      - request.method: 요청 방식 ('GET', 'POST')
      - request.GET: URL 파라미터
      - request.POST: 폼 데이터
      - request.user: 현재 사용자
      - request.FILES: 업로드 파일
    """
    
    if request.method == 'POST':
        # POST 요청 처리
        title = request.POST.get('title')
        return HttpResponse('저장되었습니다')
    else:
        # GET 요청 처리
        return render(request, 'template.html', {})
```

### 3.3 FBV 데코레이터

```python
from django.contrib.auth.decorators import login_required, permission_required
from django.http import HttpResponseForbidden

# 로그인 필수
@login_required
def create_post(request):
    # 로그인한 사용자만 접근
    post = Post.objects.create(
        title=request.POST.get('title'),
        author=request.user
    )
    return render(request, 'post_created.html')

# 권한 확인
@permission_required('blog.add_post')
def another_view(request):
    pass

# 커스텀 데코레이터
def require_ajax(view_func):
    def wrapper(request, *args, **kwargs):
        if not request.is_ajax():
            return HttpResponseForbidden()
        return view_func(request, *args, **kwargs)
    return wrapper

@require_ajax
def api_endpoint(request):
    pass
```

---

## 4. 클래스 기반 뷰(CBV)

### 4.1 CBV란?
CBV는 함수 대신 **Python 클래스**로 뷰를 구현하는 방식입니다.

**장점:**
- 코드 재사용성 높음
- 상속으로 기능 확장 쉬움
- 일관된 구조

### 4.2 기본 CBV들

#### ListView - 목록 표시
```python
from django.views.generic import ListView
from .models import Post

class PostListView(ListView):
    model = Post                           # 사용할 모델
    context_object_name = 'posts'          # 템플릿에서 사용할 변수명
    template_name = 'blog/post_list.html'  # 템플릿 경로
    paginate_by = 10                       # 페이지당 항목 수
    
    def get_queryset(self):
        """쿼리셋 커스터마이징"""
        return Post.objects.filter(is_published=True).order_by('-created_at')
    
    def get_context_data(self, **kwargs):
        """추가 컨텍스트 데이터"""
        context = super().get_context_data(**kwargs)
        context['featured_posts'] = Post.objects.filter(is_featured=True)[:3]
        return context

# URL 설정
urlpatterns = [
    path('', PostListView.as_view(), name='post-list'),
]

# 템플릿에서 사용
# {% for post in posts %}
#     {{ post.title }}
# {% endfor %}
```

#### DetailView - 상세 표시
```python
from django.views.generic import DetailView

class PostDetailView(DetailView):
    model = Post
    context_object_name = 'post'
    template_name = 'blog/post_detail.html'
    slug_field = 'slug'              # URL에서 사용할 필드
    slug_url_kwarg = 'slug'          # URL 파라미터 이름
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        post = self.get_object()
        context['comments'] = post.comments.all()
        return context

# URL 설정
urlpatterns = [
    path('post/<slug:slug>/', PostDetailView.as_view(), name='post-detail'),
]
```

#### CreateView - 생성 폼
```python
from django.views.generic import CreateView
from django.urls import reverse_lazy

class PostCreateView(CreateView):
    model = Post
    fields = ['title', 'content', 'excerpt']  # 폼에 표시할 필드
    template_name = 'blog/post_form.html'
    success_url = reverse_lazy('blog:post-list')
    
    def form_valid(self, form):
        """폼이 유효할 때 실행"""
        form.instance.author = self.request.user
        return super().form_valid(form)

# 사용 권한 제한
from django.contrib.auth.mixins import LoginRequiredMixin

class PostCreateView(LoginRequiredMixin, CreateView):
    # 로그인한 사용자만 접근 가능
    model = Post
    fields = ['title', 'content']
    success_url = reverse_lazy('blog:post-list')
```

#### UpdateView - 수정
```python
from django.views.generic import UpdateView

class PostUpdateView(UpdateView):
    model = Post
    fields = ['title', 'content']
    template_name = 'blog/post_form.html'
    slug_field = 'slug'
    slug_url_kwarg = 'slug'
    
    def get_success_url(self):
        """저장 후 이동할 URL"""
        return reverse('blog:post-detail', kwargs={'slug': self.object.slug})
```

#### DeleteView - 삭제
```python
from django.views.generic import DeleteView

class PostDeleteView(DeleteView):
    model = Post
    template_name = 'blog/post_confirm_delete.html'
    success_url = reverse_lazy('blog:post-list')
    slug_field = 'slug'
    slug_url_kwarg = 'slug'
```

### 4.3 Mixin - CBV 확장

```python
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin

# 로그인 필수 Mixin
class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    fields = ['title', 'content']

# 권한 확인 Mixin
class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    fields = ['title', 'content']
    
    def test_func(self):
        """조건 확인"""
        post = self.get_object()
        return self.request.user == post.author

# 커스텀 Mixin
class OwnerMixin:
    """소유자만 접근 가능"""
    def test_func(self):
        obj = self.get_object()
        return obj.author == self.request.user

class PostUpdateView(LoginRequiredMixin, OwnerMixin, UserPassesTestMixin, UpdateView):
    model = Post
    fields = ['title', 'content']
```

---

## 5. URL 리버싱

### 5.1 URL 리버싱이란?
URL 패턴 이름을 사용해 **URL을 역으로 생성**하는 기능입니다.

```python
# URLs에서 이름 설정
urlpatterns = [
    path('post/<slug:slug>/', views.post_detail, name='post-detail'),
]

# 뷰에서 사용
from django.urls import reverse

def some_view(request):
    url = reverse('blog:post-detail', kwargs={'slug': 'django-orm'})
    # 결과: '/blog/post/django-orm/'

# 템플릿에서 사용
{% url 'blog:post-detail' slug=post.slug %}
<!-- 결과: /blog/post/django-orm/ -->

# Redirect에서 사용
from django.shortcuts import redirect
from django.urls import reverse_lazy

def create_post(request):
    post = Post.objects.create(title='New Post')
    return redirect('blog:post-detail', slug=post.slug)
```

### 5.2 네임스페이스(Namespace)

```python
# blog/urls.py
app_name = 'blog'  # 네임스페이스 설정

urlpatterns = [
    path('', views.post_list, name='post-list'),
    path('post/<slug:slug>/', views.post_detail, name='post-detail'),
]

# 사용
url = reverse('blog:post-detail', kwargs={'slug': 'django'})

# 템플릿에서
{% url 'blog:post-detail' slug=post.slug %}
```

---

## 6. 실전 예제

### 6.1 검색 기능이 있는 포스트 목록

```python
from django.views.generic import ListView
from django.db.models import Q

class PostListView(ListView):
    model = Post
    paginate_by = 10
    
    def get_queryset(self):
        queryset = Post.objects.filter(is_published=True)
        
        # GET 파라미터에서 검색어 가져오기
        search = self.request.GET.get('search')
        if search:
            queryset = queryset.filter(
                Q(title__icontains=search) |
                Q(content__icontains=search)
            )
        
        return queryset.order_by('-created_at')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['search'] = self.request.GET.get('search', '')
        return context

# 템플릿에서
<form method="get">
    <input type="text" name="search" value="{{ search }}">
    <button>검색</button>
</form>
```

### 6.2 권한 확인하는 포스트 수정

```python
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.http import Http404

class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    fields = ['title', 'content']
    slug_field = 'slug'
    slug_url_kwarg = 'slug'
    
    def test_func(self):
        """포스트 작성자인지 확인"""
        post = self.get_object()
        return post.author == self.request.user
    
    def handle_no_permission(self):
        """권한 없을 때 처리"""
        raise Http404("수정 권한이 없습니다")
```

---

## 요약

| 항목 | FBV | CBV |
|-----|-----|-----|
| 문법 | 함수 | 클래스 |
| 코드량 | 적음 | 많음 |
| 재사용성 | 낮음 | 높음 |
| 확장성 | 낮음 | 높음 |
| 커스터마이징 | 자유로움 | 정형화됨 |

**선택 기준:**
- 간단한 기능 → FBV
- 복잡한 기능, 재사용 예상 → CBV

다음 레벨: **09 - 정적/미디어 파일 관리**
