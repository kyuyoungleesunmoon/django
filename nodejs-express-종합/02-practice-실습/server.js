// ============================================
// Express 서버 - 최신 ES6+ 문법 사용
// ============================================

import 'dotenv/config';
import express from 'express';
import cors from 'cors';
import postsRouter from './routes/posts.js';

const app = express();
const PORT = process.env.PORT ?? 3000;

// ============================================
// 미들웨어 설정
// ============================================

// CORS 설정 (프론트엔드와 통신)
app.use(cors({
    origin: process.env.CORS_ORIGIN || 'http://127.0.0.1:5500',
    credentials: true
}));

// JSON 파싱
app.use(express.json());

// URL-encoded 파싱
app.use(express.urlencoded({ extended: true }));

// 정적 파일 제공 (public 폴더)
app.use(express.static('public'));

// 커스텀 로깅 미들웨어
app.use((req, res, next) => {
    const timestamp = new Date().toISOString();
    console.log(`[${timestamp}] ${req.method} ${req.url}`);
    next();
});

// ============================================
// 라우트 설정
// ============================================

// 기본 라우트
app.get('/', (req, res) => {
    res.json({
        message: '🚀 Express API Server',
        version: '1.0.0',
        endpoints: {
            posts: '/api/posts',
            health: '/api/health'
        }
    });
});

// 헬스 체크
app.get('/api/health', (req, res) => {
    res.json({
        status: 'OK',
        timestamp: new Date().toISOString(),
        uptime: process.uptime()
    });
});

// Posts API 라우트
app.use('/api/posts', postsRouter);

// ============================================
// 에러 핸들링 미들웨어
// ============================================

// 404 핸들러
app.use((req, res) => {
    res.status(404).json({
        error: 'Not Found',
        message: `경로를 찾을 수 없습니다: ${req.url}`
    });
});

// 전역 에러 핸들러
app.use((err, req, res, next) => {
    console.error('Error:', err.stack);
    res.status(err.status || 500).json({
        error: err.message || 'Internal Server Error',
        ...(process.env.NODE_ENV === 'development' && { stack: err.stack })
    });
});

// ============================================
// 서버 시작
// ============================================

app.listen(PORT, () => {
    console.log(`
╔════════════════════════════════════════╗
║   🚀 Express Server Running           ║
║   📡 Port: ${PORT}                     ║
║   🌍 Environment: ${process.env.NODE_ENV}   ║
║   📍 URL: http://localhost:${PORT}     ║
╚════════════════════════════════════════╝
    `);
    console.log('✅ API Endpoints:');
    console.log(`   GET  http://localhost:${PORT}/api/posts`);
    console.log(`   GET  http://localhost:${PORT}/api/posts/:id`);
    console.log(`   POST http://localhost:${PORT}/api/posts`);
    console.log(`   PUT  http://localhost:${PORT}/api/posts/:id`);
    console.log(`   DELETE http://localhost:${PORT}/api/posts/:id\n`);
});

export default app;
