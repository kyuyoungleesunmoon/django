# 📚 Django 완벽 학습 가이드

## 🎯 학습 목표

Django를 처음부터 배워서 완전한 웹 애플리케이션을 만들 수 있게 되는 것이 목표입니다.

---

## 📖 커리큘럼 구조

### 01. Django 소개 및 기본 개념
- Django란 무엇인가?
- MTV 아키텍처 이해
- Django 프로젝트 구조 학습
- 프로젝트 설정 및 초기화

**필수 파일:**
- `01_Introduction/THEORY_01_Django_Overview.md` - 이론 학습
- `01_Introduction/PROJECT_SETUP.md` - 프로젝트 생성 가이드

---

### 07. Django 프로젝트에서 앱 개발하기

#### 07-1. 블로그 앱과 페이지 앱 만들기
- 앱 개념 이해
- 앱 생성 및 등록
- 앱 구조 이해

**실습 코드:**
```bash
python manage.py startapp blog
python manage.py startapp pages
```

#### 07-2. 데이터베이스 개념 이해하기
- 관계형 데이터베이스 개념
- 테이블, 행, 열 이해
- ORM (Object-Relational Mapping) 개념
- Primary Key, Foreign Key 이해

#### 07-3. 모델 만들기
- Django 모델 정의
- 필드 타입 학습
- 모델 옵션 설정
- 마이그레이션 실행

**실습 코드:**
- `07_App_Development/blog/models.py`
- `07_App_Development/pages/models.py`

**학습 자료:**
- `07_App_Development/THEORY_07_App_Development.md`

**실습 순서:**
```bash
# 1단계: 모델 작성
# blog/models.py와 pages/models.py 코드 복사

# 2단계: admin.py 설정
python manage.py createsuperuser

# 3단계: 마이그레이션 생성
python manage.py makemigrations

# 4단계: 마이그레이션 적용
python manage.py migrate

# 5단계: 관리자 페이지 확인
python manage.py runserver
# http://127.0.0.1:8000/admin/ 접속
```

---

### 08. 웹 페이지 만들기

#### 08-1. URL 설정하기
- URL 패턴 작성
- 경로 컨버터 학습
- URL 역참조 (Reverse) 이해

#### 08-2. FBV (Function-Based View) 로 페이지 만들기
- 함수형 뷰 작성
- HTTP 요청/응답 처리
- 데이터 조회 및 템플릿 렌더링
- 데코레이터 활용

**특징:**
- 간단하고 직관적
- 빠른 개발
- 명시적인 제어

#### 08-3. CBV (Class-Based View) 로 페이지 만들기
- 클래스형 뷰 작성
- Generic CBV (ListView, DetailView 등)
- Mixin을 통한 기능 확장
- 코드 재사용성 향상

**특징:**
- 코드 재사용성 높음
- 확장 가능
- 인증/권한 관리 용이

**실습 코드:**
- `08_Web_Pages/blog_urls.py` - URL 설정
- `08_Web_Pages/blog_views.py` - CBV 구현
- `08_Web_Pages/blog_views_fbv.py` - FBV 구현
- `08_Web_Pages/pages_urls.py` - Pages 앱 URL
- `08_Web_Pages/pages_views.py` - Pages 앱 뷰

**학습 자료:**
- `08_Web_Pages/THEORY_08_Web_Pages.md`

**실습 순서:**
```bash
# 1단계: URL 설정
# simpleblog/urls.py 수정
from django.urls import path, include

urlpatterns = [
    path('blog/', include('blog.urls')),
    path('pages/', include('pages.urls')),
]

# 2단계: blog/urls.py 생성
# 08_Web_Pages/blog_urls.py 참고

# 3단계: blog/views.py 작성
# 08_Web_Pages/blog_views.py 또는 blog_views_fbv.py 참고

# 4단계: pages/urls.py 생성
# 08_Web_Pages/pages_urls.py 참고

# 5단계: pages/views.py 작성
# 08_Web_Pages/pages_views.py 참고

# 6단계: 템플릿 생성
mkdir -p blog/templates/blog
mkdir -p pages/templates/pages
```

---

### 09. 정적 파일과 미디어 파일 관리하기

