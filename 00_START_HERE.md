# Django 학습 프로젝트 완전 가이드

## 📌 프로젝트 개요

이 프로젝트는 **Django를 처음부터 배우는 학생들을 위한 종합 학습 자료**입니다.

- ✅ 이론 + 실습 코드 포함
- ✅ 단계별 체계적 학습
- ✅ 즉시 사용 가능한 코드
- ✅ 상세한 주석 및 설명

---

## 🎯 학습 구성

### 📚 01단계: Django 기본 개념
**위치:** `01_Introduction/`

학습 내용:
- Django란 무엇인가
- MTV 아키텍처
- 프로젝트 구조
- 초기 설정

필수 파일:
- `THEORY_01_Django_Overview.md` - 이론
- `PROJECT_SETUP.md` - 프로젝트 생성

---

### 🏢 07단계: 앱 개발하기
**위치:** `07_App_Development/`

#### 07-1 블로그 앱과 페이지 앱 만들기
- 앱 생성 방법
- 앱 구조 이해
- 앱 등록

#### 07-2 데이터베이스 개념 이해하기
- RDBMS 이해
- 테이블, 행, 열
- ORM 개념
- Primary Key, Foreign Key

#### 07-3 모델 만들기
- 필드 타입
- 필드 옵션
- 모델 작성

**실습 코드:**
```
blog/
├── models.py          ← Post, Comment, Category 모델
├── admin.py          ← 관리자 설정
└── ...

pages/
├── models.py          ← Page, About, Contact 모델
├── admin.py          ← 관리자 설정
└── ...
```

**마이그레이션:**
```bash
python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser
```

---

### 🌐 08단계: 웹 페이지 만들기
**위치:** `08_Web_Pages/`

#### 08-1 URL 설정하기
- URL 패턴 작성
- 경로 컨버터
- URL 역참조

#### 08-2 FBV (Function-Based View)
- 함수형 뷰 작성
- 데코레이터 사용
- 요청/응답 처리

#### 08-3 CBV (Class-Based View) - 권장
- 클래스형 뷰
- Generic CBV
- Mixin 활용

**파일 구조:**
```
blog/
├── urls.py           ← blog_urls.py 참고
├── views.py          ← blog_views.py 참고
└── templates/
    └── blog/
        ├── post_list.html
        ├── post_detail.html
        └── post_form.html

pages/
├── urls.py           ← pages_urls.py 참고
├── views.py          ← pages_views.py 참고
└── templates/
    └── pages/
        ├── home.html
        ├── about.html
        └── contact.html
```

---

### 📁 09단계: 정적 파일과 미디어 파일 관리
**위치:** `09_Static_Media/`

#### 09-1 정적 파일 관리하기
- CSS, JavaScript, 이미지
- static/ 구조
- settings.py 설정
- collectstatic (프로덕션)

#### 09-2 미디어 파일 관리하기
- 사용자 업로드 파일
- ImageField, FileField
- 파일 유효성 검사
- 보안 고려

**디렉토리 구조:**
```
project/
├── static/              ← 정적 파일
│   ├── css/
│   ├── js/
│   └── images/
├── media/               ← 업로드 파일
│   ├── blog/
│   └── users/
└── ...
```

**설정 코드:**
```python
# settings.py
STATIC_URL = '/static/'
STATICFILES_DIRS = [BASE_DIR / 'static']
STATIC_ROOT = BASE_DIR / 'staticfiles'

MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'
```

---

### 🎨 10단계: 페이지 구성 개선하기
**위치:** `10_Page_Improvement/`

#### 10-1 포스트 목록 페이지의 문제 파악하기
- 콘텐츠 길이 문제
- 날짜 형식
- 이미지 없을 때 처리
- 빈 목록 처리

#### 10-2 템플릿에서 if 문 사용하기
- 조건부 렌더링
- 변수 존재 여부
- 불린 확인
- 복합 조건

**예제:**
```html
{% if post.image %}
    <img src="{{ post.image.url }}" alt="{{ post.title }}">
{% else %}
    <img src="{% static 'blog/images/default.png' %}">
{% endif %}

{% if post.views > 1000 %}
    <span class="badge">HOT</span>
{% elif post.views > 100 %}
    <span class="badge">POPULAR</span>
{% endif %}

{% if posts %}
    <!-- 포스트 표시 -->
{% else %}
    <p>포스트가 없습니다</p>
{% endif %}
```

#### 10-3 템플릿 필터 사용하기
- 날짜 필터: `date`, `timesince`
- 숫자 필터: `intcomma`, `floatformat`
- 문자 필터: `truncatewords`, `upper`
- 커스텀 필터 작성

**주요 필터:**
```html
{{ post.created_at|date:"Y-m-d" }}
{{ post.created_at|time_ago }}
{{ post.views|intcomma }}
{{ post.content|truncatewords:30 }}
{{ post.title|upper }}
```

**커스텀 필터 위치:**
```
blog/
├── templatetags/
│   ├── __init__.py
│   └── blog_filters.py  ← 10_Page_Improvement/blog_filters.py 참고
└── ...
```

---

## 📂 전체 디렉토리 구조

