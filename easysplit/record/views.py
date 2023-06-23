from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet

from record.models import Record
from record.serializers import RecordSerializer


class RecordViewSet(ModelViewSet):
    """
    API endpoint for managing records.
    """

    queryset = Record.objects.all()
    serializer_class = RecordSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        queryset = self.queryset
        group_id = self.request.query_params.get("group_id")
        if group_id:
            queryset = Record.objects.filter(group__id=group_id)
        return queryset

    def perform_destroy(self, instance):
        serializer = self.get_serializer()
        serializer.delete(instance)
