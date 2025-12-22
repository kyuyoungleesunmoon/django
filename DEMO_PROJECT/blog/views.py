# 08: Blog 앱의 views.py - 클래스 기반 뷰 (CBV)

from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse_lazy
from django.db.models import Q
from .models import Post, Comment, Category


class PostListView(ListView):
    """모든 발행된 포스트 목록 표시"""
    model = Post
    context_object_name = 'posts'
    template_name = 'blog/post_list.html'
    paginate_by = 10
    
    def get_queryset(self):
        """발행된 포스트만 필터링, 검색 기능 지원"""
        queryset = Post.objects.filter(is_published=True).order_by('-created_at')
        
        # 검색 기능
        search = self.request.GET.get('search')
        if search:
            queryset = queryset.filter(
                Q(title__icontains=search) |
                Q(content__icontains=search) |
                Q(excerpt__icontains=search)
            )
        
        return queryset
    
    def get_context_data(self, **kwargs):
        """추가 컨텍스트 데이터"""
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        context['search'] = self.request.GET.get('search', '')
        return context


class PostDetailView(DetailView):
    """특정 포스트의 상세 정보 표시"""
    model = Post
    context_object_name = 'post'
    template_name = 'blog/post_detail.html'
    slug_field = 'slug'
    slug_url_kwarg = 'slug'
    
    def get_context_data(self, **kwargs):
        """추가 컨텍스트 - 댓글 목록"""
        context = super().get_context_data(**kwargs)
        post = self.get_object()
        context['comments'] = post.comments.filter(is_approved=True)
        return context
    
    def get(self, request, *args, **kwargs):
        """조회수 증가"""
        self.object = self.get_object()
        self.object.views += 1
        self.object.save()
        return super().get(request, *args, **kwargs)


class PostCreateView(LoginRequiredMixin, CreateView):
    """새 포스트 작성"""
    model = Post
    fields = ['title', 'content', 'excerpt', 'is_published']
    template_name = 'blog/post_form.html'
    success_url = reverse_lazy('blog:post-list')
    
    def form_valid(self, form):
        """현재 사용자를 작성자로 설정"""
        form.instance.author = self.request.user
        return super().form_valid(form)


class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    """포스트 수정"""
    model = Post
    fields = ['title', 'content', 'excerpt', 'is_published']
    template_name = 'blog/post_form.html'
    slug_field = 'slug'
    slug_url_kwarg = 'slug'
    
    def test_func(self):
        """자신의 포스트만 수정 가능"""
        post = self.get_object()
        return self.request.user == post.author
    
    def get_success_url(self):
        """수정 후 상세 페이지로 이동"""
        return reverse_lazy('blog:post-detail', kwargs={'slug': self.object.slug})


class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    """포스트 삭제"""
    model = Post
    template_name = 'blog/post_confirm_delete.html'
    success_url = reverse_lazy('blog:post-list')
    slug_field = 'slug'
    slug_url_kwarg = 'slug'
    
    def test_func(self):
        """자신의 포스트만 삭제 가능"""
        post = self.get_object()
        return self.request.user == post.author


class CategoryListView(ListView):
    """특정 카테고리의 포스트 목록"""
    model = Post
    context_object_name = 'posts'
    template_name = 'blog/category_post_list.html'
    paginate_by = 10
    
    def get_queryset(self):
        """카테고리별 포스트 필터링"""
        category_slug = self.kwargs.get('slug')
        category = get_object_or_404(Category, slug=category_slug)
        return Post.objects.filter(is_published=True).order_by('-created_at')
    
    def get_context_data(self, **kwargs):
        """카테고리 정보 추가"""
        context = super().get_context_data(**kwargs)
        category_slug = self.kwargs.get('slug')
        context['category'] = get_object_or_404(Category, slug=category_slug)
        return context

