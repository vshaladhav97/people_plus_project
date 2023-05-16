from .views import *
from django.urls import path, include

urlpatterns = [
    path('api/register', RegisterApi.as_view()),
    path('fetch_user_profile/', UserProfileAPIView.as_view(), name="fetch_user_profile"),
    path('api/login', LoginAPIView.as_view(), name="login")

]
