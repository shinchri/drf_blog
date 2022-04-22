from rest_framework import generics, viewsets
from blog.models import Post
from .serializers import PostSerializer
from rest_framework.permissions import SAFE_METHODS, BasePermission, AllowAny, IsAdminUser, DjangoModelPermissionsOrAnonReadOnly, IsAuthenticatedOrReadOnly, IsAuthenticated
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from rest_framework import filters

class PostUserWritePermission(BasePermission):
  message = "Editing posts is restricted to the author only."

  def has_object_permission(self, request, view, obj):
    
    if request.method in SAFE_METHODS:
      return True

    return obj.author == request.user

# class PostList(viewsets.ModelViewSet):
#   permission_classes = [IsAuthenticated]
#   serializer_class = PostSerializer
#   # queryset = Post.postobjects.all()

#   def get_object(self, queryset=None, **kwargs):
#     item = self.kwargs.get("pk")
#     return get_object_or_404(Post, slug=item)

#   def get_queryset(self):
#     return Post.objects.all()



# class PostList(viewsets.ViewSet):
#   permission_classes = [IsAuthenticated]
#   queryset = Post.postobjects.all()

#   def list(self, request):
#     serializer_class = PostSerializer(self.queryset, many=True)
#     return Response(serializer_class.data)
  
#   def retrieve(self, request, pk=None):
#     post = get_object_or_404(self.queryset, pk=pk)
#     serializer_class = PostSerializer(post)
#     return Response(serializer_class.data)

  # def list(self, request):
  #   pass
  # def create(self, request):
  #   pass
  # def retrieve(self, request, pk=None):
  #   pass
  # def update(self, request, pk=None):
  #   pass
  # def partial_update(self, request, pk=None):
  #   pass
  # def destroy(self, request, pk=None):
  #   pass

# Create your views here.
class PostList(generics.ListCreateAPIView):
  # queryset = Post.postobjects.all()
  serializer_class = PostSerializer
  permission_classes = [IsAuthenticatedOrReadOnly,]

  def get_queryset(self):
    user = self.request.user
    return Post.objects.all()
    # if not user.is_authenticated:
    #   return Post.objects.all()
    # return Post.objects.filter(author=user)

# class PostDetail(generics.ListAPIView):
#     serializer_class = PostSerializer

#     def get_queryset(self):
#       slug = self.request.query_params.get('slug', None)
#       return Post.objects.filter(slug=slug)


class PostListDetailfilter(generics.ListAPIView):
  queryset = Post.objects.all()
  serializer_class = PostSerializer
  filter_backends = [filters.SearchFilter]
  search_fields = ['^slug']

  # '^' Starts-with search. (focus in this project)
  # '=' Exact matches. (focus in this project)
  # '@' Full-text search. (Currently only supported Django's PostgreSQL backend.)
  # '$' Regex search.

class PostSearch(generics.ListAPIView):
  permission_classes = [AllowAny]
  queryset = Post.objects.all()
  serializer_class = PostSerializer
  filter_backends = [filters.SearchFilter]
  search_fields = ['^slug']

  # def get_object(self, queryset=None, **kwargs):
  #     item = self.kwargs.get('pk')
  #     return get_object_or_404(Post, slug=item)

  #Define Custom Queryset
  # def get_queryset(self):
  #     slug = self.request.query_params.get('slug', None)
  #     return Post.objects.filter(slug=slug)


# for some reason the slug cannot be used to filter (problem with slug not being unique?)
# class PostDetail(generics.RetrieveAPIView):
#     serializer_class = PostSerializer

#     def get_queryset(self):
#         slug=self.kwargs['pk']
#         print(slug)
#         return Post.objects.filter(id=slug)
        
class PostDetail(generics.RetrieveUpdateDestroyAPIView, PostUserWritePermission):
  # queryset = Post.postobjects.all()
  serializer_class = PostSerializer
  permission_classes = [PostUserWritePermission,]

  def get_object(self, queryset=None, **kwargs):
    item = self.kwargs.get('pk')
    print(item)
    return get_object_or_404(Post, slug=item)
