# 09-1: Django settings.py - 정적 파일 설정

# 아래 코드를 simpleblog/settings.py에 추가하세요

from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

# ============== 정적 파일 설정 ==============

# 정적 파일 URL (브라우저에서 접근하는 경로)
STATIC_URL = '/static/'

# 개발 환경에서 정적 파일 검색 디렉토리
STATICFILES_DIRS = [
    BASE_DIR / 'static',
]

# 프로덕션에서 collectstatic 명령으로 수집된 파일이 저장될 경로
STATIC_ROOT = BASE_DIR / 'staticfiles'

# 정적 파일을 찾는 방식
STATICFILES_FINDERS = [
    'django.contrib.staticfiles.finders.FileSystemFinder',  # STATICFILES_DIRS에서 찾기
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',  # 각 앱의 static/ 폴더에서 찾기
]

# ============== 미디어 파일 설정 ==============

# 미디어 파일 URL (사용자 업로드 파일)
MEDIA_URL = '/media/'

# 미디어 파일 저장 경로
MEDIA_ROOT = BASE_DIR / 'media'

# 파일 업로드 설정
FILE_UPLOAD_MAX_MEMORY_SIZE = 5242880  # 5MB
DATA_UPLOAD_MAX_MEMORY_SIZE = 5242880  # 5MB
FILE_UPLOAD_PERMISSIONS = 0o644  # 업로드된 파일의 권한

# ============== 정적 파일 버전 관리 ==============
# 프로덕션에서 캐싱 문제를 해결하기 위해 사용
STATICFILES_STORAGE = 'django.contrib.staticfiles.storage.StaticFilesStorage'
# ManifestStaticFilesStorage를 사용하면 파일명에 해시값이 추가됨

# ============== 추가 설정 ==============

# 템플릿에서 static 태그 사용
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'django.template.context_processors.media',  # 미디어 컨텍스트 추가
            ],
        },
    },
]
