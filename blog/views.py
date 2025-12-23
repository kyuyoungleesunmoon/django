from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.db.models import Q

from .models import Post, Category, Comment, Like, Bookmark
from .forms import PostForm, CommentForm

# 포스트 목록 - 함수형 뷰
def post_list(request):
    posts = Post.objects.filter(published=True).select_related('author', 'category')
    return render(request, 'blog/post_list.html', {'posts': posts})

# 포스트 상세 - 함수형 뷰
def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    post.views += 1
    post.save()
    
    comments = post.comments.all().select_related('author')
    context = {
        'post': post,
        'comments': comments,
        'is_liked': Like.objects.filter(post=post, user=request.user).exists() if request.user.is_authenticated else False,
        'is_bookmarked': Bookmark.objects.filter(post=post, user=request.user).exists() if request.user.is_authenticated else False,
    }
    return render(request, 'blog/post_detail.html', context)

# 포스트 생성 - 클래스형 뷰
class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    form_class = PostForm
    template_name = 'blog/post_form.html'
    success_url = reverse_lazy('blog:post_list')
    
    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

# 포스트 수정
class PostUpdateView(LoginRequiredMixin, UpdateView):
    model = Post
    form_class = PostForm
    template_name = 'blog/post_form.html'
    success_url = reverse_lazy('blog:post_list')
    
    def get_queryset(self):
        return Post.objects.filter(author=self.request.user)

# 포스트 삭제
class PostDeleteView(LoginRequiredMixin, DeleteView):
    model = Post
    template_name = 'blog/post_confirm_delete.html'
    success_url = reverse_lazy('blog:post_list')
    
    def get_queryset(self):
        return Post.objects.filter(author=self.request.user)

# 댓글 작성
@login_required
def add_comment(request, pk):
    post = get_object_or_404(Post, pk=pk)
    
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.author = request.user
            comment.save()
    
    return redirect('blog:post_detail', pk=post.pk)

# 좋아요 토글
@login_required
def toggle_like(request, pk):
    post = get_object_or_404(Post, pk=pk)
    like, created = Like.objects.get_or_create(post=post, user=request.user)
    
    if not created:
        like.delete()
    
    return redirect('blog:post_detail', pk=post.pk)

# 북마크 토글
@login_required
def toggle_bookmark(request, pk):
    post = get_object_or_404(Post, pk=pk)
    bookmark, created = Bookmark.objects.get_or_create(post=post, user=request.user)
    
    if not created:
        bookmark.delete()
    
    return redirect('blog:post_detail', pk=post.pk)

# 카테고리별 포스트
def category_posts(request, pk):
    category = get_object_or_404(Category, pk=pk)
    posts = category.posts.filter(published=True)
    return render(request, 'blog/post_list.html', {'posts': posts, 'category': category})

# 검색
def search(request):
    query = request.GET.get('q', '')
    posts = Post.objects.filter(published=True)
    
    if query:
        posts = posts.filter(
            Q(title__icontains=query) |
            Q(content__icontains=query) |
            Q(author__username__icontains=query)
        )
    
    return render(request, 'blog/search.html', {'posts': posts, 'query': query})

# 대시보드 (내 포스트)
@login_required
def dashboard(request):
    my_posts = Post.objects.filter(author=request.user)
    my_comments = Comment.objects.filter(author=request.user)
    my_likes = Like.objects.filter(user=request.user)
    my_bookmarks = Bookmark.objects.filter(user=request.user)
    
    context = {
        'my_posts': my_posts,
        'my_comments': my_comments,
        'my_likes': my_likes,
        'my_bookmarks': my_bookmarks,
    }
    return render(request, 'blog/dashboard.html', context)

