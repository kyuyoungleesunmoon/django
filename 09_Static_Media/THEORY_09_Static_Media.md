# 09. 정적 파일과 미디어 파일 관리하기

## 개요
웹 애플리케이션에서는 HTML, CSS, JavaScript, 이미지 등의 파일들을 관리해야 합니다. Django에서 이러한 파일들을 효율적으로 관리하는 방법을 배웁니다.

---

## 09-1. 정적 파일 관리하기

### 정적 파일이란?
변하지 않는 파일들입니다:
- CSS 스타일시트
- JavaScript 파일
- 이미지 (로고, 아이콘 등)
- 폰트 파일
- 라이브러리 (Bootstrap, jQuery 등)

### 정적 파일 디렉토리 구조

```
myproject/
├── manage.py
├── myproject/
├── blog/
│   ├── static/
│   │   ├── blog/
│   │   │   ├── css/
│   │   │   │   └── style.css
│   │   │   ├── js/
│   │   │   │   └── script.js
│   │   │   └── images/
│   │   │       └── logo.png
│   │   └── third_party/
│   │       └── bootstrap/
│   └── templates/
└── static/           # 프로젝트 전체 정적 파일
    ├── css/
    ├── js/
    └── images/
```

### settings.py 설정

```python
# myproject/settings.py

# 정적 파일 URL
STATIC_URL = '/static/'

# 개발 환경에서 정적 파일 위치
STATICFILES_DIRS = [
    BASE_DIR / 'static',
]

# 프로덕션에서 collectstatic 명령으로 수집된 파일 위치
STATIC_ROOT = BASE_DIR / 'staticfiles'

# 정적 파일 검색 경로
STATICFILES_FINDERS = [
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
]
```

### 템플릿에서 정적 파일 사용

```html
{% load static %}

<!DOCTYPE html>
<html>
<head>
    <link rel="stylesheet" href="{% static 'blog/css/style.css' %}">
</head>
<body>
    <img src="{% static 'blog/images/logo.png' %}" alt="Logo">
    <script src="{% static 'blog/js/script.js' %}"></script>
</body>
</html>
```

### 정적 파일 수집 (프로덕션)

```bash
# 모든 정적 파일을 STATIC_ROOT에 수집
python manage.py collectstatic
```

### URL 설정 (개발 환경)

```python
# myproject/urls.py

from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('blog/', include('blog.urls')),
    path('pages/', include('pages.urls')),
]

# 개발 환경에서만 정적 파일 제공
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
```

### 정적 파일 예제

```css
/* blog/static/blog/css/style.css */

body {
    font-family: Arial, sans-serif;
    max-width: 1200px;
    margin: 0 auto;
    padding: 20px;
}

.post {
    margin: 20px 0;
    padding: 20px;
    border: 1px solid #ddd;
    border-radius: 5px;
}

.post-title {
    font-size: 24px;
    font-weight: bold;
    color: #333;
}

.post-meta {
    font-size: 14px;
    color: #999;
    margin-top: 10px;
}
```

```javascript
// blog/static/blog/js/script.js

document.addEventListener('DOMContentLoaded', function() {
    console.log('페이지 로드 완료');
    
    // 클릭 이벤트
    const buttons = document.querySelectorAll('.btn');
    buttons.forEach(button => {
        button.addEventListener('click', function() {
            console.log('버튼 클릭:', this.textContent);
        });
    });
});
```

---

## 09-2. 미디어 파일 관리하기

### 미디어 파일이란?
사용자가 업로드하는 동적 파일들입니다:
- 사용자 프로필 이미지
- 블로그 포스트 이미지
- 첨부 파일 (PDF, 문서 등)

### 미디어 파일 디렉토리 구조

```
myproject/
├── media/           # 미디어 파일 저장소
│   ├── blog/
│   │   ├── posts/
│   │   │   ├── post_1_image.jpg
│   │   │   └── post_2_image.png
│   │   └── thumbnails/
│   ├── users/
│   │   └── profiles/
│   │       └── user_1_profile.jpg
│   └── uploads/
│       └── documents/
└── manage.py
```

### settings.py 설정

```python
# myproject/settings.py

# 미디어 파일 URL
MEDIA_URL = '/media/'

# 미디어 파일 저장 경로
MEDIA_ROOT = BASE_DIR / 'media'

# 미디어 파일 업로드 크기 제한
FILE_UPLOAD_MAX_MEMORY_SIZE = 5242880  # 5MB
DATA_UPLOAD_MAX_MEMORY_SIZE = 5242880  # 5MB

# 허용된 파일 확장자
DATA_UPLOAD_MAX_NUMBER_FIELDS = 10000
```

