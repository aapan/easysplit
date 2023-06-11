from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet

from record.models import Record
from record.serializers import RecordSerializer


class RecordViewSet(ModelViewSet):
    queryset = Record.objects.all()
    serializer_class = RecordSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        queryset = self.queryset
        group_id = self.request.query_params.get("group_id")
        if group_id:
            queryset = Record.objects.filter(group__id=group_id)
        return queryset
