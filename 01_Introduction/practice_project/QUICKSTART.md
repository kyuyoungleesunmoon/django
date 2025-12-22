# 01_Introduction 실습 프로젝트 - 빠른 시작

## 30초 안에 시작하기

```bash
# 1. 현재 디렉토리 이동
cd mysite

# 2. Django 설치
pip install django

# 3. 데이터베이스 초기화
python manage.py migrate

# 4. 관리자 생성 (선택)
python manage.py createsuperuser

# 5. 서버 실행
python manage.py runserver

# 6. 브라우저 열기
# http://localhost:8000 접속
```

## 이 프로젝트에서 배우는 것

| 단계 | 내용 | 파일 |
|------|------|------|
| 1 | Django 프로젝트 구조 이해 | `mysite/settings.py` |
| 2 | Django 앱 이해 | `hello/apps.py` |
| 3 | 데이터 모델 정의 | `hello/models.py` |
| 4 | 뷰 함수 작성 | `hello/views.py` |
| 5 | URL 라우팅 | `hello/urls.py` |
| 6 | HTML 템플릿 | `templates/hello/` |
| 7 | 관리자 페이지 | `hello/admin.py` |

## 주요 URL

| URL | 설명 |
|-----|------|
| `/` | 메시지 목록 페이지 |
| `/hello/greet/` | 간단한 인사 페이지 |
| `/hello/message/1/` | 메시지 상세보기 |
| `/admin/` | Django 관리자 페이지 |

## 데이터베이스 구조

### Message 모델
```
id (자동 생성)
├── title (CharField, max_length=100)
├── content (TextField)
├── created_at (DateTimeField, auto_now_add=True)
└── updated_at (DateTimeField, auto_now=True)
```

## 관리자 페이지 사용법

1. `/admin/`에 접속
2. 생성한 계정으로 로그인
3. "메시지들" 섹션에서 메시지 추가/수정/삭제

## 도움말

더 자세한 내용은 상위 폴더의 `THEORY_01_Django_Overview.md`를 참고하세요.
