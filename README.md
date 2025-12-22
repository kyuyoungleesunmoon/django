# 📚 HTML/CSS 완벽 학습 가이드

Django 개발자를 위한 체계적인 HTML/CSS 학습 커리큘럼입니다.

## 📂 프로젝트 구조

```
html_css강의/
├── beginner-초급/          # 초급 과정
│   ├── 01-theory-이론.html
│   ├── 02-practice-실습.html
│   └── 02-practice-styles.css
│
├── intermediate-중급/       # 중급 과정
│   ├── 01-theory-이론.html
│   ├── 02-practice-실습.html
│   └── 02-practice-styles.css
│
├── advanced-고급/           # 고급 과정
│   ├── 01-theory-이론.html
│   └── 02-practice-실습.html
│
├── nodejs-express-종합/    # Node.js + Express 과정
│   ├── 01-theory-이론.html
│   └── 02-practice-실습/
│       ├── server.js
│       ├── routes/
│       ├── public/
│       └── package.json
│
└── README.md               # 이 파일
```

---

## 🎯 학습 로드맵

### 📘 초급 (Beginner)
**목표:** HTML/CSS의 기초를 완벽히 이해하기

#### 학습 내용
- ✅ HTML 문서 구조 (DOCTYPE, html, head, body)
- ✅ 주요 HTML 태그 (h1~h6, p, a, img, div, span)
- ✅ 시맨틱 태그 (header, nav, main, section, footer)
- ✅ 폼 요소 (input, select, textarea, button) - Django 연동 핵심!
- ✅ CSS 선택자 (태그, 클래스, 아이디)
- ✅ 박스 모델 (margin, padding, border)
- ✅ 기본 스타일 속성 (color, font-size, background)

#### 실습 프로젝트
**나의 프로필 페이지 만들기**
- HTML 구조 작성
- CSS로 스타일링
- 폼 만들기
- 반응형 기초

#### 학습 시간
약 2~3일 (하루 2시간 기준)

---

### 📙 중급 (Intermediate)
**목표:** 현대적인 레이아웃 기법 마스터하기

#### 학습 내용
- ✅ **Flexbox** (실무 필수!)
  - flex-direction, justify-content, align-items
  - flex-grow, flex-shrink, flex-basis
  - 실전 레이아웃 패턴
  
- ✅ **CSS Grid**
  - grid-template-columns/rows
  - grid-area, gap
  - 반응형 Grid
  
- ✅ **반응형 디자인**
  - 미디어 쿼리 (@media)
  - 브레이크포인트 (576px, 768px, 992px, 1200px)
  - 모바일 우선 접근법

#### 실습 프로젝트
**반응형 블로그 레이아웃**
- Hero 섹션 (Grid)
- 포스트 카드 (Flexbox)
- 사이드바
- 완전한 반응형 구현

#### 학습 시간
약 3~5일 (하루 2시간 기준)

---

### 📕 고급 (Advanced)
**목표:** Bootstrap과 Django Template Language 활용

#### 학습 내용
- ✅ **Bootstrap 5**
  - CDN 연결
  - Grid System (12컬럼)
  - 컴포넌트 (Card, Modal, Navbar, Button)
  - 유틸리티 클래스
  
- ✅ **Django Template Language (DTL)**
  - 템플릿 상속 ({% extends %}, {% block %})
  - 변수 출력 ({{ variable }})
  - 제어문 ({% if %}, {% for %})
  - 필터 (|title, |default)

#### 실습 프로젝트
**Django + Bootstrap 대시보드**
- Bootstrap 컴포넌트 활용
- DTL로 동적 데이터 표시
- 완전한 관리자 대시보드 UI

#### 학습 시간
약 2~3일 (하루 2시간 기준)

---

## 🚀 시작하기 - Live Server (필수!)

### ⭐ Live Server 설치 (30초 소요)

1. **VS Code 열기**
2. **Extensions (Ctrl+Shift+X)** 클릭
3. **"Live Server"** 검색 (Ritwick Dey 제작)
4. **Install** 클릭

### 🎯 Live Server 사용법

#### 모든 HTML 파일 실행 방법:
```
1. 파일 탐색기에서 HTML 파일 찾기
2. 파일 우클릭
3. "Open with Live Server" 클릭
4. 브라우저가 자동으로 열림 (보통 http://127.0.0.1:5500)
```

#### 장점:
- ✅ **자동 새로고침** - 파일 저장 시 즉시 반영
- ✅ **간편한 사용** - 클릭 한 번
- ✅ **CORS 문제 없음** - JavaScript fetch 작동
- ✅ **포트 자동 할당** - 충돌 걱정 없음

### 💡 팁
- 여러 HTML 파일을 동시에 열 수 있습니다
- 하단 상태바에 "Port: 5500" 표시 확인
- 종료: 하단 상태바의 "Port: 5500" 클릭

---

## 📖 학습 순서

