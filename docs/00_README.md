# Django 백엔드 심화 - 완전 가이드

## 📚 학습 구성

이 프로젝트는 다음 3가지 핵심 주제를 다룹니다:

### 1️⃣ **CRUD 웹 앱 구축**
- 포스트(블로그 글) 작성, 조회, 수정, 삭제
- 댓글, 좋아요, 북마크 기능
- 카테고리/태그로 포스트 분류
- 고급 검색 및 필터링

### 2️⃣ **Django ORM 심화**
- 모델 간 관계 (ForeignKey, ManyToMany, OneToOne)
- N+1 쿼리 문제 해결
- select_related / prefetch_related 최적화
- 복잡한 필터링 (Q 객체)
- 집계 함수 (Count, Sum, Avg)
- 시그널과 Manager 커스터마이징

### 3️⃣ **기본 인증/권한**
- 회원가입 및 로그인
- 권한 시스템 (Permissions)
- 그룹 관리 (Groups)
- 소유자만 접근 가능하도록 제어
- 데이터베이스 레벨 보안

---

## 🗂️ 프로젝트 파일 구조

```
c:\DJangGo/
├── README.md                          # 실행 가이드
├── requirements.txt                   # Python 패키지 목록
│
├── docs/                              # 📖 이론 문서
│   ├── 01_DJANGO_ORM_THEORY.md        # ORM 개념 및 쿼리
│   ├── 02_AUTH_PERMISSION_THEORY.md   # 인증/권한 이론
│   ├── 03_ORM_EXAMPLES.md             # ORM 실전 예제 15개
│   └── 04_AUTH_EXAMPLES.md            # 인증 실전 예제 15개
│
├── myproject/                         # Django 프로젝트
│   ├── manage.py                      # Django 관리 스크립트
│   ├── settings.py                    # 프로젝트 설정
│   ├── urls.py                        # URL 라우팅
│   ├── wsgi.py                        # WSGI 설정
│   │
│   └── blog/                          # 📝 블로그 앱
│       ├── models.py                  # 데이터베이스 모델 (6개)
│       ├── views.py                   # 뷰 로직 (14개 함수/클래스)
│       ├── urls.py                    # 앱 URL 라우팅
│       ├── forms.py                   # 폼 (로그인, 회원가입, 포스트, 댓글)
│       ├── admin.py                   # 관리자 페이지
│       ├── signals.py                 # 자동 통계 업데이트
│       └── apps.py                    # 앱 설정
│
└── templates/                         # 🎨 HTML 템플릿
    └── blog/
        ├── base.html                  # 기본 템플릿 (네비게이션)
        ├── home.html                  # 홈페이지
        ├── login.html                 # 로그인
        ├── register.html              # 회원가입
        ├── post_list.html             # 포스트 목록
        ├── post_detail.html           # 포스트 상세 페이지
        ├── post_form.html             # 포스트 작성/수정
        ├── post_confirm_delete.html   # 포스트 삭제 확인
        ├── dashboard.html             # 사용자 대시보드
        └── advanced_search.html       # 고급 검색
```

---

## 🗄️ 데이터베이스 모델 (6개)

### 1. **Category** (카테고리)
```
- id (PK)
- name (문자열, unique)
- slug (슬러그, unique)
- description (설명)
- created_at (생성 시간)
```

### 2. **Tag** (태그)
```
- id (PK)
- name (문자열, unique)
- slug (슬러그, unique)
```

### 3. **Post** (포스트 - 핵심)
```
- id (PK)
- title (제목)
- slug (슬러그, unique)
- author (FK → User, 다대일)
- category (FK → Category, 다대일)
- content (본문)
- excerpt (요약)
- tags (M2M → Tag, 다대다)
- status (초안/발행/보관)
- is_featured (주목 포스트)
- views (조회수)
- created_at / updated_at / published_at (시간)
```