#### 09-1. 정적 파일 관리하기
- CSS, JavaScript, 이미지 관리
- static/ 디렉토리 구조
- settings.py 정적 파일 설정
- 템플릿에서 정적 파일 사용
- collectstatic 명령 (프로덕션)

**파일 구조:**
```
blog/
├── static/
│   ├── blog/
│   │   ├── css/
│   │   │   └── style.css
│   │   ├── js/
│   │   │   └── script.js
│   │   └── images/
│   │       └── default.png
```

#### 09-2. 미디어 파일 관리하기
- 사용자 업로드 파일 관리
- ImageField, FileField 사용
- 파일 업로드 유효성 검사
- 이미지 최적화
- 보안 고려사항

**실습 코드:**
- `09_Static_Media/settings_static_media.py` - settings.py 설정
- `09_Static_Media/urls_example.py` - urls.py 설정
- `09_Static_Media/models_with_media.py` - 미디어 필드 추가
- `09_Static_Media/forms_example.py` - 파일 유효성 검사

**학습 자료:**
- `09_Static_Media/THEORY_09_Static_Media.md`

**실습 순서:**
```bash
# 1단계: settings.py 수정
# 09_Static_Media/settings_static_media.py 참고

# 2단계: urls.py 수정
# 09_Static_Media/urls_example.py 참고

# 3단계: 모델에 이미지 필드 추가
# 09_Static_Media/models_with_media.py 참고

# 4단계: 마이그레이션 수행
python manage.py makemigrations
python manage.py migrate

# 5단계: 정적 파일 디렉토리 생성
mkdir -p static/blog/css
mkdir -p static/blog/js
mkdir -p media/blog/posts

# 6단계: admin.py에서 이미지 미리보기 설정
```

---

### 10. 페이지 구성 개선하기

#### 10-1. 포스트 목록 페이지의 문제 파악하기
- 콘텐츠 표시 문제 (길이)
- 날짜 형식 문제
- 이미지 없을 때 처리
- 빈 목록 처리
- 조회수 표시 및 포맷팅

#### 10-2. 템플릿 파일에서 if 문 사용하기
- 조건부 콘텐츠 표시
- 변수 존재 여부 확인
- 불린 값 확인
- 비교 연산 (>, <, ==)
- 복합 조건 (and, or, not)
- 리스트 비어있는지 확인

**예제:**
```html
{% if post.image %}
    <img src="{{ post.image.url }}" alt="{{ post.title }}">
{% else %}
    <img src="{% static 'blog/images/default.png' %}" alt="기본 이미지">
{% endif %}

{% if post.views > 1000 %}
    <span class="badge">HOT</span>
{% elif post.views > 100 %}
    <span class="badge">POPULAR</span>
{% endif %}

{% if posts %}
    <!-- 포스트 목록 표시 -->
{% else %}
    <p>포스트가 없습니다.</p>
{% endif %}
```

#### 10-3. 템플릿 필터 사용하기
- 날짜 필터 (date, timesince)
- 숫자 필터 (intcomma, floatformat)
- 문자열 필터 (truncatewords, upper, lower)
- URL 필터
- 커스텀 필터 작성

**자주 사용되는 필터:**
```html
<!-- 날짜 -->
{{ post.created_at|date:"Y-m-d" }}
{{ post.created_at|date:"Y년 m월 d일" }}

<!-- 숫자 -->
{{ post.views|intcomma }}

<!-- 텍스트 -->
{{ post.content|truncatewords:30 }}

<!-- 시간 차이 -->
{{ post.created_at|timesince }} 전
```

**실습 코드:**
- `10_Page_Improvement/blog_filters.py` - 커스텀 필터 정의
- `10_Page_Improvement/post_list_improved.html` - 개선된 템플릿

**학습 자료:**
- `10_Page_Improvement/THEORY_10_Page_Improvement.md`

**실습 순서:**
```bash
# 1단계: templatetags 디렉토리 생성
mkdir -p blog/templatetags

# 2단계: __init__.py 생성
touch blog/templatetags/__init__.py

# 3단계: 커스텀 필터 정의
# 10_Page_Improvement/blog_filters.py 를 blog/templatetags/blog_filters.py로 저장

# 4단계: 템플릿에서 필터 로드
{% load blog_filters %}

# 5단계: 필터 사용
{{ post.created_at|korean_date }}
{{ post.views|intcomma }}
```

---

