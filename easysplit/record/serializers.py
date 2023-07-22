from django.db.models import FloatField, Sum, Value
from django.db.models.functions import Coalesce
from rest_framework.serializers import ModelSerializer, PrimaryKeyRelatedField

from account.models import Group, Member
from record.models import Balance, From, Record, To


class BalanceSerializer(ModelSerializer):
    """
    Serializer for the Balance model.
    """

    class Meta:
        model = Balance
        fields = ["balance", "currency"]


class FromSerializer(ModelSerializer):
    """
    Serializer for the From model.
    """

    member_id = PrimaryKeyRelatedField(queryset=Member.objects.all(), source="member")

    class Meta:
        model = From
        fields = ["member_id", "amount"]


class ToSerializer(ModelSerializer):
    """
    Serializer for the To model.
    """

    member_id = PrimaryKeyRelatedField(queryset=Member.objects.all(), source="member")

    class Meta:
        model = To
        fields = ["member_id", "amount"]


class RecordSerializer(ModelSerializer):
    """
    Serializer for the Record model, including nested serializers for the From and To models.
    """

    from_members = FromSerializer(many=True)
    to_members = ToSerializer(many=True)
    group_id = PrimaryKeyRelatedField(queryset=Group.objects.all(), source="group")

    class Meta:
        model = Record
        fields = [
            "id",
            "group_id",
            "what",
            "amount",
            "type",
            "currency",
            "exchange_rate",
            "note",
            "is_equal_split",
            "from_members",
            "to_members",
        ]

    @staticmethod
    def update_members_balance(record: Record):
        """
        Update the member's balance based on the provided record and item.

        Args:
            record (Record): The record object containing the currency information.
            item (dict): The item dictionary containing the member and amount details.
        """
        for member in record.group.members.all():
            try:
                balance = Balance.objects.get(member=member, currency=record.currency)
            except Balance.DoesNotExist:
                balance = Balance.objects.create(
                    member=member, currency=record.currency
                )
            total_expense = member.from_set.filter(
                record__currency=record.currency
            ).aggregate(
                total_amount=Coalesce(
                    Sum("amount", output_field=FloatField()),
                    Value(0, output_field=FloatField()),
                )
            )[
                "total_amount"
            ]
            total_income = member.to_set.filter(
                record__currency=record.currency
            ).aggregate(
                total_amount=Coalesce(
                    Sum("amount", output_field=FloatField()),
                    Value(0, output_field=FloatField()),
                )
            )[
                "total_amount"
            ]
            balance.balance = total_expense + total_income
            balance.save()

    def create(self, validated_data):
        """
        Create a new Record instance and related From and To instances.

        Args:
            validated_data (dict): Validated data for the Record and nested From/To instances.

        Returns:
            Record: The created Record instance.
        """
        from_data = validated_data.pop("from_members")
        to_data = validated_data.pop("to_members")
        record = Record.objects.create(**validated_data)

        for from_item in from_data:
            From.objects.create(record=record, **from_item)

        for to_item in to_data:
            To.objects.create(record=record, **to_item)

        self.update_members_balance(record)

        return record

    def update(self, instance, validated_data):
        """
        Update an existing Record instance and related From and To instances.

        Args:
            instance (Record): The existing Record instance to update.
            validated_data (dict): Validated data for the Record and nested From/To instances.

        Returns:
            Record: The updated Record instance.
        """
        from_data = validated_data.pop("from_members")
        to_data = validated_data.pop("to_members")

        instance.group = validated_data.get("group", instance.group)
        instance.what = validated_data.get("what", instance.what)
        instance.amount = validated_data.get("amount", instance.amount)
        instance.type = validated_data.get("type", instance.type)
        instance.currency = validated_data.get("currency", instance.currency)
        instance.exchange_rate = validated_data.get(
            "exchange_rate", instance.exchange_rate
        )
        instance.note = validated_data.get("note", instance.note)
        instance.is_equal_split = validated_data.get(
            "is_equal_split", instance.is_equal_split
        )
        instance.save()

        From.objects.filter(record=instance).delete()
        To.objects.filter(record=instance).delete()

        for from_item in from_data:
            From.objects.create(record=instance, **from_item)
        for to_item in to_data:
            To.objects.create(record=instance, **to_item)

        self.update_members_balance(instance)

        return instance

    def delete(self, instance):
        """
        Delete the Record instance and its related From and To instances.

        Args:
            instance (Record): The Record instance to delete.

        Returns:
            None
        """
        From.objects.filter(record=instance).delete()
        To.objects.filter(record=instance).delete()

        self.update_members_balance(instance)

        instance.delete()
