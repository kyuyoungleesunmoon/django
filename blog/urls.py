from django.urls import path
from . import views

app_name = 'blog'

urlpatterns = [
    # 포스트
    path('', views.post_list, name='post_list'),
    path('post/<int:pk>/', views.post_detail, name='post_detail'),
    path('post/create/', views.PostCreateView.as_view(), name='post_create'),
    path('post/<int:pk>/edit/', views.PostUpdateView.as_view(), name='post_edit'),
    path('post/<int:pk>/delete/', views.PostDeleteView.as_view(), name='post_delete'),
    
    # 댓글
    path('post/<int:pk>/comment/', views.add_comment, name='add_comment'),
    
    # 좋아요 & 북마크
    path('post/<int:pk>/like/', views.toggle_like, name='toggle_like'),
    path('post/<int:pk>/bookmark/', views.toggle_bookmark, name='toggle_bookmark'),
    
    # 카테고리 & 검색
    path('category/<int:pk>/', views.category_posts, name='category_posts'),
    path('search/', views.search, name='search'),
    
    # 대시보드
    path('dashboard/', views.dashboard, name='dashboard'),
]
