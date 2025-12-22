# 08: Blog 앱의 views.py (CBV 버전 - 권장)

from django.views.generic import (
    ListView, DetailView, CreateView, UpdateView, DeleteView
)
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse_lazy
from django.db.models import Q
from django.core.exceptions import PermissionDenied

try:
    from .models import Post, Comment
except ImportError:
    # 모델이 정의되지 않은 경우를 위한 fallback
    Post = None
    Comment = None


class PostListView(ListView):
    """블로그 포스트 목록을 보여주는 뷰"""
    model = Post
    template_name = 'blog/post_list.html'
    context_object_name = 'posts'
    paginate_by = 10
    
    def get_queryset(self):
        """발행된 포스트만 필터링"""
        queryset = Post.objects.filter(is_published=True)
        
        # 검색 기능
        search_query = self.request.GET.get('search', '')
        if search_query:
            queryset = queryset.filter(
                Q(title__icontains=search_query) |
                Q(content__icontains=search_query)
            )
        
        return queryset.order_by('-created_at')
    
    def get_context_data(self, **kwargs):
        """컨텍스트에 검색어 추가"""
        context = super().get_context_data(**kwargs)
        context['search_query'] = self.request.GET.get('search', '')
        return context


class PostDetailView(DetailView):
    """포스트 상세 내용을 보여주는 뷰"""
    model = Post
    template_name = 'blog/post_detail.html'
    context_object_name = 'post'
    
    def get_queryset(self):
        """발행된 포스트만"""
        return Post.objects.filter(is_published=True)
    
    def get_context_data(self, **kwargs):
        """컨텍스트에 댓글 추가"""
        context = super().get_context_data(**kwargs)
        context['comments'] = self.object.comments.filter(is_approved=True)
        return context
    
    def get(self, request, *args, **kwargs):
        """조회수 증가"""
        response = super().get(request, *args, **kwargs)
        self.object.views += 1
        self.object.save(update_fields=['views'])
        return response


class PostCreateView(LoginRequiredMixin, CreateView):
    """포스트 생성 뷰"""
    model = Post
    template_name = 'blog/post_form.html'
    fields = ['title', 'content', 'excerpt', 'is_published']
    login_url = 'admin:login'  # 로그인하지 않은 경우 리다이렉트
    
    def form_valid(self, form):
        """폼 유효성 확인 후 작성자 설정"""
        form.instance.author = self.request.user
        return super().form_valid(form)
    
    def get_success_url(self):
        """성공 후 이동할 URL"""
        return reverse_lazy('blog:post_detail', kwargs={'pk': self.object.pk})


class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    """포스트 수정 뷰"""
    model = Post
    template_name = 'blog/post_form.html'
    fields = ['title', 'content', 'excerpt', 'is_published']
    login_url = 'admin:login'
    
    def get_queryset(self):
        """현재 사용자의 포스트만"""
        return Post.objects.filter(author=self.request.user)
    
    def test_func(self):
        """작성자만 수정 가능한지 확인"""
        post = self.get_object()
        return post.author == self.request.user
    
    def get_success_url(self):
        return reverse_lazy('blog:post_detail', kwargs={'pk': self.object.pk})


class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    """포스트 삭제 뷰"""
    model = Post
    template_name = 'blog/post_confirm_delete.html'
    success_url = reverse_lazy('blog:post_list')
    login_url = 'admin:login'
    
    def get_queryset(self):
        """현재 사용자의 포스트만"""
        return Post.objects.filter(author=self.request.user)
    
    def test_func(self):
        """작성자만 삭제 가능한지 확인"""
        post = self.get_object()
        return post.author == self.request.user


# ============== 페이지 앱의 뷰 ==============

class PageListView(ListView):
    """페이지 목록 뷰"""
    model = Post  # 실제로는 pages.models.Page를 사용
    template_name = 'pages/page_list.html'
    context_object_name = 'pages'
    
    def get_queryset(self):
        """활성화된 페이지만"""
        # from pages.models import Page
        # return Page.objects.filter(is_active=True)
        pass


class PageDetailView(DetailView):
    """페이지 상세 뷰"""
    model = Post  # 실제로는 pages.models.Page를 사용
    template_name = 'pages/page_detail.html'
    context_object_name = 'page'
    
    def get_queryset(self):
        # from pages.models import Page
        # return Page.objects.filter(is_active=True)
        pass
