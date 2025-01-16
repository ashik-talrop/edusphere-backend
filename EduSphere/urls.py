from django.contrib import admin
from django.urls import path, include, re_path
from django.views.static import serve
from django.conf import settings
from api.v1.accounts.views import refresh_token 



urlpatterns = [
    path('admin/', admin.site.urls),
    path('api-auth/', include('rest_framework.urls')),
    path('api/token/refresh/', refresh_token, name='token_refresh'),
    path('api/v1/accounts/', include('api.v1.accounts.urls', namespace='api_v1_accounts')),
    path('api/v1/posts/', include('api.v1.posts.urls', namespace='api_v1_posts')),

    re_path(r'^media/(?P<path>.*)$', serve, {'document_root': settings.MEDIA_ROOT}),
    re_path(r'^static/(?P<path>.*)$', serve, {'document_root': settings.STATIC_FILE_ROOT}),
]
