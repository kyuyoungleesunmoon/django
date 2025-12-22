"""
URL configuration for mysite project.
"""
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('hello/', include('hello.urls')),  # hello 앱의 URL을 포함
    path('', include('hello.urls')),  # 루트 경로도 hello 앱으로
]
