from django.urls import path, re_path
from api.v1.accounts import views  # Ensure views is imported

# If UserProfileSignupView is in views.py

app_name = "api_v1_accounts"

urlpatterns = [
    re_path(r'signup/', views.signup, name='user_profile_signup'),
    re_path(r'^login/$', views.login),  
    re_path(r'^logout/$', views.logout_view),  
    re_path(r'^profile-details/$', views.profile_details),  
    re_path(r'^user-details/(?P<pk>.*)/$', views.user_details),

]
