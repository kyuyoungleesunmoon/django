# Express RESTful API 실습 프로젝트

## 🚀 시작하기

### 1단계: 패키지 설치
```bash
npm install
```

### 2단계: 서버 시작
```bash
# 일반 모드
npm start

# 개발 모드 (파일 변경시 자동 재시작)
npm run dev
```

### 3단계: 프론트엔드 열기
1. VS Code에서 `public/index.html` 파일을 엽니다
2. 파일을 우클릭하고 **"Open with Live Server"** 선택
3. 브라우저에서 자동으로 열립니다 (보통 `http://127.0.0.1:5500`)

## 📡 API 엔드포인트

### 포스트 API

| 메서드 | 엔드포인트 | 설명 | 예제 |
|--------|-----------|------|------|
| GET | `/api/posts` | 모든 포스트 조회 | `GET http://localhost:3000/api/posts` |
| GET | `/api/posts/:id` | 특정 포스트 조회 | `GET http://localhost:3000/api/posts/1` |
| POST | `/api/posts` | 새 포스트 작성 | `POST http://localhost:3000/api/posts` |
| PUT | `/api/posts/:id` | 포스트 전체 수정 | `PUT http://localhost:3000/api/posts/1` |
| PATCH | `/api/posts/:id` | 포스트 부분 수정 | `PATCH http://localhost:3000/api/posts/1` |
| DELETE | `/api/posts/:id` | 포스트 삭제 | `DELETE http://localhost:3000/api/posts/1` |

### 쿼리 파라미터
```
GET /api/posts?search=nodejs          # 검색
GET /api/posts?author=홍길동          # 작성자 필터
GET /api/posts?sortBy=date            # 정렬 (date, title)
```

## 📝 사용 예제

### 1. 모든 포스트 조회
```javascript
const response = await fetch('http://localhost:3000/api/posts');
const result = await response.json();
console.log(result);
```

### 2. 새 포스트 작성
```javascript
const response = await fetch('http://localhost:3000/api/posts', {
    method: 'POST',
    headers: {
        'Content-Type': 'application/json'
    },
    body: JSON.stringify({
        title: '새 포스트',
        content: '포스트 내용입니다.',
        author: '홍길동',
        tags: ['nodejs', 'express']
    })
});
const result = await response.json();
console.log(result);
```

### 3. 포스트 수정
```javascript
// PATCH - 부분 수정
const response = await fetch('http://localhost:3000/api/posts/1', {
    method: 'PATCH',
    headers: {
        'Content-Type': 'application/json'
    },
    body: JSON.stringify({
        title: '수정된 제목'
    })
});
```

### 4. 포스트 삭제
```javascript
const response = await fetch('http://localhost:3000/api/posts/1', {
    method: 'DELETE'
});
const result = await response.json();
console.log(result);
```

## 🛠️ 프로젝트 구조

```
02-practice-실습/
├── server.js              # 메인 서버 파일
├── routes/
│   └── posts.js           # Posts 라우터
├── public/
│   └── index.html         # 프론트엔드 UI
├── package.json           # 프로젝트 설정
├── .env                   # 환경 변수
├── .gitignore             # Git 제외 파일
└── README.md              # 이 파일
```

## 🔧 환경 변수 (.env)

```env
PORT=3000
NODE_ENV=development
CORS_ORIGIN=http://127.0.0.1:5500
```

## 📚 학습 포인트

### ✅ 완료한 내용
- [x] Express 서버 구축
- [x] RESTful API 설계
- [x] CRUD 기능 구현
- [x] 미들웨어 사용 (CORS, JSON 파싱, 로깅)
- [x] 에러 핸들링
- [x] ES6 모듈 (import/export)
- [x] async/await 비동기 처리
- [x] 쿼리 파라미터 처리
- [x] 입력 검증
- [x] 프론트엔드-백엔드 연동

### 🎯 추가로 학습할 내용
- [ ] 데이터베이스 연동 (MongoDB, PostgreSQL)
- [ ] JWT 인증
- [ ] 파일 업로드
- [ ] WebSocket 실시간 통신
- [ ] API 문서화 (Swagger)
- [ ] 단위 테스트

## ❓ 자주 묻는 질문

### Q1: CORS 오류가 발생합니다
**A:** `.env` 파일의 `CORS_ORIGIN`을 Live Server 주소와 일치시키세요.

### Q2: 포트가 이미 사용 중입니다
**A:** `.env` 파일에서 `PORT`를 다른 번호로 변경하세요 (예: 3001).

### Q3: npm install이 실패합니다
**A:** Node.js 버전을 확인하세요 (v18 이상 권장).

## 🔗 참고 자료
- [Express 공식 문서](https://expressjs.com/)
- [MDN - Fetch API](https://developer.mozilla.org/ko/docs/Web/API/Fetch_API)
- [REST API 설계 가이드](https://restfulapi.net/)

## 📞 문의
문제가 발생하면 이슈를 등록해주세요!
