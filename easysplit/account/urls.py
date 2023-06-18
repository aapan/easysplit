from django.urls import include, path
from rest_framework.routers import SimpleRouter
from rest_framework_simplejwt.views import TokenVerifyView

from account import views

router = SimpleRouter(trailing_slash=False)
router.register("group", views.GroupViewSet, basename="group")
# router.register("member", views.MemberViewSet, basename="member")


urlpatterns = [
    path("account/token", views.CustomTokenObtainPairView.as_view(), name="token_get"),
    path(
        "account/token/refresh",
        views.CustomTokenRefreshView.as_view(),
        name="token_refresh",
    ),
    path("account/token/verify", TokenVerifyView.as_view(), name="token_verify"),
    path("", include(router.urls)),
    path("group/<uuid:group_id>/members", views.MembersView.as_view(), name="members"),
]
