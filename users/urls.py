from django.urls import path
from .views import UserCreateView, UserUpdateView, UserDeleteView, UserRetrieveView
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)


app_name = "users"

urlpatterns = [
    path("login/", TokenObtainPairView.as_view(permission_classes=[AllowAny]), name="login"),
    path("token/refresh/", TokenRefreshView.as_view(permission_classes=[AllowAny]), name="token_refresh"),

    path("create/", UserCreateView.as_view(), name="user_create"),
    path("<int:pk>/update/", UserUpdateView.as_view(), name="user_update"),
    path("<int:pk>/delete/", UserDeleteView.as_view(), name="user_delete"),
    path("<int:pk>/retrieve/", UserRetrieveView.as_view(), name="user_retrieve"),
]
