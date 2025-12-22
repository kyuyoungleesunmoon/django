# 08: Pages 앱의 urls.py

from django.urls import path
from . import views

app_name = 'pages'

urlpatterns = [
    # 홈페이지
    path('', views.HomePageView.as_view(), name='home'),
    
    # About 페이지
    path('about/', views.AboutPageView.as_view(), name='about'),
    
    # Contact 페이지
    path('contact/', views.ContactPageView.as_view(), name='contact'),
    
    # 페이지 목록
    path('pages/', views.PageListView.as_view(), name='page-list'),
    
    # 페이지 상세
    path('page/<slug:slug>/', views.PageDetailView.as_view(), name='page-detail'),
]
