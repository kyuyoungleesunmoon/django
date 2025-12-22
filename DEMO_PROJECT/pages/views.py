# 08: Pages 앱의 views.py

from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView, DetailView, TemplateView
from .models import Page, About, Contact
from blog.models import Post


class HomePageView(TemplateView):
    """홈페이지"""
    template_name = 'pages/home.html'
    
    def get_context_data(self, **kwargs):
        """최신 포스트 5개 표시"""
        context = super().get_context_data(**kwargs)
        context['latest_posts'] = Post.objects.filter(is_published=True)[:5]
        return context


class AboutPageView(DetailView):
    """About 페이지"""
    model = About
    context_object_name = 'about'
    template_name = 'pages/about.html'
    
    def get_object(self):
        """첫 번째 About 객체 반환"""
        return About.objects.first()


class ContactPageView(DetailView):
    """Contact 페이지"""
    model = Contact
    context_object_name = 'contact'
    template_name = 'pages/contact.html'
    
    def get_object(self):
        """첫 번째 Contact 객체 반환"""
        return Contact.objects.first()


class PageDetailView(DetailView):
    """정적 페이지 상세"""
    model = Page
    context_object_name = 'page'
    template_name = 'pages/page_detail.html'
    slug_field = 'slug'
    slug_url_kwarg = 'slug'
    
    def get_queryset(self):
        """활성화된 페이지만"""
        return Page.objects.filter(is_active=True)


class PageListView(ListView):
    """모든 페이지 목록"""
    model = Page
    context_object_name = 'pages'
    template_name = 'pages/page_list.html'
    
    def get_queryset(self):
        """활성화된 페이지만, 순서로 정렬"""
        return Page.objects.filter(is_active=True).order_by('order')

