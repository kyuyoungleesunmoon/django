# 10. 페이지 구성 개선하기

## 개요
Django 템플릿에서 조건문과 필터를 활용하여 웹 페이지의 표현을 더 풍부하게 만드는 방법을 배웁니다.

---

## 10-1. 포스트 목록 페이지의 문제 파악하기

### 기본 포스트 목록 페이지의 문제점

```html
<!-- 문제가 있는 버전 -->
<div class="posts">
    {% for post in posts %}
        <div class="post">
            <h2>{{ post.title }}</h2>
            <p>{{ post.content }}</p>  <!-- 너무 길다 -->
            <p>작성자: {{ post.author }}</p>
            <p>작성일: {{ post.created_at }}</p>
            <p>조회수: {{ post.views }}</p>
        </div>
    {% endfor %}
</div>
```

### 문제점 분석

1. **콘텐츠 표시 문제**
   - 전체 내용을 표시하면 목록 페이지가 너무 길어짐
   - 요약 텍스트가 필요함

2. **날짜 형식 문제**
   - `2024-01-15 10:30:45.123456+00:00` 같은 형식이 보임
   - 사용자 친화적인 형식으로 변환 필요

3. **이미지 없을 때 처리**
   - 이미지가 없으면 빈 공간이 생김
   - 기본 이미지로 처리해야 함

4. **빈 목록 처리**
   - 포스트가 없으면 아무것도 표시되지 않음
   - 사용자에게 메시지를 보여야 함

5. **조회수 표시**
   - 조회수가 0이면 "(조회 없음)" 같은 메시지 필요
   - 조회수가 많으면 숫자 포맷팅 필요

---

## 10-2. 템플릿 파일에서 if 문 사용하기

### if 문 기본 구문

```html
{% if 조건 %}
    <!-- 참일 때 -->
{% else %}
    <!-- 거짓일 때 -->
{% endif %}
```

### 조건 유형

#### 1. 변수 존재 여부 확인

```html
<!-- 이미지 있을 때만 표시 -->
{% if post.image %}
    <img src="{{ post.image.url }}" alt="{{ post.title }}">
{% else %}
    <img src="{% static 'blog/images/default.png' %}" alt="기본 이미지">
{% endif %}

<!-- 내용 비어있는지 확인 -->
{% if post.excerpt %}
    <p>{{ post.excerpt }}</p>
{% endif %}
```

#### 2. 불린 값 확인

```html
<!-- 발행됨 여부 -->
{% if post.is_published %}
    <span class="badge bg-success">발행됨</span>
{% else %}
    <span class="badge bg-secondary">미발행</span>
{% endif %}
```

#### 3. 비교 연산

```html
<!-- 숫자 비교 -->
{% if post.views > 100 %}
    <span class="popular">인기글</span>
{% elif post.views > 50 %}
    <span class="trending">핫글</span>
{% else %}
    <span class="new">새글</span>
{% endif %}

<!-- 문자열 비교 -->
{% if post.status == 'published' %}
    <span>발행됨</span>
{% elif post.status == 'draft' %}
    <span>임시저장</span>
{% endif %}
```

#### 4. 리스트/쿼리셋 확인

```html
<!-- 목록이 비어있는지 확인 -->
{% if posts %}
    <!-- 포스트가 있을 때 -->
    <div class="posts">
        {% for post in posts %}
            <div class="post">
                <h3>{{ post.title }}</h3>
            </div>
        {% endfor %}
    </div>
{% else %}
    <!-- 포스트가 없을 때 -->
    <p class="text-muted">작성된 포스트가 없습니다.</p>
{% endif %}

<!-- 특정 개수 이상인지 확인 -->
{% if posts|length > 5 %}
    <p>포스트가 많습니다!</p>
{% endif %}
```

#### 5. 복합 조건

```html
<!-- AND 조건 -->
{% if post.is_published and post.views > 0 %}
    <span class="published-popular">인기 발행글</span>
{% endif %}

<!-- OR 조건 -->
{% if post.status == 'published' or post.status == 'featured' %}
    <span>공개 포스트</span>
{% endif %}

<!-- NOT 조건 -->
{% if not post.is_draft %}
    <p>{{ post.content }}</p>
{% endif %}
```

### 개선된 포스트 목록 페이지

