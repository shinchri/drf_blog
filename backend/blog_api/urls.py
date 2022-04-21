from django.urls import path
# from .views import PostList
from .views import PostList, PostDetail, PostListDetailfilter, PostSearch
from rest_framework.routers import DefaultRouter

app_name="blog_api"

urlpatterns = [
  # path('posts/<str:pk>/', PostDetail.as_view(), name="detailcreate"),
  path('post/<str:pk>/', PostDetail.as_view(), name="detailcreate"),
  path('search/', PostListDetailfilter.as_view(), name="postsearch"),
  # path('post/<int:pk>/', PostDetail.as_view(), name="detailcreate"),
  # path('posts/', PostDetail.as_view(), name='detailcreate'),
  path('', PostList.as_view(), name="listcreate"),
]

# only uses PostList
# router = DefaultRouter()
# router.register('', PostList, basename='post')
# urlpatterns = router.urls