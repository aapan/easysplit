from rest_framework.serializers import HiddenField, ModelSerializer

from record.models import Balance, From, Record, To


class BalanceSerializer(ModelSerializer):
    class Meta:
        model = Balance
        fields = "__all__"


class FromSerializer(ModelSerializer):
    # id = HiddenField()

    class Meta:
        model = From
        fields = "__all__"


class ToSerializer(ModelSerializer):
    # id = HiddenField()

    class Meta:
        model = To
        fields = "__all__"


class RecordSerializer(ModelSerializer):
    from_ = FromSerializer(source="from", read_only=False, many=True)
    to = ToSerializer(read_only=False, many=True)

    class Meta:
        model = Record
        fields = "__all__"
