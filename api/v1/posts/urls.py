from django.urls import path, re_path
from api.v1.posts import views

app_name = "api_v1_posts"

urlpatterns = [
    re_path(r'^list-posts/$', views.posts),
    re_path(r'^post/(?P<pk>.*)/$', views.post),
    re_path(r'^create-post/$', views.create_post),
    re_path(r'^user-post/$', views.user_post),
    re_path(r'^comments/(?P<pk>.*)/$', views.comments),
    re_path(r'^add-comments/(?P<pk>.*)/$', views.add_comment),
    re_path(r'^toggle-like/(?P<pk>.*)/$', views.toggle_like_post),
    re_path(r'^schools/$', views.schools),
    re_path(r'^users-post/(?P<pk>.*)/$', views.users_post),
    re_path(r'^toggle-saved/(?P<pk>.*)/$', views.toggle_saved),
    re_path(r'^saved-posts/$', views.saved_posts),
    re_path(r'^saved-posts-bt-users/(?P<pk>.*)/$', views.saved_posts_bt_users),

]