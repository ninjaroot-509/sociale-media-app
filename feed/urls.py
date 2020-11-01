from django.contrib import admin
from django.urls import path, include
from .views import *

urlpatterns=[
    path('', home, name='home'),
	path('Gallery/', ArtListView.as_view(), name='gallery'),
    path('category/<slug>/', CategoryView.as_view(), name='category'),
	path('art/new/', create_art, name='art-create'),
	path('art/<int:pk>/', art_detail, name='art-detail'),
	path('like/', like, name='art-like'),
	path('art/<int:pk>/update/', ArtUpdateView.as_view(), name='art-update'),
	path('art/<int:pk>/delete/', ArtDeleteView.as_view(), name='art-delete'),
	path('search_arts/', search_arts, name='search_arts'),
	path('user_arts/<str:username>', UserArtListView.as_view(), name='user-arts'),
	path('post/<int:pk>/', post_detail, name='post-detail'),
]