### 4. **Comment** (댓글 - 계층 구조)
```
- id (PK)
- post (FK → Post, 다대일)
- author (FK → User, 다대일)
- content (댓글 내용)
- parent (FK → self, 대댓글 지원)
- is_approved (승인 여부)
- created_at / updated_at (시간)
```

### 5. **Like** (좋아요)
```
- id (PK)
- post (FK → Post, 다대일)
- user (FK → User, 다대일)
- created_at (시간)
- unique_together (post, user) - 중복 방지
```

### 6. **PostStatistics** (포스트 통계 - 캐시)
```
- id (PK)
- post (O2O → Post, 일대일)
- total_likes (좋아요 수)
- total_comments (댓글 수)
- total_bookmarks (북마크 수)
- last_updated (마지막 업데이트)
```

---

## 👁️ 뷰 기능 (14개)

### CRUD 작업
| 뷰 | 기능 | 권한 |
|---|---|---|
| `home()` | 홈페이지 (최신 포스트) | 없음 |
| `PostListView` | 포스트 목록 | 없음 |
| `PostDetailView` | 포스트 상세 | 없음 |
| `PostCreateView` | 포스트 생성 | add_post |
| `PostUpdateView` | 포스트 수정 | 소유자 |
| `PostDeleteView` | 포스트 삭제 | 소유자 |

### 댓글
| 뷰 | 기능 |
|---|---|
| `add_comment()` | 댓글 작성 |
| `delete_comment()` | 댓글 삭제 |

### 상호작용
| 뷰 | 기능 |
|---|---|
| `toggle_like()` | 좋아요 토글 |
| `toggle_bookmark()` | 북마크 토글 |

### 사용자
| 뷰 | 기능 |
|---|---|
| `user_dashboard()` | 사용자 대시보드 |
| `register()` | 회원가입 |

### 분류 및 검색
| 뷰 | 기능 |
|---|---|
| `category_posts()` | 카테고리별 포스트 |
| `tag_posts()` | 태그별 포스트 |
| `advanced_search()` | 고급 검색 |

---

## 🔑 주요 ORM 기술

### 1. **관계 설정**
- `ForeignKey`: Post ↔ User/Category (다대일)
- `ManyToManyField`: Post ↔ Tag (다대다)
- `OneToOneField`: PostStatistics ↔ Post (일대일)
- 자기참조: Comment (대댓글)

### 2. **쿼리 최적화**
```python
# select_related (외래키, 일대일)
posts = Post.objects.select_related('author', 'category')

# prefetch_related (다대다, 역참조)
posts = Post.objects.prefetch_related('tags', 'comments')

# 결과: 데이터베이스 쿼리 횟수 대폭 감소
```

### 3. **필터링 및 집계**
```python
# Q 객체로 복잡한 필터링
posts = Post.objects.filter(
    Q(title__icontains='django') | 
    Q(content__icontains='django')
)

# 집계
stats = Post.objects.aggregate(
    total=Count('id'),
    avg_views=Avg('views')
)

# Annotation - 각 객체마다 계산
authors = User.objects.annotate(
    post_count=Count('posts')
).filter(post_count__gte=5)
```

### 4. **시그널**
포스트 생성 시 자동으로 PostStatistics 생성
좋아요/댓글 추가 시 자동으로 통계 업데이트

---

## 🔐 인증 & 권한 시스템

### 1. **사용자 인증**
```python
# 로그인
user = authenticate(request, username='john', password='pass123')
if user:
    login(request, user)

# 로그아웃
logout(request)

# 현재 사용자 접근
request.user
```

### 2. **권한 확인**
```python
# 단일 권한
user.has_perm('blog.add_post')

# 여러 권한
user.has_perms(['blog.add_post', 'blog.change_post'])

# 모듈 권한
user.has_module_perms('blog')
```

### 3. **접근 제어**
```python
# 데코레이터
@login_required
@permission_required('blog.add_post')
def create_post(request):
    pass

# 뷰 로직
if post.author != request.user:
    return HttpResponseForbidden()
```

