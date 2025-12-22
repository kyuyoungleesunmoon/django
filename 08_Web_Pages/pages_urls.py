# 08: Pages 앱의 urls.py

from django.urls import path
from . import views

app_name = 'pages'

urlpatterns = [
    path('', views.HomePageView.as_view(), name='home'),
    path('about/', views.AboutPageView.as_view(), name='about'),
    path('contact/', views.ContactPageView.as_view(), name='contact'),
    path('<slug:slug>/', views.PageDetailView.as_view(), name='page_detail'),
]
