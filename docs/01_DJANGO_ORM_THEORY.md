# Django ORM 심화 가이드

## 1. Django ORM이란?
Django ORM(Object-Relational Mapping)은 Python 객체와 데이터베이스 테이블 간의 매핑을 제공합니다.

### 장점
- SQL을 직접 작성할 필요 없음
- 데이터베이스 종류 변경이 쉬움
- 객체 지향적 코드 작성

---

## 2. 모델(Model) 정의

### 2.1 기본 모델 구조
```python
from django.db import models

class Post(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']  # 최신순 정렬
        verbose_name = 'Post'
        verbose_name_plural = 'Posts'
    
    def __str__(self):
        return self.title
```

### 2.2 필드 타입
- `CharField`: 짧은 텍스트
- `TextField`: 긴 텍스트
- `IntegerField`: 정수
- `FloatField`: 소수점
- `DateTimeField`: 날짜/시간
- `BooleanField`: True/False
- `ForeignKey`: 다대일 관계
- `ManyToManyField`: 다대다 관계
- `OneToOneField`: 일대일 관계

---

## 3. 관계 설정 (Relationships)

### 3.1 ForeignKey (다대일)
```python
class Author(models.Model):
    name = models.CharField(max_length=100)

class Post(models.Model):
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    # on_delete 옵션:
    # - CASCADE: 저자 삭제 시 포스트도 삭제
    # - SET_NULL: 저자 삭제 시 NULL로 설정 (null=True 필요)
    # - PROTECT: 삭제 방지
```

### 3.2 ManyToManyField (다대다)
```python
class Tag(models.Model):
    name = models.CharField(max_length=50)

class Post(models.Model):
    tags = models.ManyToManyField(Tag, related_name='posts')
```

### 3.3 역참조 (Reverse Relations)
```python
post = Post.objects.get(id=1)
post.author  # 저자 조회

author = Author.objects.get(id=1)
author.post_set.all()  # 또는 related_name 사용
author.posts.all()     # related_name='posts' 사용
```

---

## 4. QuerySet 주요 메서드

### 4.1 데이터 조회
```python
Post.objects.all()                    # 모든 포스트
Post.objects.filter(author_id=1)      # 조건 필터링
Post.objects.exclude(author_id=1)     # 제외
Post.objects.get(id=1)                # 단일 객체 (없으면 예외)
Post.objects.first()                  # 첫 번째
Post.objects.last()                   # 마지막
Post.objects.count()                  # 개수
```

### 4.2 필터링
```python
# Q 객체 사용 (AND, OR, NOT)
from django.db.models import Q

Post.objects.filter(
    Q(title__icontains='django') | Q(content__icontains='django')
)

# 필터 연산자
Post.objects.filter(created_at__year=2024)
Post.objects.filter(created_at__gte=datetime.now())
Post.objects.filter(title__startswith='Django')
Post.objects.filter(title__in=['Post1', 'Post2'])
```

### 4.3 정렬 및 슬라이싱
```python
Post.objects.order_by('-created_at')   # 최신순
Post.objects.order_by('title', '-created_at')
Post.objects.order_by('?')             # 랜덤
Post.objects.all()[:5]                 # 처음 5개
Post.objects.all()[5:10]               # 5-10번째
```

### 4.4 수정 및 삭제
```python
# 여러 객체 수정
Post.objects.filter(author_id=1).update(title='New Title')

# 여러 객체 삭제
Post.objects.filter(created_at__year=2023).delete()

# 개별 객체 수정
post = Post.objects.get(id=1)
post.title = 'New Title'
post.save()
```

### 4.5 집계 함수
```python
from django.db.models import Count, Sum, Avg, Q

# 저자별 포스트 개수
Author.objects.annotate(post_count=Count('post'))

# 평균 별점
Movie.objects.annotate(avg_rating=Avg('rating'))

# 조건부 집계
Post.objects.aggregate(
    total=Count('id'),
    recent=Count('id', filter=Q(created_at__year=2024))
)
```

### 4.6 검색 및 조인
```python
# select_related (ForeignKey, OneToOne - SQL JOIN)
Post.objects.select_related('author').all()

# prefetch_related (ManyToMany - 추가 쿼리)
Post.objects.prefetch_related('tags').all()

# values - 특정 필드만 조회
Post.objects.values('id', 'title')

# distinct - 중복 제거
Post.objects.filter(author__name='John').distinct()
```

---

## 5. N+1 쿼리 문제 해결

### 문제 상황
```python
# 나쁜 예: N+1 쿼리 발생
posts = Post.objects.all()
for post in posts:
    print(post.author.name)  # 매번 새로운 쿼리 실행
```

### 해결책
```python
# 좋은 예: select_related 사용
posts = Post.objects.select_related('author').all()
for post in posts:
    print(post.author.name)  # 추가 쿼리 없음
```

---

## 6. 쿼리 최적화 팁

1. **QuerySet은 지연 실행**: 필요할 때까지 DB에 쿼리하지 않음
2. **select_related**: ForeignKey, OneToOne
3. **prefetch_related**: ManyToMany, 역참조
4. **only/defer**: 특정 필드만 로드
5. **distinct**: 중복 제거
6. **explain()**: 쿼리 분석

---

## 7. 트랜잭션

```python
from django.db import transaction

@transaction.atomic
def create_post_with_tags(title, content, tag_names):
    post = Post.objects.create(title=title, content=content)
    for tag_name in tag_names:
        tag, _ = Tag.objects.get_or_create(name=tag_name)
        post.tags.add(tag)
    return post
```

---

## 8. Manager와 QuerySet 커스터마이징

```python
class PublishedManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(is_published=True)

class Post(models.Model):
    title = models.CharField(max_length=100)
    is_published = models.BooleanField(default=False)
    
    objects = models.Manager()       # 기본 manager
    published = PublishedManager()   # 커스텀 manager

# 사용
Post.published.all()  # 발행된 포스트만
```

---

## 요약 팁

- ✅ 쿼리 디버깅: `django.db.connection.queries`
- ✅ 쿼리 확인: `queryset.query`
- ✅ 최적화: `select_related`, `prefetch_related` 활용
- ✅ 대량 작업: `bulk_create`, `bulk_update`
- ✅ 테스트: `django.test.TestCase` 사용
