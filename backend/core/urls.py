from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
  path('auth/', include('drf_social_oauth2.urls', namespace='drf')),
  path('admin/', admin.site.urls),
  path('api/', include('blog_api.urls', namespace="blog_api")),
  path('api/user/', include('users.urls', namespace="users")),
  path('api-auth', include('rest_framework.urls', namespace="rest_framework")), # GUI for dev (login/logout)
  path('', include('blog.urls', namespace='blog')),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)