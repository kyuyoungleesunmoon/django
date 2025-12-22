from django.views.generic import ListView, DetailView
from django.shortcuts import render
from .models import Product, Category

# 클래스형 뷰 (CBV - Class Based View)
class ProductListView(ListView):
    """상품 목록 - ListView 사용"""
    model = Product
    template_name = 'products/product_list.html'
    context_object_name = 'products'
    paginate_by = 10
    queryset = Product.objects.filter(is_active=True)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        return context

class ProductDetailView(DetailView):
    """상품 상세보기 - DetailView 사용"""
    model = Product
    template_name = 'products/product_detail.html'
    context_object_name = 'product'
    slug_field = 'slug'
    
    def get_queryset(self):
        return Product.objects.filter(is_active=True)

class CategoryProductListView(ListView):
    """카테고리별 상품 목록"""
    model = Product
    template_name = 'products/category_products.html'
    context_object_name = 'products'
    paginate_by = 10
    
    def get_queryset(self):
        self.category = Category.objects.get(slug=self.kwargs['slug'])
        return self.category.products.filter(is_active=True)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['category'] = self.category
        context['categories'] = Category.objects.all()
        return context
