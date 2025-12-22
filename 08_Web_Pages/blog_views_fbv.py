# 08: Blog 앱의 views.py (FBV 버전)

from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, JsonResponse
from django.views.decorators.http import require_http_methods
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from .models import Post, Comment


def post_list(request):
    """모든 발행된 포스트를 나열하는 FBV"""
    
    # 발행된 포스트 조회
    queryset = Post.objects.filter(is_published=True)
    
    # 검색 기능
    search_query = request.GET.get('search', '')
    if search_query:
        queryset = queryset.filter(
            Q(title__icontains=search_query) |
            Q(content__icontains=search_query)
        )
    
    # 정렬
    sort_by = request.GET.get('sort', '-created_at')
    queryset = queryset.order_by(sort_by)
    
    # 페이지네이션 (선택사항)
    page = request.GET.get('page', 1)
    items_per_page = 10
    
    context = {
        'posts': queryset,
        'search_query': search_query,
        'total_count': queryset.count(),
    }
    
    return render(request, 'blog/post_list.html', context)


def post_detail(request, pk):
    """특정 포스트의 상세 내용을 보여주는 FBV"""
    
    # 발행된 포스트만 조회
    post = get_object_or_404(Post, pk=pk, is_published=True)
    
    # 조회수 증가
    post.views += 1
    post.save(update_fields=['views'])
    
    # 댓글 조회
    comments = post.comments.filter(is_approved=True).order_by('-created_at')
    
    context = {
        'post': post,
        'comments': comments,
    }
    
    return render(request, 'blog/post_detail.html', context)


@login_required(login_url='admin:login')
@require_http_methods(["GET", "POST"])
def post_create(request):
    """새로운 포스트를 생성하는 FBV"""
    
    if request.method == 'POST':
        # POST 요청 처리
        title = request.POST.get('title', '').strip()
        content = request.POST.get('content', '').strip()
        excerpt = request.POST.get('excerpt', '').strip()
        is_published = request.POST.get('is_published') == 'on'
        
        # 유효성 검사
        if not title or not content:
            context = {
                'error': '제목과 내용은 필수입니다.',
                'form_data': request.POST
            }
            return render(request, 'blog/post_form.html', context)
        
        # 포스트 생성
        post = Post.objects.create(
            title=title,
            content=content,
            excerpt=excerpt,
            author=request.user,
            is_published=is_published
        )
        
        return redirect('blog:post_detail', pk=post.pk)
    
    # GET 요청 처리 - 폼 표시
    return render(request, 'blog/post_form.html')


@login_required(login_url='admin:login')
@require_http_methods(["GET", "POST"])
def post_update(request, pk):
    """포스트를 수정하는 FBV"""
    
    # 포스트 조회
    post = get_object_or_404(Post, pk=pk)
    
    # 작성자 확인
    if post.author != request.user:
        return redirect('blog:post_detail', pk=pk)
    
    if request.method == 'POST':
        # 포스트 업데이트
        post.title = request.POST.get('title', post.title).strip()
        post.content = request.POST.get('content', post.content).strip()
        post.excerpt = request.POST.get('excerpt', post.excerpt).strip()
        post.is_published = request.POST.get('is_published') == 'on'
        post.save()
        
        return redirect('blog:post_detail', pk=post.pk)
    
    # GET 요청 - 폼 표시
    context = {'post': post, 'is_update': True}
    return render(request, 'blog/post_form.html', context)


@login_required(login_url='admin:login')
@require_http_methods(["GET", "POST"])
def post_delete(request, pk):
    """포스트를 삭제하는 FBV"""
    
    post = get_object_or_404(Post, pk=pk)
    
    # 작성자 확인
    if post.author != request.user:
        return redirect('blog:post_detail', pk=pk)
    
    if request.method == 'POST':
        post.delete()
        return redirect('blog:post_list')
    
    # GET 요청 - 삭제 확인 페이지 표시
    context = {'post': post}
    return render(request, 'blog/post_confirm_delete.html', context)


@login_required(login_url='admin:login')
def add_comment(request, pk):
    """댓글 추가 FBV"""
    
    post = get_object_or_404(Post, pk=pk)
    
    if request.method == 'POST':
        author = request.POST.get('author', '').strip()
        email = request.POST.get('email', '').strip()
        content = request.POST.get('content', '').strip()
        
        if author and email and content:
            Comment.objects.create(
                post=post,
                author=author,
                email=email,
                content=content,
                is_approved=False  # 관리자 승인 필요
            )
            
            return redirect('blog:post_detail', pk=pk)
    
    return redirect('blog:post_detail', pk=pk)


def get_post_count(request):
    """JSON으로 포스트 수 반환 (API 예제)"""
    count = Post.objects.filter(is_published=True).count()
    return JsonResponse({'count': count})
