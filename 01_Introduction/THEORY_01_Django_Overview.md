# 01. Django 소개 및 기본 개념

## 1.1 Django란?

### 정의
Django는 **파이썬으로 작성된 오픈소스 웹 프레임워크**입니다. 웹 애플리케이션을 빠르고 안전하게 개발하기 위한 모든 도구와 라이브러리를 제공합니다.

**프레임워크(Framework)란?**
- 건축물을 지을 때 기초, 골조, 배관 등이 미리 준비되어 있듯이
- 웹 개발에 필요한 기본 구조와 도구가 미리 준비되어 있는 것
- 개발자는 이 틀 위에서 자신의 비즈니스 로직만 추가하면 됨

### Django의 역사
- **2005년**: 미국의 신문사 Lawrence Journal-World에서 개발
- **2008년**: 오픈소스로 공개
- **현재**: 가장 인기 있는 파이썬 웹 프레임워크
- **사용 기업**: Instagram, Spotify, Dropbox, Pinterest 등

### Django의 주요 특징

#### 1. Full-Stack 프레임워크
- **Full-Stack**: 웹 개발의 모든 계층을 지원
  - Frontend (HTML, CSS, JavaScript)
  - Backend (Python, 데이터베이스)
  - 둘을 연결하는 모든 것
- 대부분의 웹 개발에 필요한 기능이 이미 포함됨
- 추가 라이브러리 설치 최소화

#### 2. MTV 아키텍처
- **M(Model)**: 데이터베이스와 상호작용
- **T(Template)**: 사용자에게 보여줄 HTML 페이지
- **V(View)**: 요청을 처리하고 응답하는 로직
- 각 부분이 명확하게 분리되어 유지보수가 쉬움

#### 3. ORM (Object-Relational Mapping)
- SQL 쿼리를 직접 작성하지 않고 파이썬 객체로 데이터베이스 조작
- 데이터베이스 종류 변경이 쉬움 (SQLite → PostgreSQL 등)
- SQL 문법을 배우지 않아도 됨

#### 4. Admin Panel
- 관리자 페이지가 자동으로 생성됨
- 데이터 추가, 수정, 삭제를 그래픽 인터페이스로 관리
- 추가 개발 시간 절약

#### 5. 내장 보안 기능
- **CSRF(Cross-Site Request Forgery) 방지**: 악의적인 요청으로부터 보호
- **XSS(Cross-Site Scripting) 방지**: 악성 스크립트 실행 방지
- **SQL Injection 방지**: 데이터베이스 공격 방지
- **비밀번호 암호화**: 저장된 비밀번호 자동 암호화

### Django의 장점

#### 1. 개발 속도 (Batteries Included)
- **Batteries Included**: 필요한 것들이 이미 들어있음
- 빠른 프로토타이핑 가능
- MVP(최소 기능 제품) 개발이 빠름

**예시:**
```
프레임워크 없을 때: 
1. 웹 서버 설정 (2시간)
2. 데이터베이스 설계 (2시간)
3. 사용자 인증 (3시간)
4. 관리자 페이지 (4시간)
= 총 11시간

Django 사용 시:
1. settings.py 설정 (10분)
2. models.py 작성 (20분)
3. 자동으로 사용자 인증 제공
4. 관리자 페이지 자동 생성
= 총 30분
```

#### 2. 재사용 가능한 컴포넌트
- 한번 만든 앱을 다른 프로젝트에서 재사용
- 커뮤니티에서 공유하는 패키지 활용
- 개발 시간 단축

#### 3. 강력한 커뮤니티
- 문제 발생 시 Stack Overflow에서 쉽게 답변 찾기
- 많은 튜토리얼과 가이드 존재
- 빠른 버그 수정 및 업데이트

#### 4. 확장성
- 작은 프로젝트부터 시작 가능
- 프로젝트 커질수록 확장 가능
- 마이크로서비스로 분리 가능

#### 5. 문서
- 공식 문서가 매우 자세함
- 한국어 문서도 많음
- 예제 코드가 풍부함

## 1.2 MTV 아키텍처 (Model-Template-View)

### 개념 설명

Django는 **MTV 아키텍처**를 사용합니다. 이는 MVC(Model-View-Controller) 패턴의 Django식 표현입니다.

#### 비유로 이해하기: 식당 운영

```
고객의 주문 → 웨이터(View) → 주방(Model) → 요리 → 서빙(Template)
```

