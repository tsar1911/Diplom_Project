from django.urls import path
from django.contrib.auth.views import LogoutView
from . import views

urlpatterns = [
    path('', views.home_page, name='home'),
    path('profile/', views.profile, name='profile'),
    path('posts/', views.PostListCreateView.as_view(), name='post-list'),
    path('posts/<int:pk>/', views.PostDetailView.as_view(), name='post-detail'),
    path('posts/<int:post_id>/comments/', views.CommentCreateView.as_view(), name='comment-create'),
    path('posts/<int:post_id>/like/', views.LikeToggleView.as_view(), name='like-toggle'),
    path('login/', views.CustomLoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(next_page='home'), name='logout'),
    path('create-post/', views.create_post, name='create-post'),
]
