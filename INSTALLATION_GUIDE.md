# 🔧 설치 및 실행 가이드

## 필수 사항 확인

### 1️⃣ Python 설치 확인
```bash
python --version
# 결과 예: Python 3.8 이상 필요
```

### 2️⃣ pip 확인
```bash
pip --version
```

---

## 📦 설치 단계

### Step 1: 가상환경 생성 및 활성화

#### Windows
```bash
# 1. 가상환경 생성
python -m venv venv

# 2. 가상환경 활성화
venv\Scripts\activate

# 3. 프롬프트가 (venv)로 시작하면 성공
# 예: (venv) C:\Users\YourName\...>
```

#### Mac/Linux
```bash
# 1. 가상환경 생성
python3 -m venv venv

# 2. 가상환경 활성화
source venv/bin/activate

# 3. 프롬프트에 (venv)가 표시되면 성공
```

### Step 2: 필수 패키지 설치

#### 방법 1: requirements.txt 사용 (권장)
```bash
# DJangGo 폴더에서
pip install -r requirements.txt

# 설치 내용:
# - Django 4.2.0
# - Pillow 10.0.0 (이미지 처리)
```

#### 방법 2: 수동 설치
```bash
# Django 설치
pip install django==4.2.0

# 이미지 처리 라이브러리 (미디어 파일 사용 시)
pip install pillow==10.0.0

# 선택사항: REST API 개발
pip install djangorestframework==3.14.0
```

### Step 3: 설치 확인
```bash
# Django 설치 확인
python -c "import django; print(django.VERSION)"
# 결과: (4, 2, 0, 'final', 0)

# Pillow 설치 확인 (미디어 파일 사용 시)
python -c "from PIL import Image; print('Pillow OK')"
# 결과: Pillow OK
```

---

## 🚀 Django 프로젝트 생성

### Step 1: 프로젝트 생성
```bash
# 프로젝트 생성
django-admin startproject simpleblog

# 프로젝트 폴더로 이동
cd simpleblog
```

### Step 2: 앱 생성
```bash
# blog 앱 생성
python manage.py startapp blog

# pages 앱 생성
python manage.py startapp pages
```

### Step 3: 설정 파일 수정 (settings.py)
```python
# simpleblog/settings.py에서 INSTALLED_APPS 찾기
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    
    # 이 두 줄 추가
    'blog',
    'pages',
]

# 정적 파일 설정 (09단계 필요)
STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'

# 미디어 파일 설정 (09단계 필요)
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'
```

### Step 4: URL 설정 (urls.py)
```python
# simpleblog/urls.py 수정
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('blog/', include('blog.urls')),
    path('pages/', include('pages.urls')),
]

# 개발 환경에서 미디어 파일 서빙
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
```

---

## 📝 코드 복사

### Step 1: 모델 복사 (07단계)

**blog/models.py 복사:**
```
source: c:\DJangGo\07_App_Development\blog\models.py
destination: simpleblog/blog/models.py
```

**pages/models.py 복사:**
```
source: c:\DJangGo\07_App_Development\pages\models.py
destination: simpleblog/pages/models.py
```

### Step 2: 관리자 설정 (선택사항)

**blog/admin.py 작성:**
```python
from django.contrib import admin
from .models import Post, Comment, Category

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ['title', 'author', 'is_published', 'created_at']
    list_filter = ['is_published', 'created_at']
    search_fields = ['title', 'content']
    prepopulated_fields = {'slug': ('title',)}
    readonly_fields = ['created_at', 'updated_at']

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ['author', 'post', 'is_approved', 'created_at']
    list_filter = ['is_approved', 'created_at']
    search_fields = ['author', 'content']

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}
```

### Step 3: 마이그레이션 실행
```bash
# 마이그레이션 파일 생성
python manage.py makemigrations

# 마이그레이션 적용
python manage.py migrate

# 결과: 성공적으로 완료되면 OK
```

### Step 4: 뷰 및 URL 복사 (08단계)

**blog/urls.py 복사:**
```
source: c:\DJangGo\08_Web_Pages\blog_urls.py
destination: simpleblog/blog/urls.py
```

**blog/views.py 복사** (두 가지 중 하나 선택):
```
# 권장: CBV 버전
source: c:\DJangGo\08_Web_Pages\blog_views.py
destination: simpleblog/blog/views.py

# 대안: FBV 버전
source: c:\DJangGo\08_Web_Pages\blog_views_fbv.py
destination: simpleblog/blog/views.py
```