- **Model**: 요리의 재료와 레시피 (데이터베이스)
- **View**: 웨이터 (주문 처리, 요리 준비 요청)
- **Template**: 예쁜 접시와 나이프포크 (HTML 포장)

### Model (모델) - 데이터 관리

**역할:**
- 데이터베이스의 구조를 정의
- 데이터의 추가, 수정, 삭제, 조회 담당
- 비즈니스 로직 구현

**특징:**
- Python 클래스로 정의
- ORM을 통해 SQL을 작성하지 않고 데이터 조작
- 자동으로 데이터베이스 테이블 생성

**예시:**
```python
# 모델 정의
class Post(models.Model):
    title = models.CharField(max_length=200)      # 제목
    content = models.TextField()                   # 내용
    author = models.ForeignKey(User, ...)          # 작성자
    created_at = models.DateTimeField(auto_now_add=True)  # 생성일

# 모델 사용 (SQL 없이!)
post = Post.objects.create(
    title="첫 글",
    content="내용입니다",
    author=user
)
# 위 코드는 다음 SQL과 같음:
# INSERT INTO blog_post (title, content, author_id, created_at) 
# VALUES ('첫 글', '내용입니다', 1, NOW());
```

### View (뷰) - 요청 처리

**역할:**
- 사용자의 요청을 받음
- 모델에서 데이터를 가져옴
- 템플릿에 데이터를 전달
- 응답(HTML, JSON 등)을 생성

**특징:**
- Python 함수 또는 클래스로 정의
- 데이터 조회, 비즈니스 로직 처리
- 권한 검사, 데이터 검증 등

**뷰의 종류:**

1. **함수형 뷰 (Function-Based View)**
```python
def post_list(request):
    """포스트 목록을 보여주는 뷰"""
    # 1. 모델에서 데이터 조회
    posts = Post.objects.all()
    
    # 2. 데이터를 컨텍스트로 준비
    context = {'posts': posts}
    
    # 3. 템플릿과 데이터를 함께 렌더링
    return render(request, 'blog/post_list.html', context)
```

2. **클래스형 뷰 (Class-Based View) - 권장**
```python
class PostListView(ListView):
    """포스트 목록을 보여주는 뷰"""
    model = Post
    template_name = 'blog/post_list.html'
    context_object_name = 'posts'
```

### Template (템플릿) - HTML 생성

**역할:**
- 데이터를 사용자 친화적인 HTML로 변환
- 뷰에서 전달받은 데이터를 HTML에 삽입
- CSS, JavaScript와 함께 화면 구성

**특징:**
- Django 템플릿 언어 사용 ({{}} 문법)
- for, if 등 프로그래밍 요소 포함
- 필터를 사용한 데이터 변환

**예시:**
```html
<!-- template: post_list.html -->
<h1>블로그 포스트</h1>

{% for post in posts %}
    <article>
        <h2>{{ post.title }}</h2>
        <p>{{ post.content }}</p>
        <p>작성자: {{ post.author.username }}</p>
        <p>작성일: {{ post.created_at|date:"Y-m-d" }}</p>
    </article>
{% endfor %}
```

### MTV 흐름도

```
┌─────────────────────────────────────────────────────────────┐
│                     사용자 (브라우저)                          │
└────────────────────────┬──────────────────────────────────────┘
                         │
                    1. URL 요청
                  (http://blog.com/posts/)
                         │
                         ▼
        ┌────────────────────────────────────┐
        │     2. URL Router (urls.py)         │
        │   어느 뷰를 실행할지 결정            │
        └────────────┬───────────────────────┘
                     │
              3. 해당 뷰 실행
                     │
                     ▼
        ┌────────────────────────────────────┐
        │    4. View (views.py)              │
        │   요청 처리 & 비즈니스 로직         │
        │   ① 모델에 쿼리 날리기             │
        │   ② 데이터 처리                   │
        └────────────┬───────────────────────┘
                     │
                     ▼
        ┌────────────────────────────────────┐
        │    5. Model (models.py)            │
        │   ① 데이터 조회                   │
        │   ② 데이터베이스와 상호작용       │
        └────────────┬───────────────────────┘
                     │
              6. 데이터 반환
                     │
                     ▼
        ┌────────────────────────────────────┐
        │    7. View에서 데이터 처리         │
        │   컨텍스트 데이터 준비             │
        └────────────┬───────────────────────┘
                     │
              8. 템플릿에 전달
                     │
                     ▼
        ┌────────────────────────────────────┐
        │    9. Template (*.html)            │
        │   데이터를 HTML로 변환             │
        │   {{ post.title }}, {% for %} 등   │
        └────────────┬───────────────────────┘
                     │
            10. HTML 생성 완료
                     │
                     ▼
        ┌────────────────────────────────────┐
        │    11. View에서 응답               │
        │    HTML을 HTTP 응답으로 반환      │
        └────────────┬───────────────────────┘
                     │
            12. 브라우저에 전송
                     │
                     ▼
┌─────────────────────────────────────────────────────────────┐
│          사용자 브라우저에서 HTML 렌더링                      │
└─────────────────────────────────────────────────────────────┘
```