### 1단계: 이론 학습
각 과정의 `01-theory-이론.html` 파일을 **Live Server로 열어** 개념을 학습합니다.

```
📁 beginner-초급/01-theory-이론.html 우클릭 
   → "Open with Live Server"

📁 intermediate-중급/01-theory-이론.html 우클릭 
   → "Open with Live Server"

📁 advanced-고급/01-theory-이론.html 우클릭 
   → "Open with Live Server"
```

### 2단계: 실습
각 과정의 `02-practice-실습.html` 파일을 **Live Server로 열어** 실습합니다.

```
파일 우클릭 → "Open with Live Server"
코드 수정 → 저장 (Ctrl+S) → 자동으로 브라우저 새로고침!
```

### 3단계: 코드 분석
- HTML 구조 파악
- CSS 스타일 이해
- 반응형 동작 확인 (브라우저 창 크기 조절)

### 4단계: 커스터마이징
- 색상 변경
- 레이아웃 수정
- 새로운 섹션 추가
- 자신만의 프로젝트로 발전

---

## 💡 학습 팁

### 초급 과정
1. **HTML 구조부터:** DOCTYPE, html, head, body의 역할 이해
2. **name 속성 중요:** 폼에서 name 속성이 Django로 전달되는 키입니다
3. **시맨틱 태그:** div만 쓰지 말고 의미 있는 태그 사용 (SEO)
4. **박스 모델 이해:** 개발자 도구로 margin, padding, border 확인

### 중급 과정
1. **Flexbox 우선:** 대부분의 레이아웃은 Flexbox로 해결
2. **Grid는 2D:** 행과 열을 동시에 제어할 때 Grid 사용
3. **반응형 테스트:** 브라우저 개발자 도구(F12)에서 다양한 기기 확인
4. **모바일 우선:** 작은 화면부터 디자인하고 확장

### 고급 과정
1. **Bootstrap 문서:** 공식 문서를 자주 참고하세요
2. **DTL 연습:** Django 프로젝트에서 실제로 사용해보기
3. **컴포넌트 조합:** Bootstrap 컴포넌트를 조합하여 복잡한 UI 구성

---

## 🛠 개발 도구 추천

### VS Code 확장
- **Live Server** - 실시간 미리보기
- **HTML CSS Support** - 자동완성
- **Prettier** - 코드 포맷팅
- **CSS Peek** - CSS 정의 바로 확인

### 브라우저 도구
- **Chrome DevTools** (F12) - 요소 검사, 반응형 테스트
- **Firefox Developer Tools** - CSS Grid 시각화

---

## 📚 추가 학습 자료

