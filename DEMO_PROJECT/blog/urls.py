# 08: Blog 앱의 urls.py

from django.urls import path
from . import views

app_name = 'blog'

urlpatterns = [
    # 포스트 목록
    path('', views.PostListView.as_view(), name='post-list'),
    
    # 포스트 상세
    path('post/<slug:slug>/', views.PostDetailView.as_view(), name='post-detail'),
    
    # 포스트 작성
    path('post/new/', views.PostCreateView.as_view(), name='post-create'),
    
    # 포스트 수정
    path('post/<slug:slug>/edit/', views.PostUpdateView.as_view(), name='post-update'),
    
    # 포스트 삭제
    path('post/<slug:slug>/delete/', views.PostDeleteView.as_view(), name='post-delete'),
    
    # 카테고리별 포스트
    path('category/<slug:slug>/', views.CategoryListView.as_view(), name='category-posts'),
]
