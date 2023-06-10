from django.urls import path
from rest_framework_simplejwt.views import TokenVerifyView

from account import views

urlpatterns = [
    path("token", views.CustomTokenObtainPairView.as_view(), name="token_get"),
    path(
        "token/refresh",
        views.CustomTokenRefreshView.as_view(),
        name="token_refresh",
    ),
    path("token/verify", TokenVerifyView.as_view(), name="token_verify"),
]
