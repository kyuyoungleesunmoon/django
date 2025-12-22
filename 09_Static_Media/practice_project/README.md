# 09_Static_Media 실습 프로젝트 - 정적 파일과 미디어

정적 파일(CSS, JS)과 미디어 파일(이미지, 동영상) 처리를 배우는 갤러리 프로젝트입니다.

## 학습 내용

✅ STATIC_URL / STATIC_ROOT 설정  
✅ MEDIA_URL / MEDIA_ROOT 설정  
✅ 정적 파일 참조 ({% load static %})  
✅ 미디어 파일 처리  
✅ 파일 업로드  

## 빠른 시작

```bash
cd gallery
pip install django pillow  # pillow는 이미지 처리 필요
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

## 디렉토리 구조

```
gallery/
├── static/              # 정적 파일 (CSS, JS, 이미지)
│   ├── css/
│   └── js/
├── media/               # 사용자 업로드 파일
│   ├── photos/          # 사진
│   └── thumbnails/      # 썸네일
└── templates/
```

## 핵심 설정

```python
# settings.py
STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'
STATICFILES_DIRS = [BASE_DIR / 'static']

MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'
```

## 템플릿에서 사용

```html
{% load static %}

<!-- 정적 파일 -->
<link rel="stylesheet" href="{% static 'css/style.css' %}">
<script src="{% static 'js/gallery.js' %}"></script>

<!-- 미디어 파일 -->
<img src="{{ photo.image.url }}" alt="사진" />
```

## 학습 과제

### 초급
- [ ] 이미지 업로드 (관리자)
- [ ] CSS 스타일 추가
- [ ] 미디어 파일 확인

### 중급
- [ ] 썸네일 생성 로직
- [ ] JavaScript로 갤러리 기능
- [ ] 이미지 검증

### 고급
- [ ] 이미지 최적화
- [ ] CDN 통합
- [ ] S3/클라우드 스토리지

## 다음 단계

**10_Page_Improvement**: 템플릿 필터와 태그

## 참고 자료

- [Django 정적 파일 문서](https://docs.djangoproject.com/en/stable/howto/static-files/)
- [Pillow 이미지 라이브러리](https://pillow.readthedocs.io/)
