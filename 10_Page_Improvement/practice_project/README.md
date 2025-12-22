# 10_Page_Improvement 실습 프로젝트 - 템플릿 필터와 태그

Django의 **템플릿 필터**와 **커스텀 태그**를 배우는 뉴스 사이트 프로젝트입니다.

## 이 프로젝트에서 배우는 것

✅ 내장 필터 (date, truncatewords, upper, lower 등)  
✅ 커스텀 필터 정의  
✅ 커스텀 태그 정의  
✅ Inclusion 태그  
✅ 템플릿 상속과 재사용  

## 제공되는 커스텀 필터

```django
<!-- 텍스트를 지정된 단어 수로 자르기 -->
{{ text|truncate_words:30 }}

<!-- 특정 단어 강조하기 -->
{{ text|highlight:"Django" }}

<!-- 숫자 곱하기 -->
{{ 5|multiply:3 }}
```

## 제공되는 커스텀 태그

```django
<!-- 주요 기사 가져오기 -->
{% get_featured_articles as featured %}

<!-- 기사 카드 렌더링 -->
{% article_card article %}
```

## 빠른 시작

```bash
cd news
pip install django
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

## 핵심 개념

### 필터 vs 태그

```django
{# 필터: 값을 수정 #}
{{ title|upper }}
{{ date|date:"Y-m-d" }}

{# 태그: 로직 처리 #}
{% if article.is_featured %}
{% for article in articles %}
{% load article_tags %}
```

## 템플릿태그 파일 구조

```
articles/
└── templatetags/
    ├── __init__.py
    └── article_tags.py  # 커스텀 필터와 태그 정의
```

## 학습 과제

### 초급
- [ ] 기사 추가 (관리자)
- [ ] 템플릿 필터 사용
- [ ] 커스텀 필터 테스트

### 중급
- [ ] 새로운 커스텀 필터 작성
- [ ] 커스텀 태그 정의
- [ ] Inclusion 태그 활용

### 고급
- [ ] 복잡한 로직의 태그
- [ ] 필터 체이닝
- [ ] 템플릿 최적화

## 유용한 내장 필터

| 필터 | 용도 |
|------|------|
| `upper` | 대문자 |
| `lower` | 소문자 |
| `capitalize` | 첫 글자만 대문자 |
| `date:"Y-m-d"` | 날짜 포맷 |
| `truncatewords:30` | 단어 자르기 |
| `length` | 길이 |
| `pluralize` | 복수형 |
| `default` | 기본값 |
| `safe` | HTML 렌더링 |

## 다음 단계

모든 단계 완료! 이제 실제 프로젝트를 만들어보세요.

## 참고 자료

- [Django 필터 문서](https://docs.djangoproject.com/en/stable/ref/templates/builtins/#built-in-filter-reference)
- [Django 태그 문서](https://docs.djangoproject.com/en/stable/ref/templates/builtins/#built-in-tag-reference)
- [커스텀 필터/태그](https://docs.djangoproject.com/en/stable/howto/custom-template-tags/)
