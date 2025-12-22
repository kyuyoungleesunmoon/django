# Django 간단한 사이트 실습 프로젝트 설정 가이드

## 프로젝트명: SimpleBlog

이 프로젝트는 Django를 학습하기 위한 간단한 블로그 사이트입니다.

## 실습 단계

### 1단계: Django 및 필수 패키지 설치

```bash
# Python 가상환경 생성
python -m venv venv

# 가상환경 활성화 (Windows)
venv\Scripts\activate

# Django 설치
pip install django==4.2
pip install pillow  # 이미지 처리용
```

### 2단계: Django 프로젝트 생성

```bash
# 프로젝트 생성
django-admin startproject simpleblog

# 프로젝트 폴더로 이동
cd simpleblog

# 초기 마이그레이션 수행
python manage.py migrate

# 개발 서버 실행
python manage.py runserver
```

브라우저에서 `http://127.0.0.1:8000/` 접속하면 Django 기본 페이지가 보입니다.

### 3단계: 슈퍼유저(관리자) 생성

```bash
python manage.py createsuperuser
# 사용자명: admin
# 이메일: admin@example.com
# 비밀번호: 원하는 비밀번호 입력

# 관리자 페이지: http://127.0.0.1:8000/admin/
```

### 4단계: 첫 번째 앱 생성 및 등록

```bash
# blog 앱 생성
python manage.py startapp blog

# pages 앱 생성
python manage.py startapp pages
```

**simpleblog/settings.py** 수정:
```python
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'blog',        # 추가
    'pages',       # 추가
]
```

이제 07 단계로 넘어가서 앱 개발을 시작합니다!
