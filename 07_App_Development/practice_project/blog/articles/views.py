from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from .models import Article, Category, Comment

def article_list(request):
    """발행된 게시글 목록"""
    articles = Article.objects.filter(is_published=True)
    
    # 카테고리 필터링
    category = request.GET.get('category')
    if category:
        articles = articles.filter(category__name=category)
    
    context = {
        'articles': articles,
        'categories': Category.objects.all(),
    }
    return render(request, 'articles/article_list.html', context)

def article_detail(request, slug):
    """게시글 상세보기"""
    article = get_object_or_404(Article, slug=slug, is_published=True)
    
    # 조회수 증가
    article.view_count += 1
    article.save(update_fields=['view_count'])
    
    # 댓글 조회
    comments = article.comments.filter(is_approved=True)
    
    context = {
        'article': article,
        'comments': comments,
    }
    return render(request, 'articles/article_detail.html', context)

def category_articles(request, category_name):
    """특정 카테고리의 게시글"""
    category = get_object_or_404(Category, name=category_name)
    articles = category.articles.filter(is_published=True)
    
    context = {
        'category': category,
        'articles': articles,
        'categories': Category.objects.all(),
    }
    return render(request, 'articles/category_articles.html', context)
