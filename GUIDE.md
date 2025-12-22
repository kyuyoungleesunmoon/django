# 예제 구성 요약

이 폴더에는 각 단계별 실습에 필요한 모든 코드가 포함되어 있습니다.

## 📁 폴더 구조 설명

### 01_Introduction/
- Django 기본 개념 학습 자료
- 프로젝트 초기 설정 가이드

### 07_App_Development/
- 앱 생성 및 모델 정의
- blog/models.py - Post, Comment, Category 모델
- pages/models.py - Page, About, Contact 모델

### 08_Web_Pages/
- URL 설정 및 뷰 작성
- blog_urls.py - Blog 앱 URL 패턴
- blog_views.py - CBV (권장)
- blog_views_fbv.py - FBV 대안
- pages_urls.py, pages_views.py - Pages 앱

### 09_Static_Media/
- 정적 파일 및 미디어 파일 관리
- settings_static_media.py - Django 설정
- models_with_media.py - ImageField 추가
- forms_example.py - 파일 유효성 검사

### 10_Page_Improvement/
- 템플릿 개선 및 필터 활용
- blog_filters.py - 커스텀 필터
- post_list_improved.html - 개선된 템플릿

### Template_Examples/
- 실제 사용 가능한 템플릿 예제
- post_list.html - 포스트 목록
- post_detail.html - 포스트 상세
- post_form.html - 포스트 작성/수정

## 🚀 사용 방법

### 1단계: 01 섹션 학습
```bash
THEORY_01_Django_Overview.md 읽기
PROJECT_SETUP.md 따라하기
```

### 2단계: 07 섹션 실습
```bash
# 모델 코드 복사
# 07_App_Development/blog/models.py → 프로젝트의 blog/models.py
# 07_App_Development/pages/models.py → 프로젝트의 pages/models.py

# 마이그레이션
python manage.py makemigrations
python manage.py migrate
```

### 3단계: 08 섹션 실습
```bash
# URL 및 뷰 코드 복사
# 08_Web_Pages/blog_urls.py → 프로젝트의 blog/urls.py
# 08_Web_Pages/blog_views.py → 프로젝트의 blog/views.py
# Template_Examples/*.html → 프로젝트의 templates/
```

### 4단계: 09 섹션 실습
```bash
# settings.py 설정 복사
# 09_Static_Media/settings_static_media.py 참고

# 마이그레이션 (ImageField 추가 후)
python manage.py makemigrations
python manage.py migrate
```

### 5단계: 10 섹션 실습
```bash
# 템플릿 필터 파일 생성
# blog/templatetags/blog_filters.py 생성

# 템플릿 복사
# 10_Page_Improvement/post_list_improved.html 참고
```

## 📚 학습 자료 위치

### 이론
- `*/THEORY_*.md` - 각 단계별 상세 이론

### 실습 코드
- `*/models.py` - 데이터 모델
- `*/views.py` - 뷰 함수/클래스
- `*_urls.py` - URL 패턴
- `*_filters.py` - 커스텀 필터
- `*.html` - 템플릿

### 설정 파일
- `settings_static_media.py` - Django 설정
- `urls_example.py` - URL 라우팅 설정
- `forms_example.py` - 폼 정의

## 💡 팁

1. **코드 복사할 때**
   - 전체 코드를 복사하지 말고 필요한 부분만 선택
   - 주석을 읽고 이해하면서 작성

2. **에러 발생 시**
   - 에러 메시지 확인
   - 파일 경로가 올바른지 확인
   - import 문이 맞는지 확인

3. **테스트 하기**
   - 각 단계 후 runserver로 확인
   - 관리자 페이지에서 데이터 확인

4. **커스터마이징**
   - 코드를 이해하면 자신만의 방식으로 수정
   - 원본 코드는 참고용으로만 사용

## ✅ 완료 체크리스트

- [ ] 01 Django 기본 개념 학습
- [ ] 07-1 앱 생성 및 등록
- [ ] 07-2 데이터베이스 개념 이해
- [ ] 07-3 모델 작성 및 마이그레이션
- [ ] 08-1 URL 설정
- [ ] 08-2 FBV 또는 08-3 CBV 구현
- [ ] 09-1 정적 파일 관리
- [ ] 09-2 미디어 파일 관리
- [ ] 10-1 포스트 목록 개선
- [ ] 10-2 if 문 템플릿 작성
- [ ] 10-3 필터 활용

모든 단계를 완료하면 완전한 Django 블로그 애플리케이션을 만들 수 있습니다!
