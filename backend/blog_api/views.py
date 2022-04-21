from rest_framework import generics
from blog.models import Post
from .serializers import PostSerializer
from rest_framework.permissions import SAFE_METHODS, BasePermission, IsAdminUser, DjangoModelPermissionsOrAnonReadOnly, IsAuthenticatedOrReadOnly

class PostUserWritePermission(BasePermission):
  message = "Editing posts is restricted to the author only."

  def has_object_permission(self, request, view, obj):
    
    if request.method in SAFE_METHODS:
      return True

    return obj.author == request.user

# Create your views here.
class PostList(generics.ListCreateAPIView):
  queryset = Post.postobjects.all()
  serializer_class = PostSerializer
  permission_classes = [IsAuthenticatedOrReadOnly,]

class PostDetail(generics.RetrieveUpdateDestroyAPIView, PostUserWritePermission):
  queryset = Post.postobjects.all()
  serializer_class = PostSerializer
  permission_classes = [PostUserWritePermission,]