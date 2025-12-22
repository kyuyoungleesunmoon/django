# 08: Pages 앱의 views.py

from django.views.generic import ListView, DetailView, TemplateView
from django.shortcuts import render, get_object_or_404
from blog.models import Post


class HomePageView(TemplateView):
    """홈페이지 뷰"""
    template_name = 'pages/home.html'
    
    def get_context_data(self, **kwargs):
        """컨텍스트에 최신 포스트 추가"""
        context = super().get_context_data(**kwargs)
        try:
            context['latest_posts'] = Post.objects.filter(
                is_published=True
            ).order_by('-created_at')[:5]
        except Exception:
            # Post 모델이 없거나 테이블이 생성되지 않은 경우
            context['latest_posts'] = []
        return context


class AboutPageView(TemplateView):
    """About 페이지 뷰"""
    template_name = 'pages/about.html'
    
    def get_context_data(self, **kwargs):
        """About 정보 추가"""
        context = super().get_context_data(**kwargs)
        # from .models import About
        # context['about'] = About.objects.first()
        context['about'] = {
            'title': 'About Us',
            'description': 'Django 블로그 학습 프로젝트입니다.',
        }
        return context


class ContactPageView(TemplateView):
    """Contact 페이지 뷰"""
    template_name = 'pages/contact.html'
    
    def post(self, request, *args, **kwargs):
        """Contact 폼 처리"""
        name = request.POST.get('name')
        email = request.POST.get('email')
        message = request.POST.get('message')
        
        # 이메일 전송 로직 (선택사항)
        # send_email(email, name, message)
        
        context = self.get_context_data(**kwargs)
        context['message'] = '메시지가 전송되었습니다.'
        return self.render_to_response(context)


class PageDetailView(DetailView):
    """일반 페이지 상세 뷰"""
    # from .models import Page
    # model = Page
    template_name = 'pages/page_detail.html'
    context_object_name = 'page'
    slug_field = 'slug'
    
    # def get_queryset(self):
    #     return Page.objects.filter(is_active=True)
