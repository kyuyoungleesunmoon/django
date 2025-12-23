# Django 블로그 프로젝트 - 실행 가이드

## 📋 프로젝트 구조

```
myproject/
├── manage.py              # Django 관리 스크립트
├── myproject/
│   ├── __init__.py
│   ├── settings.py        # 설정 파일
│   ├── urls.py            # URL 라우팅
│   └── wsgi.py            # WSGI 설정
├── blog/                  # 블로그 앱
│   ├── models.py          # 데이터베이스 모델
│   ├── views.py           # 뷰 (CRUD 로직)
│   ├── urls.py            # 앱 URL
│   ├── forms.py           # 폼
│   ├── admin.py           # 관리자 페이지
│   ├── signals.py         # Django 시그널
│   └── apps.py            # 앱 설정
└── templates/
    └── blog/              # HTML 템플릿
        ├── base.html
        ├── home.html
        ├── post_list.html
        ├── post_detail.html
        ├── post_form.html
        ├── login.html
        ├── register.html
        └── dashboard.html
```

---

## 🚀 시작하기

### 1. 환경 설정

```bash
# 터미널에서 프로젝트 디렉토리로 이동
cd c:\DJangGo

# 가상환경 생성 (선택사항이지만 권장)
python -m venv venv

# 가상환경 활성화
venv\Scripts\activate  # Windows
source venv/bin/activate  # Mac/Linux

# 패키지 설치
pip install -r requirements.txt
```

### 2. 마이그레이션 (데이터베이스 생성)

```bash
# 마이그레이션 파일 생성
python myproject/manage.py makemigrations

# 마이그레이션 실행
python myproject/manage.py migrate
```

### 3. 관리자 계정 생성

```bash
python myproject/manage.py createsuperuser
```

대화형으로 다음 정보를 입력하세요:
- 사용자명: admin
- 이메일: admin@example.com
- 비밀번호: (원하는 비밀번호)

### 4. 서버 실행

```bash
python myproject/manage.py runserver
```

브라우저에서 http://127.0.0.1:8000 접속

---

## 🛠️ 개발 팁

### 관리자 페이지 (http://127.0.0.1:8000/admin/)

1. 계정으로 로그인
2. Category, Tag, Post 등의 데이터를 직접 관리할 수 있습니다.

### 테스트 데이터 생성

```bash
# Django shell 진입
python myproject/manage.py shell
```

```python
from django.contrib.auth.models import User
from blog.models import Category, Tag, Post
from datetime import datetime

# 사용자 생성
user = User.objects.create_user('testuser', 'test@example.com', 'password123')

# 카테고리 생성
category = Category.objects.create(
    name='Django',
    slug='django',
    description='Django 관련 포스트'
)

# 태그 생성
tag1 = Tag.objects.create(name='ORM', slug='orm')
tag2 = Tag.objects.create(name='Auth', slug='auth')

# 포스트 생성
post = Post.objects.create(
    title='Django ORM 심화 학습',
    slug='django-orm',
    author=user,
    category=category,
    excerpt='Django ORM에 대한 깊이있는 학습',
    content='아주 긴 본문 내용...',
    status='published',
    is_featured=True
)

# ManyToMany 추가
post.tags.add(tag1, tag2)

# 쿼리 예제
print(Post.objects.filter(author=user))
```

---

## 📚 주요 기능

### ✅ CRUD 작업
- **Create (생성)**: POST 작성
- **Read (읽기)**: 포스트 목록 및 상세 페이지
- **Update (수정)**: 자신의 포스트 수정
- **Delete (삭제)**: 자신의 포스트 삭제

### ✅ Django ORM 심화
- 다대일 관계 (ForeignKey)
- 다대다 관계 (ManyToManyField)
- 일대일 관계 (OneToOneField)
- 자기참조 (Self-reference) - 대댓글
- select_related 최적화
- prefetch_related 최적화
- 집계 함수 (Count, Sum, Avg)
- Q 객체로 복잡한 쿼리 작성

### ✅ 인증 & 권한
- 회원가입 & 로그인
- 권한 기반 접근 제어
- 포스트 소유자만 수정/삭제 가능
- 댓글 관리 (작성자 또는 포스트 작성자만 삭제)
- 좋아요, 북마크 기능 (로그인 필요)

### ✅ 고급 기능
- 포스트 통계 (조회수, 좋아요, 댓글, 북마크)
- Django 시그널로 자동 통계 업데이트
- 검색 및 필터링
- 카테고리별 포스트
- 태그별 포스트
- 사용자 대시보드

---

## 🔐 보안 고려사항

1. **CSRF 보호**: 모든 POST 폼에 {% csrf_token %} 포함
2. **로그인 필요**: @login_required 데코레이터 사용
3. **권한 확인**: 소유권 확인 후 수정/삭제 허용
4. **SQL Injection 방지**: Django ORM 사용으로 자동 방지
5. **프로덕션 설정**:
   ```python
   DEBUG = False
   ALLOWED_HOSTS = ['yourdomain.com']
   SECRET_KEY = 'generate-secure-key'
   SECURE_HSTS_SECONDS = 31536000
   SESSION_COOKIE_SECURE = True
   CSRF_COOKIE_SECURE = True
   ```

---

## 🐛 트러블슈팅

### ModuleNotFoundError
```bash
pip install -r requirements.txt
```

### 마이그레이션 오류
```bash
python myproject/manage.py migrate --fake blog zero
python myproject/manage.py makemigrations
python myproject/manage.py migrate
```

### 포트 충돌
```bash
python myproject/manage.py runserver 8001
```

---

## 📖 참고 자료

- Django 공식 문서: https://docs.djangoproject.com/
- Django ORM 쿼리: https://docs.djangoproject.com/en/stable/topics/db/models/
- Django 인증: https://docs.djangoproject.com/en/stable/topics/auth/

---

## 🎓 학습 포인트

### Django ORM
- 모델 정의 및 관계 설정
- 최적화 쿼리 작성 (select_related, prefetch_related)
- 복잡한 필터링 (Q 객체)
- 집계 및 annotation
- 시그널 활용

### 인증 & 권한
- User 모델 활용
- 권한 설정 및 확인
- 데코레이터 사용
- 세션 관리
- 소유권 기반 접근 제어

### 웹 개발
- 클래스형 뷰 (CBV)
- 함수형 뷰
- 폼 처리
- AJAX 요청
- 템플릿 상속
