# 🚀 Django 블로그 사용법 가이드

## 📋 목차
1. [서버 실행](#1-서버-실행)
2. [주요 URL 접속](#2-주요-url-접속)
3. [관리자 페이지 사용](#3-관리자-페이지-사용)
4. [포스트 작성](#4-포스트-작성)
5. [포스트 조회](#5-포스트-조회)
6. [댓글 작성](#6-댓글-작성)
7. [좋아요 & 북마크](#7-좋아요--북마크)
8. [검색 기능](#8-검색-기능)
9. [대시보드](#9-대시보드)

---

## 1. 서버 실행

### 방법 1: 기본 실행
```powershell
cd c:\DJangGo
python manage.py runserver
```

### 방법 2: 특정 포트 실행
```powershell
python manage.py runserver 8080
```

### ✅ 성공 메시지
```
Starting development server at http://127.0.0.1:8000/
Quit the server with CTRL-BREAK.
```

---

## 2. 주요 URL 접속

| URL | 설명 | 로그인 필요 |
|-----|------|------------|
| http://127.0.0.1:8000/ | 홈 (포스트 목록) | ❌ |
| http://127.0.0.1:8000/admin/ | 관리자 페이지 | ✅ |
| http://127.0.0.1:8000/post/create/ | 포스트 작성 | ✅ |
| http://127.0.0.1:8000/post/1/ | 포스트 상세 (ID=1) | ❌ |
| http://127.0.0.1:8000/post/1/edit/ | 포스트 수정 | ✅ (작성자만) |
| http://127.0.0.1:8000/post/1/delete/ | 포스트 삭제 | ✅ (작성자만) |
| http://127.0.0.1:8000/search/ | 검색 페이지 | ❌ |
| http://127.0.0.1:8000/dashboard/ | 내 대시보드 | ✅ |
| http://127.0.0.1:8000/category/1/ | 카테고리별 포스트 | ❌ |

---

## 3. 관리자 페이지 사용

### 🔐 로그인 정보
- **URL**: http://127.0.0.1:8000/admin/
- **ID**: `admin`
- **Password**: `admin123`

### 관리 가능한 항목
1. **Users** - 사용자 관리
2. **Categories** - 카테고리 추가/수정/삭제
3. **Tags** - 태그 추가/수정/삭제
4. **Posts** - 포스트 추가/수정/삭제
5. **Comments** - 댓글 관리
6. **Likes** - 좋아요 내역
7. **Bookmarks** - 북마크 내역

### 📝 관리자 페이지에서 포스트 추가하기

1. **로그인**
   ```
   http://127.0.0.1:8000/admin/
   admin / admin123
   ```

2. **Categories 클릭 → Add Category**
   - Name: `기술`
   - Description: `기술 관련 포스트`
   - 저장

3. **Tags 클릭 → Add Tag**
   - Name: `Django`
   - 저장

4. **Posts 클릭 → Add Post**
   - Title: `Django로 블로그 만들기`
   - Content: `Django는 강력한 웹 프레임워크입니다...`
   - Author: `admin` 선택
   - Category: `기술` 선택
   - Tags: `Django` 선택
   - Published: ✅ 체크
   - 저장

---

## 4. 포스트 작성

### 방법 1: 웹 인터페이스 (로그인 필요)

1. **홈페이지 접속**
   ```
   http://127.0.0.1:8000/
   ```

2. **로그인**
   - 상단 네비게이션 → "로그인" 클릭
   - admin / admin123 입력

3. **포스트 작성**
   - 상단 네비게이션 → "✍️ 작성" 클릭
   - Title: 제목 입력
   - Content: 내용 입력
   - Category: 카테고리 선택 (선택사항)
   - Tags: 태그 선택 (선택사항)
   - Published: 공개 여부 체크
   - "저장" 버튼 클릭

### 방법 2: Python Shell에서 직접 생성

```python
python manage.py shell

from django.contrib.auth.models import User
from blog.models import Post, Category, Tag

# 사용자 가져오기
admin = User.objects.get(username='admin')

# 카테고리 생성
category = Category.objects.create(
    name='일상',
    description='일상 관련 포스트'
)

# 포스트 생성
post = Post.objects.create(
    title='새로운 포스트',
    content='포스트 내용입니다.',
    author=admin,
    category=category,
    published=True
)

# 태그 추가
tag = Tag.objects.create(name='Python')
post.tags.add(tag)

print(f'포스트 생성 완료: {post.title}')
```

---

## 5. 포스트 조회

### 전체 포스트 목록
```
http://127.0.0.1:8000/
```

**표시 정보:**
- 포스트 제목
- 작성자 (👤)
- 작성일 (📅)
- 조회수 (👁️)
- 카테고리 (배지)
- 내용 미리보기 (50단어)

### 포스트 상세 보기
```
http://127.0.0.1:8000/post/1/
```

**표시 정보:**
- 전체 내용
- 태그 목록
- 좋아요 수
- 북마크 수
- 댓글 목록
- 수정/삭제 버튼 (작성자만)

---

## 6. 댓글 작성

### ✅ 로그인 필요

1. **포스트 상세 페이지 이동**
   ```
   http://127.0.0.1:8000/post/1/
   ```

2. **댓글 작성 폼**
   - 페이지 하단에 "💬 댓글" 섹션
   - 텍스트 영역에 댓글 입력
   - "댓글 작성" 버튼 클릭

3. **작성된 댓글 확인**
   - 작성자명
   - 댓글 내용
   - 작성 시간

### Python Shell로 댓글 작성
```python
python manage.py shell

from django.contrib.auth.models import User
from blog.models import Post, Comment

# 사용자와 포스트 가져오기
user = User.objects.get(username='admin')
post = Post.objects.get(id=1)

# 댓글 생성
comment = Comment.objects.create(
    post=post,
    author=user,
    content='좋은 글이네요!'
)

print(f'댓글 작성 완료: {comment.content}')
```

---

## 7. 좋아요 & 북마크

### ✅ 로그인 필요

### 좋아요 추가/제거
1. **포스트 상세 페이지 이동**
   ```
   http://127.0.0.1:8000/post/1/
   ```

2. **❤️ 좋아요 버튼 클릭**
   - 처음 클릭: 좋아요 추가 (빨간색)
   - 다시 클릭: 좋아요 취소 (회색)
   - 좋아요 수 표시

### 북마크 추가/제거
1. **포스트 상세 페이지에서**
2. **⭐ 북마크 버튼 클릭**
   - 처음 클릭: 북마크 추가 (노란색)
   - 다시 클릭: 북마크 취소 (회색)
   - 북마크 수 표시

### 내 좋아요/북마크 확인
```
http://127.0.0.1:8000/dashboard/
```

---

## 8. 검색 기능

### 검색 페이지 접속
```
http://127.0.0.1:8000/search/
```

### 검색 방법
1. **검색어 입력**
   - 포스트 제목, 내용, 작성자명 검색

2. **검색 버튼 클릭**

3. **검색 결과 표시**
   - 일치하는 포스트 목록
   - 결과 개수 표시

### 검색 예시
- `Django` → Django 관련 포스트
- `Python` → Python 관련 포스트
- `admin` → admin이 작성한 포스트

---

## 9. 대시보드

### 내 대시보드 접속
```
http://127.0.0.1:8000/dashboard/
```

### ✅ 로그인 필요

### 표시 정보
1. **통계 카드**
   - 📝 내 포스트 수
   - 💬 내 댓글 수
   - ❤️ 내 좋아요 수
   - ⭐ 내 북마크 수

2. **내 포스트 목록**
   - 제목
   - 작성일
   - 조회수
   - 수정/삭제 버튼

---

## 🛠️ 추가 명령어

### 새 관리자 계정 생성
```powershell
python manage.py createsuperuser
```

### 데이터베이스 초기화
```powershell
# 데이터베이스 삭제
del db.sqlite3

# 마이그레이션 재실행
python manage.py migrate

# 새 관리자 생성
python manage.py createsuperuser
```

### 테스트 데이터 추가 (Python Shell)
```python
python manage.py shell

from django.contrib.auth.models import User
from blog.models import Category, Tag, Post

# 관리자 가져오기
admin = User.objects.get(username='admin')

# 카테고리 3개 생성
Category.objects.create(name='기술', description='기술 관련')
Category.objects.create(name='일상', description='일상 관련')
Category.objects.create(name='공부', description='공부 관련')

# 태그 4개 생성
Tag.objects.create(name='Django')
Tag.objects.create(name='Python')
Tag.objects.create(name='웹개발')
Tag.objects.create(name='백엔드')

print('✅ 테스트 데이터 생성 완료!')
```

---

## 📊 프로젝트 상태 확인

### 서버 상태 확인
```powershell
# 서버가 실행 중이면
# http://127.0.0.1:8000/ 접속 가능
```

### 데이터베이스 데이터 확인
```python
python manage.py shell

from blog.models import Post, Category, Tag

print(f'포스트 수: {Post.objects.count()}')
print(f'카테고리 수: {Category.objects.count()}')
print(f'태그 수: {Tag.objects.count()}')
```

### 관리자 페이지에서 확인
```
http://127.0.0.1:8000/admin/
```
- 각 모델의 데이터 개수 확인 가능

---

## 🎯 빠른 시작 (5분)

```powershell
# 1. 서버 실행
cd c:\DJangGo
python manage.py runserver

# 2. 브라우저 열기
# http://127.0.0.1:8000/

# 3. 관리자 로그인
# http://127.0.0.1:8000/admin/
# admin / admin123

# 4. 포스트 추가
# Posts → Add Post

# 5. 홈페이지에서 확인
# http://127.0.0.1:8000/
```

---

## 🐛 문제 해결

### 포트 이미 사용 중
```powershell
# 다른 포트로 실행
python manage.py runserver 8080
```

### 마이그레이션 에러
```powershell
python manage.py makemigrations
python manage.py migrate
```

### 관리자 비밀번호 분실
```powershell
python manage.py changepassword admin
```

---

## 📝 요약

| 작업 | URL | 명령어 |
|------|-----|--------|
| 서버 실행 | - | `python manage.py runserver` |
| 홈페이지 | http://127.0.0.1:8000/ | - |
| 관리자 | http://127.0.0.1:8000/admin/ | admin / admin123 |
| 포스트 작성 | http://127.0.0.1:8000/post/create/ | 로그인 필요 |
| 검색 | http://127.0.0.1:8000/search/ | - |
| 대시보드 | http://127.0.0.1:8000/dashboard/ | 로그인 필요 |

**🎉 이제 Django 블로그를 사용할 준비가 되었습니다!**
