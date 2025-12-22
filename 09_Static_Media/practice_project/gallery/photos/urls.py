from django.urls import path
from . import views

app_name = 'photos'

urlpatterns = [
    path('', views.AlbumListView.as_view(), name='album_list'),
    path('album/<int:pk>/', views.AlbumDetailView.as_view(), name='album_detail'),
    path('photo/<int:pk>/', views.PhotoDetailView.as_view(), name='photo_detail'),
]
