# 08_Web_Pages 실습 프로젝트 - 클래스형 뷰(CBV)

Django의 **클래스형 뷰(Class-Based Views)** 를 학습하기 위한 쇼핑몰 프로젝트입니다.

## 이 프로젝트에서 배우는 것

✅ ListView - 목록 뷰  
✅ DetailView - 상세 뷰  
✅ Context 추가하기  
✅ 쿼리셋 커스터마이징  
✅ URL 라우팅 (as_view())  

## 핵심 개념

### 함수형 뷰 vs 클래스형 뷰

```python
# 함수형 뷰
def product_list(request):
    products = Product.objects.all()
    return render(request, 'products/list.html', {'products': products})

# 클래스형 뷰
class ProductListView(ListView):
    model = Product
    template_name = 'products/list.html'
    context_object_name = 'products'
```

## 빠른 시작

```bash
cd shop
pip install django
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

## 주요 클래스형 뷰

| 클래스 | 용도 | 메서드 |
|--------|------|--------|
| ListView | 목록 조회 | get_queryset(), get_context_data() |
| DetailView | 상세 조회 | get_object() |
| CreateView | 객체 생성 | get_form(), form_valid() |
| UpdateView | 객체 수정 | get_object(), get_form() |
| DeleteView | 객체 삭제 | get_object(), delete() |

## 학습 과제

### 초급
- [ ] 상품 추가/수정 (관리자)
- [ ] 각 URL 페이지 확인
- [ ] 카테고리별 필터링

### 중급
- [ ] Mixin 사용 (`LoginRequiredMixin`)
- [ ] Pagination 커스터마이징
- [ ] Form 클래스 작성

### 고급
- [ ] CreateView/UpdateView 구현
- [ ] 권한 검사 (`UserPassesTestMixin`)
- [ ] 검색 기능 추가

## 다음 단계

**09_Static_Media**: 정적 파일과 미디어 처리

## 참고 자료

- [Django CBV 공식 문서](https://docs.djangoproject.com/en/stable/topics/class-based-views/)
- [Classy CBV Reference](https://ccbv.co.uk/)
