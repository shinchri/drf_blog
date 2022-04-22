from rest_framework import generics
from blog.models import Post
from .serializers import PostSerializer
from rest_framework.permissions import SAFE_METHODS, BasePermission,  IsAuthenticatedOrReadOnly, IsAuthenticated
from django.shortcuts import get_object_or_404
from rest_framework import filters

class PostUserWritePermission(BasePermission):
  message = "Editing posts is restricted to the author only."

  def has_object_permission(self, request, view, obj):
    
    if request.method in SAFE_METHODS:
      return True

    return obj.author == request.user

# Create your views here.
class PostList(generics.ListCreateAPIView):
  serializer_class = PostSerializer
  permission_classes = [IsAuthenticatedOrReadOnly,]

  def get_queryset(self):
    user = self.request.user
    return Post.objects.all()

class PostDetail(generics.RetrieveUpdateDestroyAPIView, PostUserWritePermission):
  # queryset = Post.postobjects.all()
  serializer_class = PostSerializer
  permission_classes = [IsAuthenticated,PostUserWritePermission,]

  def get_object(self, queryset=None, **kwargs):
    item = self.kwargs.get('pk')
    print(item)
    return get_object_or_404(Post, slug=item)

# Post Search
class PostListDetailfilter(generics.ListAPIView):
  queryset = Post.objects.all()
  serializer_class = PostSerializer
  filter_backends = [filters.SearchFilter]
  search_fields = ['^slug']

  # '^' Starts-with search. (focus in this project)
  # '=' Exact matches. (focus in this project)
  # '@' Full-text search. (Currently only supported Django's PostgreSQL backend.)
  # '$' Regex search.
        
# Post Admin
class CreatePost(generics.CreateAPIView):
  permission_classes = [IsAuthenticated]
  queryset = Post.objects.all()
  serializer_class = PostSerializer

class AdminPostDetail(generics.RetrieveAPIView):
  permission_classes = [IsAuthenticated]
  queryset = Post.objects.all()
  serializer_class = PostSerializer

class EditPost(generics.UpdateAPIView):
  permission_classes = [IsAuthenticated]
  queryset = Post.objects.all()
  serializer_class = PostSerializer

class DeletePost(generics.RetrieveDestroyAPIView):
  permission_classes = [IsAuthenticated]
  queryset = Post.objects.all()
  serializer_class = PostSerializer