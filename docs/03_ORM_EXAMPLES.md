# Django ORM - 실전 예제

## 1. QuerySet 최적화 예제

### 나쁜 예 (N+1 문제)
```python
# 1번의 메인 쿼리 + 각 포스트마다 1번씩 = 1 + n번 쿼리
posts = Post.objects.all()
for post in posts:
    print(post.author.username)  # 매번 새로운 쿼리 실행!
```

### 좋은 예 (최적화)
```python
# 2번의 쿼리만 실행 (1 + 1)
posts = Post.objects.select_related('author').all()
for post in posts:
    print(post.author.username)  # 추가 쿼리 없음
```

---

## 2. ManyToMany 최적화

### 나쁜 예
```python
posts = Post.objects.all()
for post in posts:
    print(post.tags.all())  # 각 포스트마다 별도의 쿼리
```

### 좋은 예
```python
posts = Post.objects.prefetch_related('tags').all()
for post in posts:
    print(post.tags.all())  # 미리 로드된 데이터 사용
```

---

## 3. 복잡한 필터링

### Q 객체 사용
```python
from django.db.models import Q

# OR 연산
posts = Post.objects.filter(
    Q(title__icontains='django') | 
    Q(content__icontains='django')
)

# AND 연산
posts = Post.objects.filter(
    Q(author__username='john') & 
    Q(status='published')
)

# NOT 연산
posts = Post.objects.filter(~Q(status='draft'))

# 복합
posts = Post.objects.filter(
    (Q(status='published') | Q(is_featured=True)) &
    ~Q(author__username='admin')
)
```

---

## 4. 집계 및 Annotation

### 저자별 포스트 개수
```python
from django.db.models import Count

authors = User.objects.annotate(
    post_count=Count('posts')
).filter(post_count__gte=5)
```

### 댓글이 많은 포스트
```python
posts = Post.objects.annotate(
    comment_count=Count('comments')
).order_by('-comment_count')[:10]
```

### 여러 통계
```python
from django.db.models import Count, Sum, Avg

stats = Post.objects.aggregate(
    total_posts=Count('id'),
    total_comments=Count('comments'),
    avg_comments=Avg('comments__id'),
    featured_count=Count('id', filter=Q(is_featured=True))
)
```

---

## 5. 배치 작업

### 대량 생성
```python
posts = [
    Post(title=f'Post {i}', content='...', author=user)
    for i in range(1000)
]
Post.objects.bulk_create(posts, batch_size=100)
```

### 대량 업데이트
```python
Post.objects.filter(status='draft').update(
    status='archived',
    updated_at=datetime.now()
)
```

### 대량 삭제
```python
Post.objects.filter(views__lt=10).delete()
```

---

## 6. 트랜잭션

### 원자적 작업 (모두 성공 또는 모두 실패)
```python
from django.db import transaction

@transaction.atomic
def create_post_with_tags(title, content, tag_names):
    post = Post.objects.create(
        title=title,
        content=content,
        author=request.user
    )
    
    for tag_name in tag_names:
        tag, _ = Tag.objects.get_or_create(name=tag_name)
        post.tags.add(tag)
    
    return post

# 사용
try:
    post = create_post_with_tags('Title', 'Content', ['Django', 'ORM'])
except Exception as e:
    # 모든 변경사항이 자동으로 롤백됨
    print(f"Error: {e}")
```

---

## 7. 쿼리 분석

### 쿼리 확인
```python
# SQL 문 확인
posts = Post.objects.filter(status='published')
print(posts.query)

# 실행된 쿼리 확인
from django.db import connection
posts = Post.objects.filter(status='published').select_related('author')
print(connection.queries)
```

### 쿼리 개수 제한
```python
from django.test.utils import override_settings
from django.db import connection

@override_settings(DEBUG=True)
def test_query_count():
    queries_before = len(connection.queries)
    
    posts = Post.objects.select_related('author').all()
    for post in posts:
        print(post.author.username)
    
    queries_after = len(connection.queries)
    print(f"Queries executed: {queries_after - queries_before}")
```

---

## 8. F 객체와 Q 객체

### F 객체 - 데이터베이스 레벨 계산
```python
from django.db.models import F

# views 를 1 증가시키기 (Python 레벨이 아닌 DB 레벨)
Post.objects.filter(id=1).update(views=F('views') + 1)

# 두 필드 비교
posts = Post.objects.filter(views__gt=F('bookmarks__count'))
```

---

## 9. Prefetch 객체로 더 세밀한 제어

```python
from django.db.models import Prefetch

# 최근 댓글 5개만 미리 로드
recent_comments = Comment.objects.filter(is_approved=True).order_by('-created_at')[:5]
prefetch = Prefetch('comments', queryset=recent_comments)

posts = Post.objects.prefetch_related(prefetch)
```

---

## 10. 커스텀 Manager

```python
class PublishedManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(status='published')

class FeaturedManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(is_featured=True)

class Post(models.Model):
    # ...
    objects = models.Manager()      # 기본
    published = PublishedManager()  # 발행된 포스트만
    featured = FeaturedManager()    # 주목 포스트만

# 사용
posts = Post.published.all()
featured = Post.featured.all()
```

---

## 11. exists() vs count() vs len()

```python
# ❌ 나쁜 예: 모든 데이터 메모리에 로드
if len(Post.objects.filter(status='draft')):
    print("Draft posts exist")

# ✅ 좋은 예: 존재 여부만 확인
if Post.objects.filter(status='draft').exists():
    print("Draft posts exist")

# ❌ 나쁜 예: 모든 포스트 로드 후 개수 셈
count = len(Post.objects.all())

# ✅ 좋은 예: 데이터베이스에서 개수만 조회
count = Post.objects.count()
```

---

## 12. values() vs values_list()

```python
# 딕셔너리 반환
posts = Post.objects.values('id', 'title', 'author__username')
# [{'id': 1, 'title': 'Post 1', 'author__username': 'john'}, ...]

# 튜플 반환 (더 가볍다)
posts = Post.objects.values_list('id', 'title', flat=False)
# [(1, 'Post 1'), (2, 'Post 2'), ...]

# flat=True는 단일 필드만 가능
post_ids = Post.objects.values_list('id', flat=True)
# [1, 2, 3, ...]
```

---

## 13. distinct() - 중복 제거

```python
# 서로 다른 저자를 가진 포스트들
posts = Post.objects.filter(
    category='Django'
).distinct('author')
```

---

## 14. get_or_create

```python
tag, created = Tag.objects.get_or_create(
    name='Django',
    defaults={'slug': 'django'}
)

if created:
    print(f"New tag created: {tag}")
else:
    print(f"Tag already exists: {tag}")
```

---

## 15. update_or_create

```python
post, created = Post.objects.update_or_create(
    id=1,
    defaults={
        'title': 'Updated Title',
        'content': 'Updated Content'
    }
)

print(f"Created: {created}, Post: {post}")
```
