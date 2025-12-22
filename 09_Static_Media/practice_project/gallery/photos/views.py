from django.views.generic import ListView, DetailView
from .models import Album, Photo

class AlbumListView(ListView):
    model = Album
    template_name = 'photos/album_list.html'
    context_object_name = 'albums'

class AlbumDetailView(DetailView):
    model = Album
    template_name = 'photos/album_detail.html'
    context_object_name = 'album'

class PhotoDetailView(DetailView):
    model = Photo
    template_name = 'photos/photo_detail.html'
    context_object_name = 'photo'
