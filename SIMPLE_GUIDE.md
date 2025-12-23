# Django 블로그 사용 가이드 (간소화 버전)

## 서버 실행

```powershell
cd c:\DJangGo
python manage.py runserver
```

서버 실행 확인:
```
Starting development server at http://127.0.0.1:8000/
```

---

## 주요 URL

| URL | 설명 |
|-----|------|
| http://127.0.0.1:8000/ | 홈 (포스트 목록) |
| http://127.0.0.1:8000/admin/ | 관리자 페이지 |
| http://127.0.0.1:8000/post/create/ | 포스트 작성 |
| http://127.0.0.1:8000/search/ | 검색 |
| http://127.0.0.1:8000/dashboard/ | 대시보드 |

---

## 관리자 로그인

**URL:** http://127.0.0.1:8000/admin/

**계정:**
- ID: `admin`
- Password: `admin123`

---

## 포스트 작성 방법

### 방법 1: 관리자 페이지 (추천)

1. http://127.0.0.1:8000/admin/ 접속
2. admin / admin123 로그인
3. "Posts" 클릭 → "Add Post" 버튼
4. 정보 입력:
   - Title: 제목 입력
   - Content: 내용 입력
   - Author: admin 선택
   - Category: 카테고리 선택 (선택사항)
   - Tags: 태그 선택 (선택사항)
   - Published: 체크 (공개)
5. "Save" 버튼 클릭

### 방법 2: 웹 페이지

1. http://127.0.0.1:8000/ 접속
2. 상단 "로그인" 클릭
3. admin / admin123 입력
4. 상단 "작성" 클릭
5. 포스트 작성 후 "저장"

---

## 현재 생성된 데이터

```
카테고리: 4개
- 기술
- 일상
- 공부
- (기존 1개)

태그: 5개
- Django
- Python
- 웹개발
- 백엔드
- (기존 1개)

포스트: 0개 (직접 추가 필요)
```

---

## 빠른 시작 (3단계)

```
1. 서버 실행
   → python manage.py runserver

2. 관리자 페이지 접속
   → http://127.0.0.1:8000/admin/
   → admin / admin123

3. 포스트 추가
   → Posts → Add Post → 작성 후 Save
```

---

## 테스트 데이터 추가 (선택사항)

Python 스크립트로 테스트 포스트 생성:

```python
python -c "
import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'myproject.settings')
import django
django.setup()

from django.contrib.auth.models import User
from blog.models import Category, Tag, Post

admin = User.objects.get(username='admin')
tech = Category.objects.get(name='기술')

post = Post.objects.create(
    title='Django 시작하기',
    content='Django는 강력한 웹 프레임워크입니다. Python으로 빠르게 웹 애플리케이션을 개발할 수 있습니다.',
    author=admin,
    category=tech,
    published=True
)
post.tags.add(Tag.objects.get(name='Django'))
print('[생성 완료] 포스트:', post.title)
"
```

---

## 문제 해결

### 서버 실행 안됨
```powershell
# 포트 충돌 시 다른 포트 사용
python manage.py runserver 8080
```

### 관리자 비밀번호 분실
```powershell
python manage.py changepassword admin
```

### 데이터베이스 초기화
```powershell
del db.sqlite3
python manage.py migrate
python manage.py createsuperuser
```

---

## 주요 기능

- **포스트 작성/수정/삭제**: 로그인 필요
- **댓글**: 포스트 상세 페이지에서 작성
- **좋아요/북마크**: 포스트 상세 페이지에서 클릭
- **검색**: 제목, 내용, 작성자로 검색
- **대시보드**: 내 포스트, 댓글, 좋아요, 북마크 확인

---

## 참고사항

- 모든 이모티콘이 제거되어 인코딩 문제 없음
- UTF-8 인코딩으로 한글 지원
- Bootstrap 5 스타일 적용
- 반응형 디자인
