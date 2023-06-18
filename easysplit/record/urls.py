from django.urls import include, path
from rest_framework.routers import SimpleRouter

from record import views

router = SimpleRouter(trailing_slash=False)
router.register("record", views.RecordViewSet, basename="record")


urlpatterns = [
    path("group/<uuid:group_id>/", include(router.urls)),
]