**pages/urls.py와 pages/views.py도 동일하게 복사**

### Step 5: 슈퍼유저 생성
```bash
python manage.py createsuperuser

# 사용자명: admin
# 이메일: admin@example.com
# 비밀번호: (원하는 비밀번호)
```

---

## ✅ 실행 및 테스트

### Step 1: 서버 시작
```bash
python manage.py runserver

# 결과:
# Starting development server at http://127.0.0.1:8000/
# Quit the server with CONTROL-C.
```

### Step 2: 브라우저에서 확인
```
홈: http://127.0.0.1:8000/
관리자: http://127.0.0.1:8000/admin/
```

### Step 3: 관리자 페이지에서 테스트
1. http://127.0.0.1:8000/admin/ 접속
2. 로그인 (위에서 생성한 슈퍼유저)
3. 포스트 생성 테스트
4. 포스트 목록 조회

---

## 🐛 일반적인 오류 및 해결법

### 오류 1: "ModuleNotFoundError: No module named 'django'"
**원인:** Django가 설치되지 않음
**해결:**
```bash
pip install django==4.2.0
```

### 오류 2: "No such table: blog_post"
**원인:** 마이그레이션을 실행하지 않음
**해결:**
```bash
python manage.py migrate
```

### 오류 3: "apps.py not found"
**원인:** 앱이 INSTALLED_APPS에 등록되지 않음
**해결:** settings.py에서 'blog', 'pages' 추가

### 오류 4: "TemplateDoesNotExist"
**원인:** 템플릿 파일이 없음
**해결:**
```
templates/
├── blog/
│   ├── post_list.html
│   └── post_detail.html
└── pages/
    └── home.html
```

### 오류 5: "ModuleNotFoundError: No module named 'PIL'"
**원인:** Pillow가 설치되지 않음 (이미지 처리 사용 시)
**해결:**
```bash
pip install pillow==10.0.0
```

---

## 📊 설치 확인 체크리스트

- [ ] Python 3.8+ 설치됨
- [ ] 가상환경 생성 및 활성화됨
- [ ] Django 4.2.0 설치됨
- [ ] Pillow 설치됨 (옵션)
- [ ] Django 프로젝트 생성됨
- [ ] blog, pages 앱 생성됨
- [ ] models.py 복사됨
- [ ] settings.py 수정됨
- [ ] urls.py 수정됨
- [ ] makemigrations 실행됨
- [ ] migrate 실행됨
- [ ] 슈퍼유저 생성됨
- [ ] runserver 실행 성공
- [ ] 관리자 페이지 로그인 성공

---

## 🎓 다음 단계

1. **기본 기능 확인**
   - [ ] 관리자 페이지에서 포스트 생성
   - [ ] 포스트 목록 페이지 확인
   - [ ] 포스트 상세 페이지 확인

2. **템플릿 추가**
   - [ ] post_list.html 생성
   - [ ] post_detail.html 생성
   - [ ] post_form.html 생성

3. **고급 기능**
   - [ ] 이미지 업로드 (09단계)
   - [ ] 검색 기능
   - [ ] 댓글 기능
   - [ ] 페이지네이션

4. **배포 준비**
   - [ ] DEBUG = False 설정
   - [ ] ALLOWED_HOSTS 설정
   - [ ] 데이터베이스 백업
   - [ ] Gunicorn/Nginx 설정

---

## 💡 유용한 Django 명령어

```bash
# 마이그레이션 상태 확인
python manage.py showmigrations

# 특정 마이그레이션 되돌리기
python manage.py migrate blog 0001

# Django 쉘 (ORM 테스트)
python manage.py shell
>>> from blog.models import Post
>>> Post.objects.all()

# 정적 파일 수집 (프로덕션)
python manage.py collectstatic

# 테스트 실행
python manage.py test

# 데이터베이스 백업
python manage.py dumpdata > backup.json

# 데이터베이스 복구
python manage.py loaddata backup.json
```

---

## ❓ 추가 도움말

### 가상환경 비활성화
```bash
deactivate
```

### 프로젝트 폴더 구조 확인
```bash
# Windows
tree /F simpleblog

# Mac/Linux
find simpleblog -type f | head -20
```

### 로그 파일 확인
```bash
# 모든 로그 보기
python manage.py runserver --verbosity 2
```

---

**행운을 빕니다! 🚀 설치 후 문제가 있으면 위의 오류 해결법을 참고하세요.**

생성 일시: 2024-12-23
마지막 업데이트: 2024-12-23