### 모델에서 미디어 필드 사용

```python
# blog/models.py

from django.db import models

class Post(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    
    # 이미지 필드
    image = models.ImageField(
        upload_to='blog/posts/%Y/%m/',  # 년/월 폴더로 자동 구성
        blank=True,
        null=True,
        verbose_name='대표 이미지'
    )
    
    # 파일 필드
    attachment = models.FileField(
        upload_to='blog/attachments/',
        blank=True,
        null=True,
        verbose_name='첨부 파일'
    )
    
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.title


class UserProfile(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='profile'
    )
    
    # 프로필 사진
    profile_image = models.ImageField(
        upload_to='users/profiles/',
        default='users/default_profile.jpg',
        verbose_name='프로필 이미지'
    )
    
    bio = models.TextField(blank=True)
```

### URL 설정 (개발 환경)

```python
# myproject/urls.py

from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('blog/', include('blog.urls')),
]

# 개발 환경에서 미디어 파일 제공
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
```

### 템플릿에서 미디어 파일 사용

```html
<!-- 이미지 표시 -->
{% if post.image %}
    <img src="{{ post.image.url }}" alt="{{ post.title }}" class="post-image">
{% else %}
    <img src="{% static 'blog/images/default.png' %}" alt="기본 이미지">
{% endif %}

<!-- 파일 다운로드 링크 -->
{% if post.attachment %}
    <a href="{{ post.attachment.url }}" download>파일 다운로드</a>
{% endif %}

<!-- 프로필 이미지 -->
<img src="{{ user.profile.profile_image.url }}" alt="{{ user.username }}">
```

### 이미지 처리 예제

```python
# blog/models.py

from PIL import Image
from django.db import models
import os

class Post(models.Model):
    title = models.CharField(max_length=200)
    image = models.ImageField(upload_to='blog/posts/')
    
    def save(self, *args, **kwargs):
        """이미지 저장 시 썸네일 생성"""
        super().save(*args, **kwargs)
        
        # 이미지 파일 최적화
        if self.image:
            img = Image.open(self.image.path)
            
            # 이미지 크기 제한 (최대 1000px)
            max_size = (1000, 1000)
            img.thumbnail(max_size, Image.Resampling.LANCZOS)
            
            # 품질 설정
            img.save(self.image.path, quality=85, optimize=True)


# admin.py에서 이미지 미리보기
from django.contrib import admin

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ['title', 'image_preview', 'created_at']
    
    def image_preview(self, obj):
        """관리자 페이지에서 이미지 미리보기"""
        if obj.image:
            return f'<img src="{obj.image.url}" width="100" height="100">'
        return '이미지 없음'
    image_preview.allow_tags = True
    image_preview.short_description = '썸네일'
```

### 파일 업로드 유효성 검사

```python
# blog/forms.py

from django import forms
from .models import Post

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'content', 'image', 'attachment']
    
    def clean_image(self):
        """이미지 파일 유효성 검사"""
        image = self.cleaned_data.get('image')
        
        if image:
            # 파일 크기 확인 (5MB 이상이면 에러)
            if image.size > 5 * 1024 * 1024:
                raise forms.ValidationError('이미지는 5MB 이하여야 합니다.')
            
            # 파일 타입 확인
            allowed_types = ['image/jpeg', 'image/png', 'image/gif']
            if image.content_type not in allowed_types:
                raise forms.ValidationError('JPEG, PNG, GIF 형식만 허용됩니다.')
        
        return image
    
    def clean_attachment(self):
        """첨부 파일 유효성 검사"""
        attachment = self.cleaned_data.get('attachment')
        
        if attachment:
            # 파일 크기 확인 (10MB 이상이면 에러)
            if attachment.size > 10 * 1024 * 1024:
                raise forms.ValidationError('파일은 10MB 이하여야 합니다.')
        
        return attachment
```

---

## 요약

- **09-1**: CSS, JS, 이미지 같은 정적 파일은 static/ 폴더에서 관리
- **09-2**: 사용자 업로드 파일은 media/ 폴더에서 관리
- 프로덕션 환경에서는 collectstatic으로 정적 파일을 수집하고 웹 서버에서 직접 제공해야 함
- 파일 업로드 시에는 보안 검사 (파일 크기, 타입 등)를 항상 실시
