# Django 첫 프로젝트 - 01_Introduction 실습

이것은 Django 기초를 학습하기 위한 **실습 프로젝트**입니다.

## 프로젝트 구조

```
mysite/
├── manage.py                 # Django 관리 명령어 도구
├── db.sqlite3               # SQLite 데이터베이스
├── mysite/                  # 프로젝트 설정 디렉토리
│   ├── __init__.py
│   ├── settings.py          # 프로젝트 설정
│   ├── urls.py              # URL 라우팅
│   └── wsgi.py              # WSGI 애플리케이션
├── hello/                   # 우리의 첫 번째 앱
│   ├── migrations/          # 데이터베이스 마이그레이션
│   ├── __init__.py
│   ├── admin.py             # 관리자 페이지 설정
│   ├── apps.py              # 앱 설정
│   ├── models.py            # 데이터 모델
│   ├── tests.py             # 테스트
│   ├── urls.py              # 앱 URL 라우팅
│   └── views.py             # 뷰 함수
└── templates/               # HTML 템플릿
    └── hello/
        ├── index.html       # 메시지 목록 페이지
        └── detail.html      # 메시지 상세 페이지
```

## 학습 목표

1. ✅ Django 프로젝트 생성
2. ✅ Django 앱 생성
3. ✅ 모델 정의 (Message 모델)
4. ✅ 뷰 작성 (함수형 뷰)
5. ✅ URL 라우팅
6. ✅ HTML 템플릿 생성
7. ✅ 관리자 페이지 설정

## 실행 방법

### 1. 가상환경 활성화
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Mac/Linux
python3 -m venv venv
source venv/bin/activate
```

### 2. Django 설치
```bash
pip install django
```

### 3. 데이터베이스 마이그레이션
```bash
python manage.py migrate
```

### 4. 슈퍼유저(관리자) 생성
```bash
python manage.py createsuperuser
# 사용자명, 이메일, 비밀번호를 입력하세요
```

### 5. 개발 서버 실행
```bash
python manage.py runserver
```

### 6. 웹 브라우저 접속

- **홈페이지**: http://127.0.0.1:8000/
- **메시지 목록**: http://127.0.0.1:8000/hello/
- **관리자 페이지**: http://127.0.0.1:8000/admin/
- **인사 페이지**: http://127.0.0.1:8000/hello/greet/

## 학습 과제

### 초급 (Level 1)
1. [ ] 프로젝트 실행 후 각 URL 페이지에 접속해보기
2. [ ] 관리자 페이지에서 Message 추가해보기
3. [ ] 다양한 제목과 내용으로 여러 메시지 생성해보기

### 중급 (Level 2)
1. [ ] `hello/models.py`에 새로운 필드 추가해보기 (예: author, category)
2. [ ] `hello/views.py`에 새로운 뷰 함수 작성해보기
3. [ ] `urls.py`에 새로운 URL 패턴 추가해보기

### 고급 (Level 3)
1. [ ] 관리자 페이지 커스터마이징 (list_display, list_filter 등)
2. [ ] 템플릿에 CSS/JavaScript 추가해보기
3. [ ] 테스트 코드 실행해보기: `python manage.py test`

## 핵심 개념

### 프로젝트 vs 앱
- **프로젝트(mysite)**: 전체 웹사이트 설정을 담당
- **앱(hello)**: 특정 기능을 담당하는 모듈 (여러 앱 가능)

### MVT 패턴
- **Model (모델)**: 데이터베이스 정의 (`models.py`)
- **View (뷰)**: 비즈니스 로직 (`views.py`)
- **Template (템플릿)**: HTML 페이지 (`templates/`)

### URL 라우팅
```
사용자 요청 → urls.py (라우팅) → views.py (뷰 함수) → models.py (데이터 조회) → templates (HTML 렌더링)
```

## 다음 단계

이 프로젝트를 마친 후:
- **07단계**: 더 복잡한 모델과 ORM 배우기
- **08단계**: 클래스형 뷰 배우기
- **09단계**: 정적 파일과 미디어 파일 처리하기
- **10단계**: 템플릿 필터와 태그 배우기

## 명령어 치트시트

```bash
# 프로젝트 생성
django-admin startproject mysite

# 앱 생성
python manage.py startapp hello

# 마이그레이션 생성
python manage.py makemigrations

# 마이그레이션 적용
python manage.py migrate

# 개발 서버 실행
python manage.py runserver

# 셸 실행 (대화형 파이썬)
python manage.py shell

# 테스트 실행
python manage.py test

# 정적 파일 수집
python manage.py collectstatic
```

## 트러블슈팅

### "ModuleNotFoundError: No module named 'django'"
→ 가상환경이 활성화되어 있지 않거나 Django가 설치되어 있지 않습니다.
```bash
pip install django
```

### "No such table: hello_message"
→ 마이그레이션을 실행하지 않았습니다.
```bash
python manage.py migrate
```

### "TemplateDoesNotExist"
→ 템플릿 디렉토리 경로가 잘못되었을 수 있습니다.
settings.py의 TEMPLATES 설정을 확인하세요.

## 참고 자료

- [Django 공식 문서](https://docs.djangoproject.com/)
- [Django Girls 튜토리얼](https://tutorial.djangogirls.org/)
- [Real Python Django 튜토리얼](https://realpython.com/get-started-with-django/)
