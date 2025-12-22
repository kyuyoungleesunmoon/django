# 10: 템플릿 필터 - blog/templatetags/blog_filters.py

from django import template
from django.utils.html import mark_safe
from django.utils.safestring import SafeString
import re

register = template.Library()


# ============== 문자열 필터 ==============

@register.filter
def highlight_text(value, search_term):
    """검색어를 하이라이트처리"""
    if not search_term or not value:
        return value
    
    # 검색어를 <mark> 태그로 감싸기 (대소문자 무시)
    pattern = re.compile(f'({re.escape(search_term)})', re.IGNORECASE)
    highlighted = pattern.sub(r'<mark>\1</mark>', str(value))
    return mark_safe(highlighted)


@register.filter
def truncate_html(value, length=100):
    """HTML 태그를 보존하면서 잘라내기"""
    if len(value) <= length:
        return value
    return mark_safe(value[:length] + '...')


@register.filter
def safe_html(value):
    """HTML을 안전하게 렌더링"""
    return mark_safe(value)


# ============== 날짜 필터 ==============

@register.filter
def korean_date(value):
    """한국식 날짜 포맷팅"""
    if not value:
        return ""
    return value.strftime("%Y년 %m월 %d일")


@register.filter
def korean_datetime(value):
    """한국식 날짜 시간 포맷팅"""
    if not value:
        return ""
    return value.strftime("%Y년 %m월 %d일 %H:%M")


@register.filter
def time_ago(value):
    """몇 시간 전과 같은 상대 시간 표시"""
    from datetime import datetime, timedelta
    from django.utils import timezone
    
    if not value:
        return ""
    
    now = timezone.now()
    diff = now - value
    
    if diff.total_seconds() < 60:
        return "방금 전"
    elif diff.total_seconds() < 3600:
        minutes = int(diff.total_seconds() // 60)
        return f"{minutes}분 전"
    elif diff.total_seconds() < 86400:
        hours = int(diff.total_seconds() // 3600)
        return f"{hours}시간 전"
    elif diff.total_seconds() < 604800:
        days = int(diff.total_seconds() // 86400)
        return f"{days}일 전"
    else:
        return value.strftime("%Y년 %m월 %d일")


# ============== 숫자 필터 ==============

@register.filter
def intcomma(value):
    """숫자에 1000 단위 쉼표 추가"""
    if not value:
        return 0
    return f"{int(value):,}"


@register.filter
def korean_number(value):
    """한국식 숫자 표시 (1,000 → 1천)"""
    if not value:
        return 0
    
    value = int(value)
    
    if value >= 1000000:
        return f"{value // 1000000}백만"
    elif value >= 1000:
        return f"{value // 1000}천"
    else:
        return str(value)


@register.filter
def multiply(value, multiplier):
    """숫자 곱하기"""
    try:
        return float(value) * float(multiplier)
    except (ValueError, TypeError):
        return 0


@register.filter
def percentage(value, total):
    """백분율 계산"""
    try:
        result = (float(value) / float(total)) * 100
        return f"{result:.1f}%"
    except (ValueError, TypeError, ZeroDivisionError):
        return "0%"


# ============== 이미지/파일 필터 ==============

@register.filter
def placeholder_image(image_url, size="300x300"):
    """이미지가 없으면 플레이스홀더 반환"""
    if image_url:
        return image_url
    return f"https://via.placeholder.com/{size}?text=No+Image"


@register.filter
def file_size(bytes_size):
    """파일 크기를 읽기 쉬운 형식으로"""
    if not bytes_size:
        return "0 B"
    
    for unit in ['B', 'KB', 'MB', 'GB']:
        if bytes_size < 1024.0:
            return f"{bytes_size:.1f} {unit}"
        bytes_size /= 1024.0
    return f"{bytes_size:.1f} TB"


@register.filter
def file_extension(filename):
    """파일 확장자 반환"""
    if not filename:
        return ""
    import os
    return os.path.splitext(filename)[1].lower()


# ============== 리스트 필터 ==============

@register.filter
def get_item(dictionary, key):
    """딕셔너리에서 값 가져오기"""
    return dictionary.get(key)


@register.filter
def shuffle(value):
    """리스트를 무작위로 섞기"""
    import random
    if not isinstance(value, list):
        value = list(value)
    random.shuffle(value)
    return value


@register.filter
def chunk(value, size):
    """리스트를 일정 크기의 청크로 나누기"""
    size = int(size)
    return [value[i:i+size] for i in range(0, len(value), size)]


# ============== 조건부 필터 ==============

@register.filter
def default_if_zero(value, default_text):
    """값이 0이면 기본값 사용"""
    if value == 0 or not value:
        return default_text
    return value


@register.filter
def default_if_empty(value, default_text):
    """값이 비어있으면 기본값 사용"""
    if not value:
        return default_text
    return value


@register.filter
def is_even(value):
    """짝수 여부"""
    return int(value) % 2 == 0


@register.filter
def is_odd(value):
    """홀수 여부"""
    return int(value) % 2 != 0


# ============== URL/링크 필터 ==============

@register.filter
def url_safe(value):
    """URL 안전 문자로 변환"""
    from urllib.parse import quote
    if not value:
        return ""
    return quote(str(value))


@register.filter
def build_query_string(dictionary):
    """딕셔너리로 쿼리 문자열 생성"""
    from urllib.parse import urlencode
    if not dictionary:
        return ""
    return urlencode(dictionary)


# ============== 데이터 타입 필터 ==============

@register.filter
def type_of(value):
    """변수의 타입 반환"""
    return type(value).__name__


@register.filter
def bool_to_text(value):
    """불린을 텍스트로"""
    if value:
        return "예"
    return "아니오"


@register.filter
def yesno_korean(value):
    """불린을 한국어로"""
    if value:
        return "있음"
    return "없음"
