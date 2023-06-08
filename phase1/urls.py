from .views import *
from django.urls import path, include

urlpatterns = [
    path('api/register', RegisterApi.as_view()),
    path('api/login', LoginAPIView.as_view(), name="login"),

    path('api/fetch_user_profile/', UserProfileAPIView.as_view(), name="fetch_user_profile"),
    path('api/fetch_all_users/', UserListAPIView.as_view(), name="fetch_all_users"),
    path('api/followers_followed_users/<int:pk>', UserFollowedAndFollowersListAPIView.as_view(), name="followers_followed_users"),
    path('api/users_followers_list/<int:pk>', UserFollowerDetailsListAPIView.as_view(), name="users_followers_list"),
    path('api/users_followed_list/<int:pk>', UserFollowerDetailsListAPIView.as_view(), name="users_followers_list")

]