### 공식 문서
- [MDN Web Docs](https://developer.mozilla.org/ko/) - HTML/CSS 레퍼런스
- [Bootstrap 5 공식 문서](https://getbootstrap.com/docs/5.3/)
- [Django Template Language](https://docs.djangoproject.com/en/4.2/ref/templates/language/)

### 연습 사이트
- [Flexbox Froggy](https://flexboxfroggy.com/) - Flexbox 게임
- [Grid Garden](https://cssgridgarden.com/) - Grid 게임
- [CSS Diner](https://flukeout.github.io/) - 선택자 연습

---

## 🎯 프로젝트 아이디어

### 초급 프로젝트
- ✅ 개인 프로필 페이지
- ✅ 간단한 명함 사이트
- ✅ 이력서 페이지

### 중급 프로젝트
- ✅ 블로그 레이아웃
- ✅ 포트폴리오 사이트
- ✅ 제품 랜딩 페이지

### 고급 프로젝트
- ✅ 관리자 대시보드
- ✅ 전자상거래 UI
- ✅ SNS 피드 레이아웃

---

## 🤔 자주 묻는 질문 (FAQ)

### Q1: 얼마나 시간이 걸리나요?
**A:** 초급 3일 + 중급 5일 + 고급 3일 = 약 2주 (하루 2시간 기준)

### Q2: CSS 프레임워크를 써도 되나요?
**A:** 네! 하지만 기초를 먼저 익힌 후 사용하세요. 이해도가 훨씬 높아집니다.

### Q3: JavaScript는 언제 배우나요?
**A:** HTML/CSS를 마스터한 후 JavaScript를 배우는 것이 좋습니다.

### Q4: Django와 어떻게 연동하나요?
**A:** 
1. Django 프로젝트 생성
2. templates 폴더에 HTML 파일 복사
3. static 폴더에 CSS 파일 복사
4. views.py에서 render() 사용

```python
def home(request):
    context = {'name': '홍길동'}
    return render(request, 'home.html', context)
```

---

## 📞 지원

학습 중 질문이나 문제가 있다면:
- GitHub Issues에 질문하기
- Django 커뮤니티에 물어보기
- MDN Web Docs 참고하기

---

## ✅ 체크리스트

### 초급 완료 기준
- [ ] HTML 문서 구조 이해
- [ ] 10개 이상의 HTML 태그 사용 가능
- [ ] 폼 만들기 (input, select 등)
- [ ] CSS 선택자 3가지 사용
- [ ] 박스 모델 이해
- [ ] 프로필 페이지 완성

### 중급 완료 기준
- [ ] Flexbox로 레이아웃 구성
- [ ] Grid로 복잡한 레이아웃 구현
- [ ] 미디어 쿼리 작성
- [ ] 반응형 웹사이트 완성
- [ ] 3가지 디바이스에서 테스트

### 고급 완료 기준
- [ ] Bootstrap 컴포넌트 5개 이상 사용
- [ ] DTL 템플릿 상속 이해
- [ ] DTL 변수, 제어문 사용
- [ ] Django 프로젝트에 적용
- [ ] 완전한 대시보드 UI 완성

---

---

## 🚀 Node.js + Express 종합 과정

**목표:** RESTful API 서버 구축 및 프론트엔드-백엔드 완벽 연동

### 📌 학습 내용
- ✅ **Node.js 기초**
  - JavaScript 런타임 환경
  - npm 패키지 관리
  - ES6+ 최신 문법 (import/export, async/await, 화살표 함수)
  
- ✅ **Express 프레임워크**
  - 서버 구축 및 라우팅
  - 미들웨어 아키텍처
  - RESTful API 설계
  - CORS, JSON 파싱
  
- ✅ **CRUD 구현**
  - GET, POST, PUT, PATCH, DELETE
  - 쿼리 파라미터 처리
  - 입력 검증
  
- ✅ **프론트엔드 연동**
  - Fetch API
  - AJAX 통신
  - 실시간 데이터 업데이트

### 📁 프로젝트 구조
```
nodejs-express-종합/
├── 01-theory-이론.html          # 이론 학습
└── 02-practice-실습/
    ├── server.js                # Express 서버
    ├── routes/
    │   └── posts.js            # Posts API
    ├── public/
    │   └── index.html          # Blog Manager UI
    ├── package.json
    ├── .env                    # 환경 변수
    └── README.md
```

### 🎯 실습 프로젝트: Blog Manager
**완전한 RESTful API + 프론트엔드 UI**

#### 백엔드 (Express)
- ✅ RESTful API 서버 (포트 3000)
- ✅ CRUD 완벽 구현
- ✅ 에러 핸들링
- ✅ CORS 설정
- ✅ 환경 변수 관리

#### 프론트엔드 (HTML/CSS/JS)
- ✅ Blog Manager UI
- ✅ 포스트 작성/수정/삭제
- ✅ 실시간 검색 및 필터
- ✅ API 상태 모니터링
- ✅ 개발자 도구

### 🚀 시작하기

#### 1단계: 이론 학습
```bash
# Live Server로 이론 파일 열기
nodejs-express-종합/01-theory-이론.html → 우클릭 → "Open with Live Server"
```

#### 2단계: 백엔드 서버 실행
```bash
cd nodejs-express-종합/02-practice-실습
npm install
node server.js
# 서버 실행: http://localhost:3000
```

#### 3단계: 프론트엔드 실행
```bash
# Live Server로 프론트엔드 열기
public/index.html → 우클릭 → "Open with Live Server"
```

#### 4단계: 테스트
- 브라우저에서 Blog Manager가 열립니다
- API와 자동으로 연결됩니다
- 포스트 CRUD 기능을 테스트하세요!

### 📊 API 엔드포인트

| 메서드 | 엔드포인트 | 설명 |
|--------|-----------|------|
| GET | `/api/posts` | 모든 포스트 조회 |
| GET | `/api/posts/:id` | 특정 포스트 조회 |
| POST | `/api/posts` | 새 포스트 작성 |
| PUT | `/api/posts/:id` | 포스트 전체 수정 |
| PATCH | `/api/posts/:id` | 포스트 부분 수정 |
| DELETE | `/api/posts/:id` | 포스트 삭제 |

### 💡 학습 시간
약 5~7일 (하루 2~3시간 기준)

### 🎓 학습 포인트
- [x] ES6 모듈 (import/export)
- [x] async/await 비동기 처리
- [x] Express Router 모듈화
- [x] RESTful API 설계 원칙
- [x] CORS 처리
- [x] 미들웨어 활용
- [x] 에러 핸들링
- [x] Fetch API
- [x] 프론트엔드-백엔드 연동

---

## 🎉 수료 후

축하합니다! 이제 다음 단계로 나아가세요:

1. **데이터베이스 연동** - MongoDB, PostgreSQL
2. **JWT 인증** - 로그인/회원가입 구현
3. **Django 심화** - DRF와 비교 학습
4. **실전 프로젝트** - 완전한 풀스택 애플리케이션
5. **포트폴리오** - 자신만의 웹사이트 만들기

---

**Happy Coding! 🚀**

---

*이 학습 자료는 Django 개발자를 위해 특별히 제작되었습니다.*
*프론트엔드 기초부터 Django 연동까지 모든 것을 다룹니다.*
