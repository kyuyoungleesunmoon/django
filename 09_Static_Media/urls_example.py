# 09: Django urls.py - 정적 파일 및 미디어 파일 서빙 설정

# 아래 코드를 simpleblog/urls.py에 작성하세요

from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('blog/', include('blog.urls')),
    path('pages/', include('pages.urls')),
]

# ============== 개발 환경에서만 정적 파일/미디어 파일 서빙 ==============
# (프로덕션에서는 웹 서버 (Nginx, Apache)가 직접 제공해야 함)

if settings.DEBUG:
    # 정적 파일 (CSS, JS, 이미지 등)
    urlpatterns += static(
        settings.STATIC_URL, 
        document_root=settings.STATIC_ROOT
    )
    
    # 미디어 파일 (사용자 업로드 파일)
    urlpatterns += static(
        settings.MEDIA_URL, 
        document_root=settings.MEDIA_ROOT
    )


# ============== 에러 페이지 핸들링 ==============

handler404 = 'pages.views.page_not_found'
handler500 = 'pages.views.server_error'
