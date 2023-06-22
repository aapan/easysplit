from django.conf import settings
from django.contrib import admin
from django.contrib.auth.decorators import login_required
from django.urls import include, path, re_path
from django.views import static
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework.permissions import AllowAny

urlpatterns = [
    # admin
    path("admin/", admin.site.urls),
    # application
    path("", include("account.urls")),
    path("", include("record.urls")),
]


# swagger
schema_view = get_schema_view(
    openapi.Info(
        title="easysplit API",
        default_version="v1",
        description="easysplit API",
    ),
    public=True,
    permission_classes=(AllowAny,),
)

urlpatterns += [
    re_path(
        r"^static/(?P<path>.*)$",
        static.serve,
        {"document_root": settings.STATIC_ROOT},
        name="static",
    ),
    re_path(
        r"^__hiddenswagger(?P<format>\.json|\.yaml)$",
        login_required(schema_view.without_ui(cache_timeout=0)),
        name="schema-json",
    ),
    re_path(
        r"^__hiddenswagger/$",
        login_required(schema_view.with_ui("swagger", cache_timeout=0)),
        name="schema-swagger-ui",
    ),
    re_path(
        r"^redoc/$",
        login_required(schema_view.with_ui("redoc", cache_timeout=0)),
        name="schema-redoc",
    ),
    re_path(r"^accounts/", include("rest_framework.urls", namespace="rest_framework")),
]
