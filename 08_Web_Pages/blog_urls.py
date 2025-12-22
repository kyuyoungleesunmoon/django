# 08: Blog 앱의 urls.py

from django.urls import path
from . import views

app_name = 'blog'

urlpatterns = [
    # FBV 예제 (주석 처리)
    # path('', views.post_list, name='post_list'),
    # path('<int:pk>/', views.post_detail, name='post_detail'),
    # path('create/', views.post_create, name='post_create'),
    # path('<int:pk>/update/', views.post_update, name='post_update'),
    # path('<int:pk>/delete/', views.post_delete, name='post_delete'),
    
    # CBV 예제 (권장)
    path('', views.PostListView.as_view(), name='post_list'),
    path('<int:pk>/', views.PostDetailView.as_view(), name='post_detail'),
    path('create/', views.PostCreateView.as_view(), name='post_create'),
    path('<int:pk>/update/', views.PostUpdateView.as_view(), name='post_update'),
    path('<int:pk>/delete/', views.PostDeleteView.as_view(), name='post_delete'),
]