### 4. **그룹 관리**
```python
editors = Group.objects.get_or_create(name='Editors')[0]
editors.permissions.add(add_post_perm, change_post_perm)
user.groups.add(editors)
```

---

## 🚀 실행 방법

### 1단계: 환경 설정
```bash
cd c:\DJangGo
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```

### 2단계: 데이터베이스 생성
```bash
cd myproject
python manage.py makemigrations
python manage.py migrate
```

### 3단계: 관리자 계정 생성
```bash
python manage.py createsuperuser
# 사용자명: admin
# 비밀번호: (원하는 비밀번호)
```

### 4단계: 서버 실행
```bash
python manage.py runserver
```

### 5단계: 접속
- 메인: http://127.0.0.1:8000
- 관리자: http://127.0.0.1:8000/admin

---

## 📖 문서 로드맵

### 이론 학습
1. `01_DJANGO_ORM_THEORY.md` - ORM 개념 이해
2. `02_AUTH_PERMISSION_THEORY.md` - 인증/권한 이해

### 실전 예제
3. `03_ORM_EXAMPLES.md` - 15가지 ORM 실행 코드
4. `04_AUTH_EXAMPLES.md` - 15가지 인증 실행 코드

### 실제 코드
5. `myproject/blog/models.py` - 모델 구현
6. `myproject/blog/views.py` - CRUD 뷰 구현
7. `templates/blog/` - 템플릿 구현

---

## 💡 핵심 배운 내용

### ORM
✅ 모델 정의 및 관계 설정
✅ N+1 쿼리 문제 진단 및 해결
✅ select_related / prefetch_related 활용
✅ Q 객체로 복잡한 쿼리 작성
✅ 집계 및 Annotation
✅ 시그널 활용

### 인증 & 권한
✅ 사용자 생성 및 로그인
✅ 권한 할당 및 확인
✅ 소유권 기반 접근 제어
✅ 그룹으로 권한 관리
✅ 보안 베스트 프랙티스

### 웹 개발
✅ 클래스형 뷰 (CBV)
✅ 함수형 뷰
✅ 폼 처리
✅ 템플릿 상속
✅ 정적 파일 및 미디어 처리

---

## 🔗 추천 다음 단계

1. **REST API**: Django REST Framework
2. **캐싱**: Redis, Memcached
3. **테스트**: Django TestCase, pytest
4. **배포**: Docker, Gunicorn, Nginx
5. **모니터링**: Sentry, New Relic
6. **비동기 작업**: Celery

---

## 📞 문제 해결

### 마이그레이션 오류
```bash
python manage.py migrate --fake blog zero
python manage.py migrate blog
```

### 포트 충돌
```bash
python manage.py runserver 8001
```

### 권한 재설정
```bash
python manage.py migrate auth
python manage.py migrate
```

---

## 🎯 프로젝트 특징

✨ **완전한 구현**
- 모든 CRUD 작업 구현됨
- 실제 동작하는 코드

🏗️ **구조적 설계**
- ORM 최적화된 쿼리
- 권한 기반 접근 제어
- Django 베스트 프랙티스 준수

📚 **충실한 문서**
- 이론 설명
- 15개 실전 예제
- 주석이 풍부한 코드

🔒 **보안 고려**
- CSRF 보호
- SQL Injection 방지
- 권한 기반 접근

---

## ✅ 체크리스트

학습을 마친 후 다음을 확인하세요:

- [ ] ORM 모델 관계 이해
- [ ] select_related와 prefetch_related 차이 설명
- [ ] 권한 시스템 작동 원리 이해
- [ ] 포스트 작성 및 수정 권한 확인
- [ ] 쿼리 최적화 개선 효과 측정
- [ ] 자신의 포스트만 수정/삭제 가능 확인
- [ ] 댓글 및 좋아요 기능 작동 확인
- [ ] 검색 및 필터링 기능 작동 확인

---

**프로젝트를 통해 Django 백엔드 심화를 완전히 마스터할 수 있습니다!** 🎓
