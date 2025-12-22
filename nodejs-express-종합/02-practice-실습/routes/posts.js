// ============================================
// Posts 라우터 - RESTful API 구현
// ============================================

import express from 'express';

const router = express.Router();

// 메모리 기반 데이터 저장소 (실전에서는 데이터베이스 사용)
let posts = [
    {
        id: 1,
        title: 'Node.js 시작하기',
        content: 'Node.js는 JavaScript 런타임입니다.',
        author: '홍길동',
        createdAt: new Date('2024-01-15'),
        tags: ['nodejs', 'javascript']
    },
    {
        id: 2,
        title: 'Express 프레임워크',
        content: 'Express로 웹 서버를 쉽게 만들 수 있습니다.',
        author: '김철수',
        createdAt: new Date('2024-01-16'),
        tags: ['express', 'backend']
    },
    {
        id: 3,
        title: 'RESTful API 설계',
        content: 'REST 원칙에 따라 API를 설계하는 방법을 알아봅니다.',
        author: '이영희',
        createdAt: new Date('2024-01-17'),
        tags: ['rest', 'api']
    }
];

let nextId = 4;

// ============================================
// GET /api/posts - 모든 포스트 조회
// ============================================
router.get('/', (req, res) => {
    try {
        // 쿼리 파라미터 처리 예제
        const { search, author, sortBy } = req.query;
        
        let filteredPosts = [...posts];
        
        // 검색 기능
        if (search) {
            filteredPosts = filteredPosts.filter(post =>
                post.title.includes(search) || post.content.includes(search)
            );
        }
        
        // 작성자 필터
        if (author) {
            filteredPosts = filteredPosts.filter(post =>
                post.author === author
            );
        }
        
        // 정렬
        if (sortBy === 'date') {
            filteredPosts.sort((a, b) => b.createdAt - a.createdAt);
        } else if (sortBy === 'title') {
            filteredPosts.sort((a, b) => a.title.localeCompare(b.title));
        }
        
        res.json({
            success: true,
            count: filteredPosts.length,
            data: filteredPosts
        });
    } catch (error) {
        res.status(500).json({
            success: false,
            error: error.message
        });
    }
});

// ============================================
// GET /api/posts/:id - 특정 포스트 조회
// ============================================
router.get('/:id', (req, res) => {
    try {
        const id = parseInt(req.params.id);
        const post = posts.find(p => p.id === id);
        
        if (!post) {
            return res.status(404).json({
                success: false,
                error: '포스트를 찾을 수 없습니다.'
            });
        }
        
        res.json({
            success: true,
            data: post
        });
    } catch (error) {
        res.status(500).json({
            success: false,
            error: error.message
        });
    }
});

// ============================================
// POST /api/posts - 새 포스트 생성
// ============================================
router.post('/', (req, res) => {
    try {
        const { title, content, author, tags } = req.body;
        
        // 입력 검증
        if (!title || !content || !author) {
            return res.status(400).json({
                success: false,
                error: 'title, content, author는 필수입니다.'
            });
        }
        
        if (title.length < 3) {
            return res.status(400).json({
                success: false,
                error: '제목은 최소 3자 이상이어야 합니다.'
            });
        }
        
        // 새 포스트 생성
        const newPost = {
            id: nextId++,
            title,
            content,
            author,
            tags: tags || [],
            createdAt: new Date()
        };
        
        posts.push(newPost);
        
        res.status(201).json({
            success: true,
            message: '포스트가 생성되었습니다.',
            data: newPost
        });
    } catch (error) {
        res.status(500).json({
            success: false,
            error: error.message
        });
    }
});

// ============================================
// PUT /api/posts/:id - 포스트 전체 수정
// ============================================
router.put('/:id', (req, res) => {
    try {
        const id = parseInt(req.params.id);
        const { title, content, author, tags } = req.body;
        
        const index = posts.findIndex(p => p.id === id);
        
        if (index === -1) {
            return res.status(404).json({
                success: false,
                error: '포스트를 찾을 수 없습니다.'
            });
        }
        
        // 입력 검증
        if (!title || !content || !author) {
            return res.status(400).json({
                success: false,
                error: 'title, content, author는 필수입니다.'
            });
        }
        
        // 전체 수정 (기존 데이터 완전 대체)
        posts[index] = {
            id,
            title,
            content,
            author,
            tags: tags || [],
            createdAt: posts[index].createdAt,
            updatedAt: new Date()
        };
        
        res.json({
            success: true,
            message: '포스트가 수정되었습니다.',
            data: posts[index]
        });
    } catch (error) {
        res.status(500).json({
            success: false,
            error: error.message
        });
    }
});

// ============================================
// PATCH /api/posts/:id - 포스트 부분 수정
// ============================================
router.patch('/:id', (req, res) => {
    try {
        const id = parseInt(req.params.id);
        const updates = req.body;
        
        const index = posts.findIndex(p => p.id === id);
        
        if (index === -1) {
            return res.status(404).json({
                success: false,
                error: '포스트를 찾을 수 없습니다.'
            });
        }
        
        // 부분 수정 (전달된 필드만 업데이트)
        posts[index] = {
            ...posts[index],
            ...updates,
            id, // ID는 변경 불가
            createdAt: posts[index].createdAt, // 생성일 유지
            updatedAt: new Date()
        };
        
        res.json({
            success: true,
            message: '포스트가 수정되었습니다.',
            data: posts[index]
        });
    } catch (error) {
        res.status(500).json({
            success: false,
            error: error.message
        });
    }
});

// ============================================
// DELETE /api/posts/:id - 포스트 삭제
// ============================================
router.delete('/:id', (req, res) => {
    try {
        const id = parseInt(req.params.id);
        const index = posts.findIndex(p => p.id === id);
        
        if (index === -1) {
            return res.status(404).json({
                success: false,
                error: '포스트를 찾을 수 없습니다.'
            });
        }
        
        const deletedPost = posts.splice(index, 1)[0];
        
        res.json({
            success: true,
            message: '포스트가 삭제되었습니다.',
            data: deletedPost
        });
    } catch (error) {
        res.status(500).json({
            success: false,
            error: error.message
        });
    }
});

export default router;
