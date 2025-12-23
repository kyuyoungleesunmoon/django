# Django Blog Project - Step by Step Tutorial

## Overview
This tutorial will guide you through building a complete Django blog application from scratch. Each step builds upon the previous one, allowing you to understand and implement the entire project incrementally.

**Final Result:** A fully functional blog with posts, comments, likes, bookmarks, categories, and tags.

**Estimated Time:** 4-6 hours

---

## Table of Contents

1. [Step 1: Environment Setup](#step-1-environment-setup)
2. [Step 2: Create Django Project](#step-2-create-django-project)
3. [Step 3: Create Blog App](#step-3-create-blog-app)
4. [Step 4: Design and Create Models](#step-4-design-and-create-models)
5. [Step 5: Configure Admin Panel](#step-5-configure-admin-panel)
6. [Step 6: Setup URL Routing](#step-6-setup-url-routing)
7. [Step 7: Create Views](#step-7-create-views)
8. [Step 8: Create Templates](#step-8-create-templates)
9. [Step 9: Create Forms](#step-9-create-forms)
10. [Step 10: Add Advanced Features](#step-10-add-advanced-features)
11. [Step 11: Testing and Deployment](#step-11-testing-and-deployment)

---

## Step 1: Environment Setup

### What You'll Learn
- Installing Django
- Understanding Python virtual environments
- Setting up your development environment

### Theory
Django is a high-level Python web framework that encourages rapid development. Before starting, you need to have Python installed and create a virtual environment to isolate your project dependencies.

### Implementation

**1.1 Check Python Installation**
```powershell
python --version
# Should show Python 3.8 or higher
```

**1.2 Install Django**
```powershell
pip install django==4.2.8
```

**1.3 Verify Installation**
```powershell
python -m django --version
# Should show 4.2.8
```

### Checkpoint
- [ ] Python 3.8+ installed
- [ ] Django 4.2.8 installed
- [ ] Version check successful

**Next:** Create your Django project

---

## Step 2: Create Django Project

### What You'll Learn
- Django project structure
- Difference between project and app
- Basic project configuration

### Theory
A Django **project** is a collection of settings and apps. An **app** is a module that does something specific (like a blog). One project can have multiple apps.

### Implementation

**2.1 Create Project Directory**
```powershell
mkdir DJangGo
cd DJangGo
```

**2.2 Create Django Project**
```powershell
django-admin startproject myproject .
```

**Note:** The dot (.) at the end creates the project in the current directory.

**2.3 Understand Project Structure**
```
DJangGo/
├── manage.py          # Command-line utility
└── myproject/         # Project package
    ├── __init__.py    # Python package marker
    ├── settings.py    # Project settings
    ├── urls.py        # URL declarations
    └── wsgi.py        # Web server gateway
```

**2.4 Test the Project**
```powershell
python manage.py runserver
```

Visit http://127.0.0.1:8000/ - You should see the Django welcome page!

**2.5 Stop the Server**
Press `Ctrl+C` in the terminal.

### Checkpoint
- [ ] Project created successfully
- [ ] Server runs without errors
- [ ] Welcome page displays

**Next:** Create the blog application

---

## Step 3: Create Blog App

### What You'll Learn
- Creating Django apps
- Registering apps in settings
- App structure

### Theory
Apps are modular components of a Django project. Each app should do one thing well. Our blog app will handle all blog-related functionality.

### Implementation

**3.1 Create Blog App**
```powershell
python manage.py startapp blog
```

**3.2 App Structure Created**
```
blog/
├── __init__.py
├── admin.py       # Admin configuration
├── apps.py        # App configuration
├── models.py      # Data models
├── tests.py       # Tests
├── views.py       # View functions
└── migrations/    # Database migrations
```

**3.3 Register App in Settings**

Open `myproject/settings.py` and add 'blog' to INSTALLED_APPS:

```python
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'blog',  # Add this line
]
```

**3.4 Configure Templates Directory**

In the same file, find TEMPLATES and update DIRS:

```python
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],  # Add this
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]
```

### Checkpoint
- [ ] Blog app created
- [ ] App registered in INSTALLED_APPS
- [ ] Templates directory configured

**Next:** Design your data models

---

## Step 4: Design and Create Models

### What You'll Learn
- Django ORM (Object-Relational Mapping)
- Model fields and relationships
- Database migrations

### Theory
Models define your data structure. Each model is a Python class that represents a database table. Django's ORM automatically converts your models into database tables.

**Key Concepts:**
- **Field Types:** CharField, TextField, DateTimeField, etc.
- **Relationships:** ForeignKey (many-to-one), ManyToManyField (many-to-many)
- **Meta Options:** ordering, verbose_name_plural, etc.

### Implementation

**4.1 Create Basic Models**

Open `blog/models.py` and replace everything with:

```python
from django.db import models
from django.contrib.auth.models import User


# Category Model
class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name_plural = "categories"
    
    def __str__(self):
        return self.name


# Tag Model
class Tag(models.Model):
    name = models.CharField(max_length=50, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.name


# Post Model
class Post(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='posts')
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True, related_name='posts')
    tags = models.ManyToManyField(Tag, related_name='posts', blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    published = models.BooleanField(default=True)
    views = models.IntegerField(default=0)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return self.title
```

**Understanding the Code:**

- `User` is imported from Django's auth system
- `CharField`: For short text (title, name)
- `TextField`: For long text (content, description)
- `ForeignKey`: One-to-many relationship
- `ManyToManyField`: Many-to-many relationship
- `auto_now_add=True`: Sets field to now when creating
- `auto_now=True`: Updates field on every save
- `on_delete=models.CASCADE`: Delete posts when author is deleted
- `related_name`: Reverse relationship name

**4.2 Create Migration**
```powershell
python manage.py makemigrations
```

You should see:
```
Migrations for 'blog':
  blog\migrations\0001_initial.py
    - Create model Category
    - Create model Tag
    - Create model Post
```

**4.3 Apply Migration**
```powershell
python manage.py migrate
```

This creates the database tables.

**4.4 Add More Models (Comment, Like, Bookmark)**

Add these to `blog/models.py`:

```python
# Comment Model
class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comments')
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.author.username}'s comment"


# Like Model
class Like(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='likes')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='likes')
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ('post', 'user')
    
    def __str__(self):
        return f"{self.user.username} - {self.post.title}"


# Bookmark Model
class Bookmark(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='bookmarks')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='bookmarks')
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ('post', 'user')
    
    def __str__(self):
        return f"{self.user.username} - {self.post.title}"
```

**4.5 Create and Apply New Migration**
```powershell
python manage.py makemigrations
python manage.py migrate
```

### Checkpoint
- [ ] All 6 models created
- [ ] Migrations created and applied
- [ ] No errors during migration

**Exercise:** Try to understand each field in the models. What does `unique_together` do?

**Next:** Configure the admin panel

---

## Step 5: Configure Admin Panel

### What You'll Learn
- Django admin interface
- Registering models
- Customizing admin display

### Theory
Django provides a built-in admin interface for managing your data. You need to register your models and optionally customize how they appear.

### Implementation

**5.1 Create Superuser**
```powershell
python manage.py createsuperuser
```

Enter:
- Username: `admin`
- Email: `admin@example.com` (or press Enter)
- Password: `admin123`
- Password (again): `admin123`

**5.2 Register Models in Admin**

Open `blog/admin.py` and replace with:

```python
from django.contrib import admin
from .models import Category, Tag, Post, Comment, Like, Bookmark


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'created_at']
    search_fields = ['name']


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ['name', 'created_at']
    search_fields = ['name']


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ['title', 'author', 'category', 'views', 'published', 'created_at']
    list_filter = ['published', 'category', 'created_at']
    search_fields = ['title', 'author__username', 'content']
    filter_horizontal = ['tags']
    readonly_fields = ['created_at', 'updated_at', 'views']
    
    fieldsets = (
        ('Basic Info', {
            'fields': ('title', 'author', 'category')
        }),
        ('Content', {
            'fields': ('content', 'tags')
        }),
        ('Status', {
            'fields': ('published', 'views')
        }),
        ('Dates', {
            'fields': ('created_at', 'updated_at')
        }),
    )


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ['author', 'post', 'created_at']
    list_filter = ['created_at']
    search_fields = ['author__username', 'post__title', 'content']
    readonly_fields = ['created_at', 'updated_at']


@admin.register(Like)
class LikeAdmin(admin.ModelAdmin):
    list_display = ['user', 'post', 'created_at']
    list_filter = ['created_at']
    search_fields = ['user__username', 'post__title']


@admin.register(Bookmark)
class BookmarkAdmin(admin.ModelAdmin):
    list_display = ['user', 'post', 'created_at']
    list_filter = ['created_at']
    search_fields = ['user__username', 'post__title']
```

**Understanding the Code:**

- `@admin.register()`: Decorator to register model
- `list_display`: Fields shown in list view
- `list_filter`: Adds filter sidebar
- `search_fields`: Enables search
- `filter_horizontal`: Better UI for many-to-many
- `readonly_fields`: Fields that can't be edited
- `fieldsets`: Groups fields in the form

**5.3 Test Admin Panel**

```powershell
python manage.py runserver
```

Visit http://127.0.0.1:8000/admin/

Login with:
- Username: `admin`
- Password: `admin123`

You should see all your models!

**5.4 Create Test Data**

In the admin panel:

1. **Create Categories:**
   - Click "Categories" → "Add Category"
   - Name: "Technology", Description: "Tech posts"
   - Add two more: "Tutorial", "Lifestyle"

2. **Create Tags:**
   - Click "Tags" → "Add Tag"
   - Create: "Django", "Python", "WebDev"

3. **Create a Post:**
   - Click "Posts" → "Add Post"
   - Title: "Getting Started with Django"
   - Content: "Django is a powerful web framework..."
   - Author: admin
   - Category: Technology
   - Tags: Django, Python
   - Published: ✓
   - Click "Save"

### Checkpoint
- [ ] Superuser created
- [ ] Admin panel accessible
- [ ] All models visible in admin
- [ ] Test data created

**Next:** Setup URL routing

---

## Step 6: Setup URL Routing

### What You'll Learn
- URL patterns
- URL namespacing
- Path converters

### Theory
URLs connect web addresses to view functions. Django uses a URLconf (URL configuration) to map URLs to views.

**URL Pattern Syntax:**
```python
path('route/', view_function, name='url_name')
path('post/<int:pk>/', view_function, name='detail')
```

### Implementation

**6.1 Create Blog URLs**

Create `blog/urls.py`:

```python
from django.urls import path
from . import views

app_name = 'blog'

urlpatterns = [
    # Post URLs
    path('', views.post_list, name='post_list'),
    path('post/<int:pk>/', views.post_detail, name='post_detail'),
    path('post/create/', views.PostCreateView.as_view(), name='post_create'),
    path('post/<int:pk>/edit/', views.PostUpdateView.as_view(), name='post_edit'),
    path('post/<int:pk>/delete/', views.PostDeleteView.as_view(), name='post_delete'),
    
    # Comment URL
    path('post/<int:pk>/comment/', views.add_comment, name='add_comment'),
    
    # Like & Bookmark URLs
    path('post/<int:pk>/like/', views.toggle_like, name='toggle_like'),
    path('post/<int:pk>/bookmark/', views.toggle_bookmark, name='toggle_bookmark'),
    
    # Category & Search URLs
    path('category/<int:pk>/', views.category_posts, name='category_posts'),
    path('search/', views.search, name='search'),
    
    # Dashboard URL
    path('dashboard/', views.dashboard, name='dashboard'),
]
```

**Understanding the Code:**

- `app_name = 'blog'`: Namespace for URLs
- `<int:pk>`: URL parameter (integer primary key)
- `.as_view()`: For class-based views
- `name`: Used in templates with `{% url 'blog:post_list' %}`

**6.2 Include Blog URLs in Project**

Open `myproject/urls.py` and update:

```python
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('blog.urls')),  # Add this line
]
```

### Checkpoint
- [ ] blog/urls.py created
- [ ] URLs included in project
- [ ] URL patterns defined

**Note:** Views don't exist yet, so URLs won't work. That's OK - we'll create them next!

**Next:** Create view functions

---

## Step 7: Create Views

### What You'll Learn
- Function-based views
- Class-based views
- View logic and data processing

### Theory
Views are Python functions or classes that receive web requests and return web responses. They contain the logic for your application.

**Two Types:**
1. **Function-Based Views (FBV):** Simple functions
2. **Class-Based Views (CBV):** Classes with methods

### Implementation

**7.1 Create Basic Views**

Open `blog/views.py` and replace with:

```python
from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.db.models import Q

from .models import Post, Category, Comment, Like, Bookmark
from .forms import PostForm, CommentForm


# Post List - Function-Based View
def post_list(request):
    posts = Post.objects.filter(published=True).select_related('author', 'category')
    return render(request, 'blog/post_list.html', {'posts': posts})


# Post Detail - Function-Based View
def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    post.views += 1
    post.save()
    
    comments = post.comments.all().select_related('author')
    context = {
        'post': post,
        'comments': comments,
        'is_liked': Like.objects.filter(post=post, user=request.user).exists() if request.user.is_authenticated else False,
        'is_bookmarked': Bookmark.objects.filter(post=post, user=request.user).exists() if request.user.is_authenticated else False,
    }
    return render(request, 'blog/post_detail.html', context)


# Post Create - Class-Based View
class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    form_class = PostForm
    template_name = 'blog/post_form.html'
    success_url = reverse_lazy('blog:post_list')
    
    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


# Post Update
class PostUpdateView(LoginRequiredMixin, UpdateView):
    model = Post
    form_class = PostForm
    template_name = 'blog/post_form.html'
    success_url = reverse_lazy('blog:post_list')
    
    def get_queryset(self):
        return Post.objects.filter(author=self.request.user)


# Post Delete
class PostDeleteView(LoginRequiredMixin, DeleteView):
    model = Post
    template_name = 'blog/post_confirm_delete.html'
    success_url = reverse_lazy('blog:post_list')
    
    def get_queryset(self):
        return Post.objects.filter(author=self.request.user)


# Add Comment
@login_required
def add_comment(request, pk):
    post = get_object_or_404(Post, pk=pk)
    
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.author = request.user
            comment.save()
    
    return redirect('blog:post_detail', pk=post.pk)


# Toggle Like
@login_required
def toggle_like(request, pk):
    post = get_object_or_404(Post, pk=pk)
    like, created = Like.objects.get_or_create(post=post, user=request.user)
    
    if not created:
        like.delete()
    
    return redirect('blog:post_detail', pk=post.pk)


# Toggle Bookmark
@login_required
def toggle_bookmark(request, pk):
    post = get_object_or_404(Post, pk=pk)
    bookmark, created = Bookmark.objects.get_or_create(post=post, user=request.user)
    
    if not created:
        bookmark.delete()
    
    return redirect('blog:post_detail', pk=post.pk)


# Category Posts
def category_posts(request, pk):
    category = get_object_or_404(Category, pk=pk)
    posts = category.posts.filter(published=True)
    return render(request, 'blog/post_list.html', {'posts': posts, 'category': category})


# Search
def search(request):
    query = request.GET.get('q', '')
    posts = Post.objects.filter(published=True)
    
    if query:
        posts = posts.filter(
            Q(title__icontains=query) |
            Q(content__icontains=query) |
            Q(author__username__icontains=query)
        )
    
    return render(request, 'blog/search.html', {'posts': posts, 'query': query})


# Dashboard
@login_required
def dashboard(request):
    my_posts = Post.objects.filter(author=request.user)
    my_comments = Comment.objects.filter(author=request.user)
    my_likes = Like.objects.filter(user=request.user)
    my_bookmarks = Bookmark.objects.filter(user=request.user)
    
    context = {
        'my_posts': my_posts,
        'my_comments': my_comments,
        'my_likes': my_likes,
        'my_bookmarks': my_bookmarks,
    }
    return render(request, 'blog/dashboard.html', context)
```

**Understanding the Code:**

- `get_object_or_404()`: Returns object or 404 error
- `@login_required`: Requires user to be logged in
- `LoginRequiredMixin`: Class-based version of login_required
- `select_related()`: Optimizes database queries
- `Q objects`: Complex queries with OR conditions
- `form.save(commit=False)`: Save without writing to DB yet

### Checkpoint
- [ ] All view functions created
- [ ] No syntax errors
- [ ] Imports correct

**Note:** Forms and templates don't exist yet. We'll create them next!

**Next:** Create HTML templates

---

## Step 8: Create Templates

### What You'll Learn
- Django template language
- Template inheritance
- Template tags and filters

### Theory
Templates are HTML files with Django template syntax. They display data from views and handle user input.

**Key Concepts:**
- `{{ variable }}`: Display variable
- `{% tag %}`: Template tag
- `{% extends %}`: Template inheritance
- `{% block %}`: Overridable sections

### Implementation

**8.1 Create Template Directory**

```powershell
mkdir templates
mkdir templates\blog
```

**8.2 Create Base Template**

Create `templates/blog/base.html`:

```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{% block title %}Django Blog{% endblock %}</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
    <style>
        body { font-family: 'Arial', sans-serif; background-color: #f8f9fa; }
        .navbar { background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); }
        .navbar-brand { font-weight: bold; font-size: 1.3rem; }
        .main-content { min-height: calc(100vh - 200px); padding: 2rem 0; }
        .card { transition: transform 0.3s, box-shadow 0.3s; border: none; border-radius: 10px; }
        .card:hover { transform: translateY(-3px); box-shadow: 0 5px 15px rgba(0,0,0,0.1); }
        .btn-gradient { background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); border: none; }
        .btn-gradient:hover { background: linear-gradient(135deg, #764ba2 0%, #667eea 100%); }
        .footer { background-color: #343a40; color: white; padding: 2rem 0; margin-top: 3rem; }
    </style>
</head>
<body>
    <!-- Navigation -->
    <nav class="navbar navbar-expand-lg navbar-dark sticky-top">
        <div class="container">
            <a class="navbar-brand" href="{% url 'blog:post_list' %}">Blog</a>
            <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarNav">
                <span class="navbar-toggler-icon"></span>
            </button>
            <div class="collapse navbar-collapse" id="navbarNav">
                <ul class="navbar-nav ms-auto">
                    <li class="nav-item"><a class="nav-link" href="{% url 'blog:post_list' %}">Home</a></li>
                    <li class="nav-item"><a class="nav-link" href="{% url 'blog:search' %}">Search</a></li>
                    {% if user.is_authenticated %}
                        <li class="nav-item"><a class="nav-link" href="{% url 'blog:post_create' %}">Write</a></li>
                        <li class="nav-item"><a class="nav-link" href="{% url 'blog:dashboard' %}">Dashboard</a></li>
                        <li class="nav-item"><a class="nav-link" href="{% url 'admin:logout' %}">Logout</a></li>
                    {% else %}
                        <li class="nav-item"><a class="nav-link" href="{% url 'admin:login' %}">Login</a></li>
                    {% endif %}
                </ul>
            </div>
        </div>
    </nav>

    <!-- Messages -->
    {% if messages %}
        <div class="container mt-3">
            {% for message in messages %}
                <div class="alert alert-{{ message.tags }} alert-dismissible fade show" role="alert">
                    {{ message }}
                    <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
                </div>
            {% endfor %}
        </div>
    {% endif %}

    <!-- Main Content -->
    <div class="main-content">
        <div class="container">
            {% block content %}{% endblock %}
        </div>
    </div>

    <!-- Footer -->
    <footer class="footer text-center">
        <p>&copy; 2024 Django Blog Tutorial</p>
    </footer>

    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/js/bootstrap.bundle.min.js"></script>
</body>
</html>
```

**8.3 Create Post List Template**

Create `templates/blog/post_list.html`:

```html
{% extends 'blog/base.html' %}

{% block title %}Post List - Blog{% endblock %}

{% block content %}
<h1 class="mb-4">All Posts</h1>

{% if posts %}
    <div class="row">
        {% for post in posts %}
            <div class="col-md-8 mb-4">
                <div class="card">
                    <div class="card-body">
                        <h5 class="card-title">{{ post.title }}</h5>
                        <p class="card-text text-muted">
                            <small>Author: {{ post.author.username }} | Date: {{ post.created_at|date:"Y-m-d" }} | Views: {{ post.views }}</small>
                        </p>
                        {% if post.category %}
                            <span class="badge bg-info">{{ post.category.name }}</span>
                        {% endif %}
                        <p class="card-text mt-2">{{ post.content|truncatewords:50 }}</p>
                        <a href="{% url 'blog:post_detail' post.pk %}" class="btn btn-sm btn-primary">Read More</a>
                        {% if user == post.author %}
                            <a href="{% url 'blog:post_edit' post.pk %}" class="btn btn-sm btn-warning">Edit</a>
                            <a href="{% url 'blog:post_delete' post.pk %}" class="btn btn-sm btn-danger">Delete</a>
                        {% endif %}
                    </div>
                </div>
            </div>
        {% endfor %}
    </div>
{% else %}
    <div class="alert alert-info">No posts yet.</div>
{% endif %}

{% if user.is_authenticated %}
    <div class="mt-4">
        <a href="{% url 'blog:post_create' %}" class="btn btn-gradient">Write New Post</a>
    </div>
{% endif %}
{% endblock %}
```

**8.4 Create Post Detail Template**

Create `templates/blog/post_detail.html`:

```html
{% extends 'blog/base.html' %}

{% block title %}{{ post.title }} - Blog{% endblock %}

{% block content %}
<div class="row">
    <div class="col-md-8">
        <h1>{{ post.title }}</h1>
        <p class="text-muted">
            <small>Author: {{ post.author.username }} | Date: {{ post.created_at|date:"Y-m-d H:i" }} | Views: {{ post.views }}</small>
        </p>

        {% if post.category %}
            <p><span class="badge bg-info">{{ post.category.name }}</span></p>
        {% endif %}

        <div class="border-top border-bottom py-3 my-4">
            {{ post.content }}
        </div>

        {% if post.tags.all %}
            <p>
                {% for tag in post.tags.all %}
                    <span class="badge bg-secondary">{{ tag.name }}</span>
                {% endfor %}
            </p>
        {% endif %}

        <!-- Like & Bookmark -->
        {% if user.is_authenticated %}
            <div class="my-3">
                <a href="{% url 'blog:toggle_like' post.pk %}" class="btn btn-sm {% if is_liked %}btn-danger{% else %}btn-outline-danger{% endif %}">
                    Like ({{ post.likes.count }})
                </a>
                <a href="{% url 'blog:toggle_bookmark' post.pk %}" class="btn btn-sm {% if is_bookmarked %}btn-warning{% else %}btn-outline-warning{% endif %}">
                    Bookmark ({{ post.bookmarks.count }})
                </a>
            </div>
        {% endif %}

        <!-- Edit/Delete -->
        {% if user == post.author %}
            <div class="my-3">
                <a href="{% url 'blog:post_edit' post.pk %}" class="btn btn-warning">Edit</a>
                <a href="{% url 'blog:post_delete' post.pk %}" class="btn btn-danger">Delete</a>
            </div>
        {% endif %}

        <hr class="my-4">

        <!-- Comments -->
        <h3>Comments ({{ post.comments.count }})</h3>

        {% if user.is_authenticated %}
            <form method="post" action="{% url 'blog:add_comment' post.pk %}" class="mb-4">
                {% csrf_token %}
                <textarea name="content" class="form-control" placeholder="Write a comment" rows="3" required></textarea>
                <button type="submit" class="btn btn-primary mt-2">Post Comment</button>
            </form>
        {% else %}
            <p class="alert alert-info">Please <a href="{% url 'admin:login' %}">login</a> to comment.</p>
        {% endif %}

        {% for comment in comments %}
            <div class="card mb-3">
                <div class="card-body">
                    <p class="card-text"><strong>{{ comment.author.username }}</strong></p>
                    <p class="card-text">{{ comment.content }}</p>
                    <small class="text-muted">{{ comment.created_at|date:"Y-m-d H:i" }}</small>
                </div>
            </div>
        {% empty %}
            <p class="text-muted">No comments yet.</p>
        {% endfor %}
    </div>

    <!-- Sidebar -->
    <div class="col-md-4">
        <div class="card mb-4">
            <div class="card-body">
                <h5>Post Info</h5>
                <ul class="list-unstyled">
                    <li>Author: {{ post.author.username }}</li>
                    <li>Date: {{ post.created_at|date:"Y-m-d" }}</li>
                    <li>Views: {{ post.views }}</li>
                    <li>Likes: {{ post.likes.count }}</li>
                </ul>
            </div>
        </div>
    </div>
</div>
{% endblock %}
```

**8.5 Create Other Required Templates**

Create `templates/blog/post_form.html`:

```html
{% extends 'blog/base.html' %}

{% block title %}Post Form{% endblock %}

{% block content %}
<h1 class="mb-4">{% if form.instance.pk %}Edit Post{% else %}Write New Post{% endif %}</h1>

<div class="row">
    <div class="col-md-8">
        <form method="post" class="card p-4">
            {% csrf_token %}
            {{ form.as_p }}
            <div class="mt-3">
                <button type="submit" class="btn btn-primary">{{ form.instance.pk|yesno:"Update,Save" }}</button>
                <a href="{% url 'blog:post_list' %}" class="btn btn-secondary">Cancel</a>
            </div>
        </form>
    </div>
</div>
{% endblock %}
```

Create `templates/blog/post_confirm_delete.html`:

```html
{% extends 'blog/base.html' %}

{% block title %}Delete Confirmation{% endblock %}

{% block content %}
<div class="row">
    <div class="col-md-6">
        <div class="card border-danger">
            <div class="card-body">
                <h5 class="card-title text-danger">Delete Post Warning</h5>
                <p class="card-text">Are you sure you want to delete "<strong>{{ object.title }}</strong>"?</p>
                <p class="text-muted small">This action cannot be undone.</p>
                <form method="post">
                    {% csrf_token %}
                    <button type="submit" class="btn btn-danger">Delete</button>
                    <a href="{% url 'blog:post_detail' object.pk %}" class="btn btn-secondary">Cancel</a>
                </form>
            </div>
        </div>
    </div>
</div>
{% endblock %}
```

Create `templates/blog/search.html`:

```html
{% extends 'blog/base.html' %}

{% block title %}Search{% endblock %}

{% block content %}
<h1>Search Posts</h1>

<form method="get" class="card p-4 mb-4">
    <div class="row">
        <div class="col-md-6 mb-3">
            <input type="text" name="q" class="form-control" placeholder="Search..." value="{{ query }}">
        </div>
        <div class="col-md-6 mb-3">
            <button type="submit" class="btn btn-primary w-100">Search</button>
        </div>
    </div>
</form>

{% if posts %}
    <h3>Search Results ({{ posts|length }})</h3>
    <div class="row">
        {% for post in posts %}
            <div class="col-md-8 mb-4">
                <div class="card">
                    <div class="card-body">
                        <h5 class="card-title">{{ post.title }}</h5>
                        <p class="card-text text-muted"><small>Author: {{ post.author.username }} | Date: {{ post.created_at|date:"Y-m-d" }}</small></p>
                        <p class="card-text">{{ post.content|truncatewords:50 }}</p>
                        <a href="{% url 'blog:post_detail' post.pk %}" class="btn btn-sm btn-primary">Details</a>
                    </div>
                </div>
            </div>
        {% endfor %}
    </div>
{% elif query %}
    <p class="alert alert-info">No results found.</p>
{% else %}
    <p class="alert alert-secondary">Enter a search term.</p>
{% endif %}
{% endblock %}
```

Create `templates/blog/dashboard.html`:

```html
{% extends 'blog/base.html' %}

{% block title %}Dashboard{% endblock %}

{% block content %}
<h1>My Dashboard</h1>

<div class="row mb-4">
    <div class="col-md-3">
        <div class="card text-center">
            <div class="card-body">
                <h5>My Posts</h5>
                <p class="h3">{{ my_posts.count }}</p>
            </div>
        </div>
    </div>
    <div class="col-md-3">
        <div class="card text-center">
            <div class="card-body">
                <h5>My Comments</h5>
                <p class="h3">{{ my_comments.count }}</p>
            </div>
        </div>
    </div>
    <div class="col-md-3">
        <div class="card text-center">
            <div class="card-body">
                <h5>Likes</h5>
                <p class="h3">{{ my_likes.count }}</p>
            </div>
        </div>
    </div>
    <div class="col-md-3">
        <div class="card text-center">
            <div class="card-body">
                <h5>Bookmarks</h5>
                <p class="h3">{{ my_bookmarks.count }}</p>
            </div>
        </div>
    </div>
</div>

<h3 class="mt-5">My Posts</h3>
{% if my_posts %}
    <table class="table">
        <thead>
            <tr>
                <th>Title</th>
                <th>Date</th>
                <th>Views</th>
                <th>Actions</th>
            </tr>
        </thead>
        <tbody>
            {% for post in my_posts %}
                <tr>
                    <td><a href="{% url 'blog:post_detail' post.pk %}">{{ post.title }}</a></td>
                    <td>{{ post.created_at|date:"Y-m-d" }}</td>
                    <td>{{ post.views }}</td>
                    <td>
                        <a href="{% url 'blog:post_edit' post.pk %}" class="btn btn-sm btn-warning">Edit</a>
                        <a href="{% url 'blog:post_delete' post.pk %}" class="btn btn-sm btn-danger">Delete</a>
                    </td>
                </tr>
            {% endfor %}
        </tbody>
    </table>
{% else %}
    <p class="alert alert-info">No posts yet. <a href="{% url 'blog:post_create' %}">Write one</a></p>
{% endif %}
{% endblock %}
```

### Checkpoint
- [ ] All 7 templates created
- [ ] Templates use inheritance
- [ ] Bootstrap styling applied

**Next:** Create forms

---

## Step 9: Create Forms

### What You'll Learn
- Django forms
- ModelForm
- Form validation

### Theory
Forms handle user input. Django provides Form and ModelForm classes to easily create and validate forms.

### Implementation

**9.1 Create Forms**

Create `blog/forms.py`:

```python
from django import forms
from .models import Post, Comment


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'content', 'category', 'tags', 'published']
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter post title'
            }),
            'content': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Write your post content',
                'rows': 10
            }),
            'category': forms.Select(attrs={
                'class': 'form-control'
            }),
            'tags': forms.CheckboxSelectMultiple(),
            'published': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            }),
        }


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']
        widgets = {
            'content': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Write a comment',
                'rows': 3
            }),
        }
```

**Understanding the Code:**

- `ModelForm`: Automatically creates form from model
- `fields`: Which model fields to include
- `widgets`: Customize HTML input elements
- `attrs`: HTML attributes (class, placeholder, etc.)

### Checkpoint
- [ ] Forms created
- [ ] No syntax errors

**Next:** Test the complete application

---

## Step 10: Testing and Final Touches

### What You'll Learn
- Running the complete application
- Creating test data
- Testing all features

### Implementation

**10.1 Run Server**

```powershell
python manage.py runserver
```

**10.2 Test Each Feature**

1. **Homepage:** http://127.0.0.1:8000/
   - Should show empty or existing posts

2. **Admin Panel:** http://127.0.0.1:8000/admin/
   - Login with admin/admin123
   - Add more posts, categories, tags

3. **Create Post:** http://127.0.0.1:8000/post/create/
   - Test post creation

4. **Post Detail:** Click on any post
   - Test comments
   - Test likes
   - Test bookmarks

5. **Search:** http://127.0.0.1:8000/search/
   - Search for posts

6. **Dashboard:** http://127.0.0.1:8000/dashboard/
   - View your statistics

### Checkpoint
- [ ] Server runs without errors
- [ ] All pages load correctly
- [ ] Can create posts
- [ ] Can add comments
- [ ] Can like/bookmark posts
- [ ] Search works
- [ ] Dashboard shows data

---

## Congratulations!

You've built a complete Django blog application from scratch! 

### What You've Learned

1. Django project structure
2. Models and database design
3. Admin panel customization
4. URL routing
5. Function-based and class-based views
6. Template language and inheritance
7. Forms and validation
8. User authentication
9. Database relationships
10. Query optimization

### Next Steps

**Enhance Your Blog:**
1. Add user registration
2. Add pagination
3. Add rich text editor
4. Add image upload
5. Add REST API
6. Deploy to production

### Resources

- Django Documentation: https://docs.djangoproject.com/
- Django Girls Tutorial: https://tutorial.djangogirls.org/
- Real Python Django: https://realpython.com/tutorials/django/

---

## Troubleshooting

### Common Issues

**1. Migration Errors**
```powershell
# Reset migrations
python manage.py migrate --run-syncdb
```

**2. Port Already in Use**
```powershell
# Use different port
python manage.py runserver 8080
```

**3. Template Not Found**
- Check TEMPLATES DIRS in settings.py
- Verify template file names
- Check template folder structure

**4. Static Files Not Loading**
```powershell
# Collect static files
python manage.py collectstatic
```

---

## Summary

This tutorial covered:
- ✅ Complete Django blog setup
- ✅ 6 models with relationships
- ✅ Admin panel configuration
- ✅ 12 views (function and class-based)
- ✅ 7 templates with Bootstrap
- ✅ 2 forms
- ✅ Full CRUD operations
- ✅ User authentication
- ✅ Comments, likes, bookmarks

**Total Lines of Code:** ~800
**Time Invested:** 4-6 hours
**Skill Level Achieved:** Intermediate Django Developer

Keep coding and happy learning!
