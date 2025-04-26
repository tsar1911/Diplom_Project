from rest_framework import generics, permissions
from .models import Post, Comment, Like
from .serializers import PostSerializer, CommentSerializer
from django.shortcuts import get_object_or_404
from django.core.exceptions import PermissionDenied
from django.http import HttpResponse
from django.shortcuts import render
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from .forms import PostForm


class PostListCreateView(generics.ListCreateAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class PostDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get_object(self):
        obj = get_object_or_404(Post, pk=self.kwargs['pk'])
        if self.request.method in ['PUT', 'DELETE'] and obj.author != self.request.user:
            raise PermissionDenied("You are not the author of this post")
        return obj


class CommentCreateView(generics.CreateAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        post = get_object_or_404(Post, pk=self.kwargs['post_id'])
        serializer.save(author=self.request.user, post=post)

    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)
        messages.success(request, 'Комментарий добавлен!')
        return redirect('home')

class LikeToggleView(generics.CreateAPIView):
    queryset = Like.objects.all()
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        post = get_object_or_404(Post, pk=self.kwargs['post_id'])
        like, created = Like.objects.get_or_create(
            user=self.request.user,
            post=post
        )
        if not created:
            like.delete()

    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)
        messages.success(request, 'Лайк обновлён!')
        return redirect('home')

def home_page(request):
    posts = Post.objects.all().order_by('-created_at')[:10]
    return render(request, 'core/home.html', {
        'posts': posts,
        'new_feature': True
    })

class CustomLoginView(LoginView):
    template_name = 'core/login.html'
    redirect_authenticated_user = True

@login_required
def create_post(request):
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return redirect('home')
    else:
        form = PostForm()
    return render(request, 'core/create_post.html', {'form': form})
def profile(request):
    return render(request, 'core/profile.html', {
        'user': request.user,
        'posts': request.user.posts.all()  # Пример данных
    })