```
DJangGo/
│
├── README.md                  ← 종합 가이드 (메인)
├── GUIDE.md                   ← 빠른 참조 가이드
│
├── 01_Introduction/           ← 01단계: Django 기본
│   ├── THEORY_01_Django_Overview.md
│   └── PROJECT_SETUP.md
│
├── 07_App_Development/        ← 07단계: 앱 개발
│   ├── THEORY_07_App_Development.md
│   ├── blog/
│   │   └── models.py
│   └── pages/
│       └── models.py
│
├── 08_Web_Pages/              ← 08단계: 웹 페이지
│   ├── THEORY_08_Web_Pages.md
│   ├── blog_urls.py
│   ├── blog_views.py          (CBV 버전)
│   ├── blog_views_fbv.py      (FBV 버전)
│   ├── pages_urls.py
│   └── pages_views.py
│
├── 09_Static_Media/           ← 09단계: 정적/미디어 파일
│   ├── THEORY_09_Static_Media.md
│   ├── settings_static_media.py
│   ├── urls_example.py
│   ├── models_with_media.py
│   └── forms_example.py
│
├── 10_Page_Improvement/       ← 10단계: 페이지 개선
│   ├── THEORY_10_Page_Improvement.md
│   ├── blog_filters.py
│   └── post_list_improved.html
│
└── Template_Examples/         ← 실전 템플릿
    ├── post_list.html
    ├── post_detail.html
    └── post_form.html
```

---

## 🚀 빠른 시작

### 1️⃣ 환경 설정
```bash
# 가상환경 생성
python -m venv venv

# 가상환경 활성화 (Windows)
venv\Scripts\activate

# Django 설치
pip install django==4.2 pillow
```

### 2️⃣ 프로젝트 생성
```bash
django-admin startproject simpleblog
cd simpleblog
python manage.py startapp blog
python manage.py startapp pages
```

### 3️⃣ 설정 수정
```python
# simpleblog/settings.py

INSTALLED_APPS = [
    ...
    'blog',
    'pages',
]

# 정적/미디어 파일 설정
STATIC_URL = '/static/'
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'
```

### 4️⃣ 마이그레이션
```bash
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

### 5️⃣ 관리자 페이지
- http://127.0.0.1:8000/admin/

---

## 📖 학습 순서

### 👶 초보자
1. **01단계** 읽기 (1-2시간)
2. **07-1, 07-2** 학습 (2-3시간)
3. **07-3** 코딩 (2-3시간)
4. **08-3** CBV로 배우기 (3-4시간)
5. **09-1, 09-2** 학습 (2-3시간)
6. **10-2, 10-3** 템플릿 배우기 (2-3시간)

### 👨‍💻 중급자
1. **07** 빠르게 복습 (1-2시간)
2. **08-2** FBV와 **08-3** CBV 비교 (2-3시간)
3. **09** 심화 학습 (2-3시간)
4. **10** 완전 이해 (2-3시간)

---

## ✨ 각 파일별 사용 방법

### 이론 파일 (THEORY_*.md)
- 📖 읽기
- 📝 중요 부분 필기
- 🔗 링크 클릭해서 관련 코드 확인

### 실습 코드 (*.py)
- 💾 필요한 부분 복사
- 🔍 주석 읽기
- 📝 수정하며 이해하기
- ✅ 실행하며 확인하기

### 템플릿 파일 (*.html)
- 🎨 구조 분석
- 🏷️ 태그 이해
- 🔄 변수 치환 방식 학습
- 📝 필요에 따라 수정

---

## 🎓 학습 결과

이 과정을 모두 완료하면:

✅ Django 기본 개념 완벽 이해
✅ Model-Template-View 패턴 습득
✅ 데이터베이스 설계 능력
✅ FBV/CBV 모두 작성 가능
✅ 정적/미디어 파일 관리
✅ 템플릿 문법 마스터
✅ 완전한 웹 애플리케이션 구현 능력

---

## 💡 학습 팁

1. **한 번에 하나씩**
   - 한 섹션을 완료한 후 다음으로
   - 작은 단위로 나누어 학습

2. **직접 코딩**
   - 복사-붙여넣기 지양
   - 손으로 타이핑하며 이해

3. **에러는 친구**
   - 에러 메시지 읽기
   - Django는 매우 친절한 에러 메시지 제공

4. **실습 후 수정**
   - 코드를 이해하면 자신만의 방식으로 수정
   - 예: 모델 필드 추가, 템플릿 디자인 변경

5. **도움말 활용**
   - Django 공식 문서: https://docs.djangoproject.com/
   - 검색: Django [기능명]

---

## 🔗 추천 자료

### 공식 문서
- Django 공식: https://docs.djangoproject.com/
- Django 한국어: https://django-doc-ko-1.11.readthedocs.io/

### 추가 학습
- Django for Beginners
- Django Rest Framework
- Django + React/Vue

---

## 📞 문제 해결

### 일반적인 에러

**ModuleNotFoundError**
→ import 문 확인, 앱 등록 확인

**TemplateDoesNotExist**
→ 템플릿 경로 확인, 앱 INSTALLED_APPS 확인

**No such table**
→ python manage.py migrate 실행

**Page not found (404)**
→ urls.py 패턴 확인, 뷰 함수 확인

---

## 🎉 축하합니다!

이 가이드를 따라 학습하면 **완전한 Django 개발자**가 될 수 있습니다.

**다음 단계:**
- ✅ Django REST Framework로 API 개발
- ✅ Celery로 비동기 작업
- ✅ Docker로 배포
- ✅ 프론트엔드 프레임워크 통합 (React, Vue)

---

**Happy Coding! 🚀**

마지막 업데이트: 2024-12-23