```html
{% load static %}

<!DOCTYPE html>
<html>
<head>
    <link rel="stylesheet" href="{% static 'blog/css/style.css' %}">
</head>
<body>
    <div class="container">
        <h1>블로그 포스트</h1>
        
        <!-- 검색 폼 -->
        <form method="get" class="search-form">
            <input type="text" name="search" 
                   placeholder="검색..." 
                   value="{{ search_query }}">
            <button type="submit">검색</button>
        </form>
        
        <!-- 포스트가 있을 때 -->
        {% if posts %}
            <div class="posts-count">
                총 {{ posts|length }}개의 포스트
            </div>
            
            <div class="posts-list">
                {% for post in posts %}
                    <article class="post-card">
                        <!-- 이미지 처리 -->
                        <div class="post-image">
                            {% if post.image %}
                                <img src="{{ post.image.url }}" 
                                     alt="{{ post.title }}"
                                     class="img-fluid">
                            {% else %}
                                <img src="{% static 'blog/images/default-post.png' %}" 
                                     alt="기본 이미지"
                                     class="img-fluid">
                            {% endif %}
                        </div>
                        
                        <div class="post-content">
                            <!-- 제목 -->
                            <h2 class="post-title">
                                <a href="{% url 'blog:post_detail' pk=post.id %}">
                                    {{ post.title }}
                                </a>
                            </h2>
                            
                            <!-- 발행 상태 -->
                            {% if post.is_published %}
                                <span class="badge badge-success">발행됨</span>
                            {% else %}
                                <span class="badge badge-secondary">미발행</span>
                            {% endif %}
                            
                            <!-- 요약 또는 내용 -->
                            <p class="post-excerpt">
                                {% if post.excerpt %}
                                    {{ post.excerpt }}
                                {% else %}
                                    {{ post.content|truncatewords:30 }}
                                {% endif %}
                            </p>
                            
                            <!-- 메타 정보 -->
                            <div class="post-meta">
                                <span class="author">
                                    작성자: 
                                    <strong>{{ post.author.get_full_name|default:post.author.username }}</strong>
                                </span>
                                
                                <!-- 조회수 처리 -->
                                <span class="views">
                                    {% if post.views > 0 %}
                                        조회: <strong>{{ post.views }}</strong>
                                        
                                        <!-- 조회수에 따른 뱃지 -->
                                        {% if post.views > 1000 %}
                                            <span class="badge badge-danger">HOT</span>
                                        {% elif post.views > 500 %}
                                            <span class="badge badge-warning">TRENDING</span>
                                        {% elif post.views > 100 %}
                                            <span class="badge badge-info">POPULAR</span>
                                        {% endif %}
                                    {% else %}
                                        <em>(조회 없음)</em>
                                    {% endif %}
                                </span>
                                
                                <!-- 날짜는 10-3에서 필터로 처리 -->
                                <span class="date">작성일: {{ post.created_at }}</span>
                            </div>
                            
                            <!-- 댓글 수 -->
                            {% if post.comments.count > 0 %}
                                <div class="post-comments">
                                    댓글: {{ post.comments.count }}개
                                </div>
                            {% endif %}
                        </div>
                    </article>
                {% endfor %}
            </div>
        
        <!-- 포스트가 없을 때 -->
        {% else %}
            <div class="alert alert-info">
                <p>작성된 포스트가 없습니다.</p>
                {% if search_query %}
                    <p>'{{ search_query }}'에 해당하는 포스트를 찾을 수 없습니다.</p>
                {% else %}
                    <p>첫 번째 포스트를 작성해보세요!</p>
                {% endif %}
            </div>
        {% endif %}
    </div>
</body>
</html>
```

---

## 10-3. 템플릿 필터 사용하기

### 필터란?
변수의 값을 변환하는 기능입니다. 파이프 `|`로 적용합니다.

### 자주 사용되는 필터

#### 1. 문자열 필터

```html
<!-- 소문자 -->
{{ post.title|lower }}

<!-- 대문자 -->
{{ post.title|upper }}

<!-- 첫 글자만 대문자 -->
{{ post.title|title }}

<!-- 문자열 길이 -->
{{ post.content|length }}

<!-- 공백 제거 -->
{{ " hello world "|striptags }}

<!-- 줄바꿈을 <br>로 변환 -->
{{ post.content|linebreaks }}

<!-- HTML 이스케이프 (보안) -->
{{ user_input|escape }}
```

#### 2. 날짜 필터

```html
<!-- 기본 날짜 형식 -->
{{ post.created_at|date:"Y-m-d" }}
<!-- 결과: 2024-01-15 -->

<!-- 한국 날짜 형식 -->
{{ post.created_at|date:"Y년 m월 d일" }}
<!-- 결과: 2024년 1월 15일 -->

<!-- 시간 포함 -->
{{ post.created_at|date:"Y-m-d H:i:s" }}
<!-- 결과: 2024-01-15 10:30:45 -->

<!-- 상대 시간 (몇 시간 전) -->
{{ post.created_at|timesince }} ago
<!-- 결과: 2시간 ago -->

<!-- 미래 시간까지의 차이 -->
{{ post.deadline|timeuntil }}
```

