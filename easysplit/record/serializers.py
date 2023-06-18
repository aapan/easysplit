from django.db.models import FloatField, Sum, Value
from django.db.models.functions import Coalesce
from rest_framework.serializers import ModelSerializer

from record.models import Balance, From, Record, To


class BalanceSerializer(ModelSerializer):
    """
    Serializer for the Balance model.
    """

    class Meta:
        model = Balance
        fields = ["member", "balance", "currency"]


class FromSerializer(ModelSerializer):
    """
    Serializer for the From model.
    """

    class Meta:
        model = From
        fields = ["member", "amount"]


class ToSerializer(ModelSerializer):
    """
    Serializer for the To model.
    """

    class Meta:
        model = To
        fields = ["member", "amount"]


class RecordSerializer(ModelSerializer):
    """
    Serializer for the Record model, including nested serializers for the From and To models.
    """

    from_members = FromSerializer(many=True)
    to_members = ToSerializer(many=True)

    class Meta:
        model = Record
        fields = [
            "id",
            "group",
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
            balance.balance = balance.balance + total_expense + total_income
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

        # Update or create 'From' objects
        existing_from_ids = []
        for from_item in from_data:
            from_id = from_item.get("id")
            if from_id:
                existing_from_ids.append(from_id)
                from_instance = From.objects.get(id=from_id, record=instance)
                from_instance.member = from_item.get("member", from_instance.member)
                from_instance.amount = from_item.get("amount", from_instance.amount)
                from_instance.save()
            else:
                From.objects.create(record=instance, **from_item)

        # Delete removed 'From' objects
        From.objects.filter(record=instance).exclude(id__in=existing_from_ids).delete()

        # Update or create 'To' objects
        existing_to_ids = []
        for to_item in to_data:
            to_id = to_item.get("id")
            if to_id:
                existing_to_ids.append(to_id)
                to_instance = To.objects.get(id=to_id, record=instance)
                to_instance.member = to_item.get("member", to_instance.member)
                to_instance.amount = to_item.get("amount", to_instance.amount)
                to_instance.save()
            else:
                To.objects.create(record=instance, **to_item)

        # Delete removed 'To' objects
        To.objects.filter(record=instance).exclude(id__in=existing_to_ids).delete()

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
        # Delete 'From' objects
        From.objects.filter(record=instance).delete()

        # Delete 'To' objects
        To.objects.filter(record=instance).delete()

        # Delete 'Record' object
        instance.delete()
