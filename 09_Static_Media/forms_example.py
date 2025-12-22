# 09: Django forms.py - 파일 업로드 폼과 유효성 검사

from django import forms
from blog.models import Post, Comment
import os
from PIL import Image


class PostForm(forms.ModelForm):
    """블로그 포스트 작성/수정 폼"""
    
    class Meta:
        model = Post
        fields = ['title', 'content', 'excerpt', 'image', 'is_published']
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': '포스트 제목을 입력하세요'
            }),
            'content': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 8,
                'placeholder': '포스트 내용을 입력하세요'
            }),
            'excerpt': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': '포스트 요약'
            }),
            'image': forms.FileInput(attrs={
                'class': 'form-control',
                'accept': 'image/*'
            }),
            'is_published': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            }),
        }
    
    def clean_image(self):
        """이미지 파일 유효성 검사"""
        image = self.cleaned_data.get('image')
        
        if image:
            # 파일 크기 확인 (5MB 이상이면 에러)
            max_size = 5 * 1024 * 1024  # 5MB
            if image.size > max_size:
                raise forms.ValidationError(
                    f'이미지는 5MB 이하여야 합니다. '
                    f'(현재: {image.size / 1024 / 1024:.2f}MB)'
                )
            
            # 파일 타입 확인
            allowed_types = ['image/jpeg', 'image/png', 'image/gif', 'image/webp']
            if image.content_type not in allowed_types:
                raise forms.ValidationError(
                    'JPEG, PNG, GIF, WebP 형식만 허용됩니다.'
                )
            
            # 이미지 해상도 확인 (선택사항)
            try:
                img = Image.open(image)
                width, height = img.size
                if width < 300 or height < 300:
                    raise forms.ValidationError(
                        '이미지 크기는 최소 300x300 픽셀 이상이어야 합니다.'
                    )
            except Exception as e:
                raise forms.ValidationError(f'이미지 파일 검사 실패: {str(e)}')
        
        return image
    
    def clean_title(self):
        """제목 유효성 검사"""
        title = self.cleaned_data.get('title')
        
        if title:
            if len(title.strip()) < 3:
                raise forms.ValidationError('제목은 최소 3글자 이상이어야 합니다.')
            
            if len(title) > 200:
                raise forms.ValidationError('제목은 200글자 이하여야 합니다.')
        
        return title
    
    def clean_content(self):
        """내용 유효성 검사"""
        content = self.cleaned_data.get('content')
        
        if content:
            if len(content.strip()) < 10:
                raise forms.ValidationError('내용은 최소 10글자 이상이어야 합니다.')
        
        return content


class CommentForm(forms.ModelForm):
    """댓글 작성 폼"""
    
    class Meta:
        model = Comment
        fields = ['author', 'email', 'content']
        widgets = {
            'author': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': '이름'
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': '이메일'
            }),
            'content': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': '댓글 내용'
            }),
        }
    
    def clean_content(self):
        """댓글 내용 유효성 검사"""
        content = self.cleaned_data.get('content')
        
        if content:
            if len(content.strip()) < 3:
                raise forms.ValidationError('댓글은 최소 3글자 이상이어야 합니다.')
            
            if len(content) > 1000:
                raise forms.ValidationError('댓글은 1000글자 이하여야 합니다.')
        
        return content


class ImageUploadForm(forms.Form):
    """단순 이미지 업로드 폼"""
    
    image = forms.ImageField(
        label='이미지 선택',
        help_text='최대 5MB, JPEG/PNG/GIF/WebP 형식'
    )
    
    def clean_image(self):
        """이미지 파일 유효성 검사"""
        image = self.cleaned_data.get('image')
        
        if image:
            # 파일 크기
            if image.size > 5 * 1024 * 1024:  # 5MB
                raise forms.ValidationError('파일 크기는 5MB 이하여야 합니다.')
            
            # 파일 타입
            allowed_types = ['image/jpeg', 'image/png', 'image/gif', 'image/webp']
            if image.content_type not in allowed_types:
                raise forms.ValidationError('지원하지 않는 파일 형식입니다.')
        
        return image


class FileUploadForm(forms.Form):
    """파일 업로드 폼 (PDF, 문서 등)"""
    
    file = forms.FileField(
        label='파일 선택',
        help_text='최대 10MB'
    )
    
    def clean_file(self):
        """파일 유효성 검사"""
        file = self.cleaned_data.get('file')
        
        if file:
            # 파일 크기
            if file.size > 10 * 1024 * 1024:  # 10MB
                raise forms.ValidationError('파일 크기는 10MB 이하여야 합니다.')
            
            # 파일 확장자
            allowed_extensions = ['.pdf', '.doc', '.docx', '.txt', '.xlsx']
            file_ext = os.path.splitext(file.name)[1].lower()
            
            if file_ext not in allowed_extensions:
                raise forms.ValidationError(
                    f'허용된 파일 형식: {", ".join(allowed_extensions)}'
                )
        
        return file