#### 3. 숫자 필터

```html
<!-- 정수 부분만 -->
{{ 3.14159|floatformat:0 }}
<!-- 결과: 3 -->

<!-- 소수점 2자리 -->
{{ 3.14159|floatformat:2 }}
<!-- 결과: 3.14 -->

<!-- 단위 추가 -->
{{ post.views|default:"0" }}

<!-- 1000 단위로 쉼표 추가 -->
{{ post.views|intcomma }}
<!-- 결과: 1,234 -->
```

#### 4. URL/링크 필터

```html
<!-- URL 안전 처리 -->
<a href="/blog/{{ post.slug|urlencode }}/">{{ post.title }}</a>

<!-- HTML 링크 생성 -->
{{ post.url|urlize }}
```

#### 5. 텍스트 잘라내기 필터

```html
<!-- 단어 기준으로 잘라내기 -->
{{ post.content|truncatewords:30 }}
<!-- 결과: "Lorem ipsum dolor sit amet... (처음 30단어)" -->

<!-- HTML 태그는 무시 -->
{{ post.content|truncatewords_html:50 }}

<!-- 문자 기준으로 잘라내기 -->
{{ post.title|truncatechars:20 }}
<!-- 결과: "This is a long title..." (처음 20글자) -->
```

#### 6. 리스트 필터

```html
<!-- 첫 번째 항목 -->
{{ posts|first }}

<!-- 마지막 항목 -->
{{ posts|last }}

<!-- 역순 정렬 -->
{% for comment in post.comments|dictsort:"created_at" %}
    <p>{{ comment.content }}</p>
{% endfor %}

<!-- 중복 제거 -->
{% for category in posts|dictsortreversed:"category" %}
    ...
{% endfor %}
```

### 필터 조합하기

```html
<!-- 여러 필터를 연결해서 사용 -->
{{ post.created_at|date:"Y-m-d"|upper }}

<!-- 안전하게 처리 -->
<h2>{{ post.title|safe|truncatewords:10 }}</h2>

<!-- 기본값 설정 -->
{{ post.excerpt|default:"요약이 없습니다." }}

<!-- 조건부 처리 -->
{% if post.views > 0 %}
    조회: {{ post.views|intcomma }}회
{% else %}
    조회 없음
{% endif %}
```

### 커스텀 필터 만들기

```python
# blog/templatetags/blog_filters.py

from django import template
import re

register = template.Library()


@register.filter
def mark_safe(value):
    """문자열을 안전하게 마크"""
    return mark_safe(value)


@register.filter
def highlight(value, arg):
    """검색어를 하이라이트"""
    if not arg:
        return value
    
    pattern = re.compile(f'({re.escape(arg)})', re.IGNORECASE)
    return pattern.sub(r'<mark>\1</mark>', value)


@register.filter
def placeholder_image(image_url, size='300x300'):
    """이미지가 없으면 플레이스홀더 반환"""
    if not image_url:
        return f'https://via.placeholder.com/{size}'
    return image_url


# 사용법:
# {{ post.content|highlight:search_query }}
# {{ post.image.url|placeholder_image }}
```

### 개선된 포스트 목록 페이지 (필터 적용)

```html
{% load static %}
{% load blog_filters %}

<div class="posts-list">
    {% for post in posts %}
        <article class="post-card">
            <img src="{{ post.image.url|placeholder_image }}" 
                 alt="{{ post.title }}">
            
            <h2>{{ post.title|truncatewords:10 }}</h2>
            
            <p>{{ post.excerpt|default:post.content|truncatewords:30 }}</p>
            
            <div class="post-meta">
                <!-- 한국 날짜 형식 -->
                작성일: {{ post.created_at|date:"Y년 m월 d일" }}
                
                <!-- 상대 시간 -->
                ({{ post.created_at|timesince }} 전)
                
                <!-- 조회수 포맷팅 -->
                조회: {{ post.views|intcomma }}
            </div>
            
            <!-- 검색어 하이라이트 -->
            {% if search_query %}
                <p class="highlight-text">
                    {{ post.content|highlight:search_query|truncatewords:20 }}
                </p>
            {% endif %}
        </article>
    {% endfor %}
</div>
```

---

## 요약

- **10-1**: 포스트 목록 페이지의 문제점을 파악하는 것이 개선의 첫 단계
- **10-2**: if/else 문으로 조건부 콘텐츠 표시 (이미지, 상태, 빈 목록 처리 등)
- **10-3**: 필터로 날짜, 숫자, 텍스트 등을 원하는 형식으로 변환
- 커스텀 필터를 만들어 프로젝트에 특화된 필터 추가 가능
