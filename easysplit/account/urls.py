from django.urls import include, path
from rest_framework.routers import SimpleRouter

from account import views

router = SimpleRouter(trailing_slash=False)
router.register("group", views.GroupViewSet, basename="group")


urlpatterns = [
    path("account/token", views.CustomTokenObtainPairView.as_view(), name="token_get"),
    path(
        "account/token/refresh",
        views.CustomTokenRefreshView.as_view(),
        name="token_refresh",
    ),
    path(
        "account/token/verify",
        views.CustomTokenVerifyView.as_view(),
        name="token_verify",
    ),
    path(
        "account/google/token",
        views.CustomGoogleLoginView.as_view(),
        name="google_token",
    ),
    path("account/user", views.UserView.as_view(), name="user_data"),
    path("", include(router.urls)),
    path("group/<uuid:group_id>/members", views.MembersView.as_view(), name="members"),
]