## 🚀 빠른 시작 가이드

### 프로젝트 생성

```bash
# 1. Python 가상환경 생성
python -m venv venv

# 2. 가상환경 활성화 (Windows)
venv\Scripts\activate

# 3. Django 설치
pip install django==4.2 pillow

# 4. 프로젝트 생성
django-admin startproject simpleblog
cd simpleblog

# 5. 앱 생성
python manage.py startapp blog
python manage.py startapp pages

# 6. apps 등록 (settings.py)
INSTALLED_APPS = [
    ...
    'blog',
    'pages',
]

# 7. 초기 마이그레이션
python manage.py migrate

# 8. 슈퍼유저 생성
python manage.py createsuperuser

# 9. 개발 서버 실행
python manage.py runserver
```

### 브라우저 접속
- 홈: http://127.0.0.1:8000/
- 관리자: http://127.0.0.1:8000/admin/

---

## 📋 실습 체크리스트

### 07 단계
- [ ] Blog 모델 작성 (Post, Comment, Category)
- [ ] Pages 모델 작성 (Page, About, Contact)
- [ ] admin.py에 모델 등록
- [ ] makemigrations 실행
- [ ] migrate 실행
- [ ] 관리자 페이지에서 데이터 추가

### 08 단계
- [ ] blog/urls.py 작성
- [ ] pages/urls.py 작성
- [ ] simpleblog/urls.py에서 app urls 포함
- [ ] blog/views.py 작성 (CBV 또는 FBV)
- [ ] pages/views.py 작성
- [ ] 템플릿 디렉토리 생성
- [ ] 템플릿 파일 작성

### 09 단계
- [ ] settings.py 정적/미디어 파일 설정
- [ ] urls.py에서 정적/미디어 파일 서빙 설정
- [ ] 모델에 ImageField 추가
- [ ] static/ 디렉토리 생성 및 파일 추가
- [ ] 관리자 이미지 미리보기 설정

### 10 단계
- [ ] if/else 문을 사용한 조건부 렌더링
- [ ] 다양한 필터 사용 (date, truncatewords 등)
- [ ] 커스텀 필터 작성
- [ ] 개선된 포스트 목록 페이지 구현

---

## 💡 실습 팁

1. **한 번에 모든 코드를 작성하지 말기**
   - 한 섹션을 끝낼 때마다 runserver로 테스트
   - 작은 단위로 나누어서 진행

2. **관리자 페이지 활용**
   - 데이터 입력 및 확인
   - 모델 구조 이해

3. **에러 메시지 읽기**
   - Django의 에러 메시지는 매우 자세함
   - 에러 메시지를 읽으면 문제 해결 가능

4. **템플릿 문법 연습**
   - for, if 문은 매우 중요
   - 필터와 조합하면 강력함

5. **보안 고려**
   - 파일 업로드 시 유효성 검사
   - 사용자 입력 검증

---

## 📚 추가 학습 자료

### Django 공식 문서
- https://docs.djangoproject.com/

### 추천 학습 순서
1. 모델 개념 완벽 이해
2. views와 urls 연결 방식 이해
3. 템플릿 문법 익히기
4. 정적 파일 관리 이해
5. 폼 유효성 검사 학습
6. 사용자 인증 및 권한
7. 배포 (Heroku, PythonAnywhere 등)

---

## 🎓 학습 완료 후 다음 단계

### 심화 주제
- 폼 처리 (Django Forms)
- 사용자 인증 및 권한 관리
- 쿼리 최적화 (select_related, prefetch_related)
- 캐싱 (Cache Framework)
- 비동기 작업 (Celery)
- 테스트 작성 (Unit Test, Integration Test)

### 프론트엔드 통합
- JavaScript와의 연동
- AJAX 요청/응답
- REST API 작성 (Django REST Framework)
- 싱글 페이지 애플리케이션 (SPA)

### 배포
- 프로덕션 서버 설정
- 정적 파일 최적화
- 데이터베이스 최적화
- SSL/HTTPS 설정

---

## 📞 도움말

문제 해결 팁:
1. Django 공식 문서 먼저 확인
2. 에러 메시지 전문 읽기
3. 작은 테스트 코드 작성해보기
4. StackOverflow에서 검색

---

**행운을 빕니다! 🚀 Happy Coding!**