### 실제 예: 블로그 포스트 조회

#### 1단계: 사용자 요청
```
사용자: http://blog.com/posts/ 접속
```

#### 2단계: Django 처리

**urls.py에서**
```python
urlpatterns = [
    path('posts/', views.post_list, name='post_list'),
]
# → post_list 뷰 함수 실행
```

**views.py에서**
```python
def post_list(request):
    posts = Post.objects.all()  # ← Model에 요청
    return render(request, 'post_list.html', {'posts': posts})
```

**models.py에서**
```python
class Post(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    
# Post.objects.all() 실행
# → SELECT * FROM blog_post;
```

**post_list.html에서**
```html
{% for post in posts %}
    <h2>{{ post.title }}</h2>
    <p>{{ post.content }}</p>
{% endfor %}
# → <h2>첫 글</h2> <p>내용입니다</p>
```

#### 3단계: 결과
```html
<!DOCTYPE html>
<html>
<body>
    <h2>첫 글</h2>
    <p>내용입니다</p>
    
    <h2>두 번째 글</h2>
    <p>다른 내용</p>
</body>
</html>
```

## 1.2 MTV 아키텍처 (Model-Template-View)

### 개념

```
myproject/               # 프로젝트 폴더
├── manage.py            # Django 관리 스크립트
├── myproject/           # 프로젝트 설정 패키지
│   ├── __init__.py
│   ├── settings.py      # 프로젝트 설정
│   ├── urls.py          # URL 라우팅
│   ├── asgi.py          # ASGI 설정
│   └── wsgi.py          # WSGI 설정
└── myapp/               # 애플리케이션 폴더
    ├── migrations/      # 데이터베이스 마이그레이션
    ├── __init__.py
    ├── admin.py         # Admin 페이지 설정
    ├── apps.py          # 애플리케이션 설정
    ├── models.py        # 데이터 모델
    ├── tests.py         # 테스트 코드
    ├── urls.py          # 앱 URL 라우팅
    ├── views.py         # 뷰 함수/클래스
    └── templates/       # HTML 템플릿 폴더
```

## 1.4 Django 설치 및 프로젝트 생성

### 1단계: Django 설치
```bash
pip install django
```

### 2단계: 프로젝트 생성
```bash
django-admin startproject myproject
```

### 3단계: 앱 생성
```bash
python manage.py startapp myapp
```

### 4단계: 마이그레이션 수행
```bash
python manage.py migrate
```

### 5단계: 개발 서버 실행
```bash
python manage.py runserver
```

## 1.5 요청-응답 순서

1. **사용자 요청** → 브라우저에서 URL 요청
2. **URL 라우팅** → urls.py에서 URL을 뷰에 매핑
3. **뷰 처리** → 뷰 함수/클래스에서 비즈니스 로직 처리
4. **모델 접근** → 필요한 데이터를 모델을 통해 조회
5. **템플릿 렌더링** → 데이터를 템플릿에 전달하여 HTML 생성
6. **응답 반환** → 렌더링된 HTML을 클라이언트에 반환

## 1.6 주요 파일별 역할

| 파일 | 역할 |
|------|------|
| settings.py | 프로젝트 설정 (DB, 설치된 앱, 미들웨어 등) |
| urls.py | URL 패턴과 뷰 매핑 |
| views.py | 요청 처리 로직 |
| models.py | 데이터 모델 정의 |
| templates/ | HTML 템플릿 |
| static/ | CSS, JS, 이미지 등 정적 파일 |
| manage.py | 프로젝트 관리 커맨드 |

이제 실제 프로젝트를 만들어보겠습니다!
