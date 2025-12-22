from django import template

register = template.Library()

# 커스텀 필터
@register.filter
def truncate_words(text, num):
    """지정된 단어 수로 텍스트 자르기"""
    words = text.split()[:num]
    return ' '.join(words) + '...'

@register.filter
def highlight(text, word):
    """지정된 단어 강조"""
    return text.replace(word, f'<mark>{word}</mark>')

@register.filter
def multiply(value, multiplier):
    """숫자 곱하기"""
    try:
        return int(value) * int(multiplier)
    except (ValueError, TypeError):
        return value

# 커스텀 태그
@register.simple_tag
def get_featured_articles():
    """주요 기사 가져오기"""
    from articles.models import Article
    return Article.objects.filter(is_featured=True)[:3]

@register.inclusion_tag('articles/article_card.html')
def article_card(article):
    """기사 카드 렌더링"""
    return {'article': article}
