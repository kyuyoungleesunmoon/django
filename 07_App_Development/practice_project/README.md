# 07_App_Development 실습 프로젝트 - 모델과 ORM

Django의 **모델(Model)** 을 학습하기 위한 블로그 애플리케이션입니다.

## 이 프로젝트에서 배우는 것

✅ 모델 정의 (Models)  
✅ 필드 타입과 옵션  
✅ 관계 (ForeignKey, ManyToMany)  
✅ 마이그레이션  
✅ ORM 쿼리  
✅ 관리자 페이지 커스터마이징  

## 주요 모델 구조

```
Article (게시글)
├── Category (카테고리) - ForeignKey
├── Comment (댓글) - Reverse Relation
├── Tag (태그) - ManyToMany
└── User (작성자) - ForeignKey
```

## 빠른 시작

```bash
cd blog

# 1. Django 설치
pip install django

# 2. 마이그레이션
python manage.py migrate

# 3. 슈퍼유저 생성
python manage.py createsuperuser

# 4. 서버 실행
python manage.py runserver

# 5. 접속
# 홈: http://localhost:8000/
# 관리자: http://localhost:8000/admin/
```

## 핵심 모델 코드

### Article 모델 주요 필드

```python
class Article(models.Model):
    # 기본 필드
    title = CharField(max_length=200)
    slug = SlugField(unique=True)
    content = TextField()
    
    # 관계
    author = ForeignKey(User, on_delete=CASCADE)
    category = ForeignKey(Category, on_delete=SET_NULL, null=True)
    
    # 메타 데이터
    view_count = IntegerField(default=0)
    is_published = BooleanField(default=False)
    
    # 타임스탬프
    created_at = DateTimeField(auto_now_add=True)
    updated_at = DateTimeField(auto_now=True)
    
    # 메서드
    def publish(self):
        self.is_published = True
        self.save()
```

## 학습 과제

### 초급
- [ ] 관리자 페이지에서 게시글, 카테고리 추가
- [ ] 게시글 발행/미발행 토글
- [ ] 댓글 추가 (관리자에서)

### 중급
- [ ] models.py에서 새로운 필드 추가 (tags)
- [ ] 슬러그 자동 생성 구현
- [ ] 커스텀 쿼리셋 작성

### 고급
- [ ] model signals 사용 (auto save slug)
- [ ] 커스텀 manager 작성
- [ ] 데이터베이스 인덱스 최적화

## 데이터베이스 다이어그램

```
User (Django 기본)
  └── Article (1:N)
      ├── Comment (1:N)
      ├── Category (N:1)
      └── Tag (N:M)

Category
  └── Article (1:N)

Tag
  └── Article (N:M)
```

## 유용한 ORM 쿼리

```python
# 조회
Article.objects.all()
Article.objects.filter(is_published=True)
Article.objects.get(slug='my-first-post')

# 생성
Article.objects.create(title='제목', content='내용', author=user)

# 수정
article.title = '새 제목'
article.save()

# 삭제
article.delete()

# 관계 조회
article.author.username  # ForeignKey 역참조
article.comments.all()   # Reverse Relation
article.tags.all()       # ManyToMany
```

## 다음 단계

**08_Web_Pages**: 클래스형 뷰와 고급 URL 라우팅 배우기

## 참고 자료

- [Django 모델 공식 문서](https://docs.djangoproject.com/en/stable/topics/db/models/)
- [필드 타입 완전 가이드](https://docs.djangoproject.com/en/stable/ref/models/fields/)
- [쿼리셋 API](https://docs.djangoproject.com/en/stable/ref/models/querysets/)
