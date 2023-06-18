from django.db import models

from account.models import Group, Member
from common.models import CURRENCY_CHOICES, BasicModelMixin


class Balance(models.Model):
    """
    Model representing the balance of a member in a specific currency.
    """

    member = models.ForeignKey(
        Member, on_delete=models.CASCADE, related_name="balances"
    )
    balance = models.FloatField(default=0, blank=True)
    currency = models.CharField(default="TWD", max_length=10, choices=CURRENCY_CHOICES)


class Record(BasicModelMixin):
    """
    Model representing a financial record.
    """

    TYPE_CHOICES = [
        ("expense", "expense"),
        ("income", "income"),
        ("transfer", "transfer"),
    ]

    group = models.ForeignKey(Group, on_delete=models.CASCADE)
    what = models.CharField(max_length=100)
    amount = models.FloatField()
    type = models.CharField(max_length=10, choices=TYPE_CHOICES)
    currency = models.CharField(default="TWD", max_length=10, choices=CURRENCY_CHOICES)
    exchange_rate = models.FloatField(default=1)
    note = models.TextField(default="", blank=True)
    is_equal_split = models.BooleanField(default=True, blank=True)
    # images_urls


class From(models.Model):
    """
    Model representing the source of funds for a record.
    """

    record = models.ForeignKey(
        Record, on_delete=models.CASCADE, related_name="from_members"
    )
    member = models.ForeignKey(Member, on_delete=models.PROTECT)
    amount = models.FloatField()


class To(models.Model):
    """
    Model representing the destination of funds for a record.
    """

    record = models.ForeignKey(
        Record, on_delete=models.CASCADE, related_name="to_members"
    )
    member = models.ForeignKey(Member, on_delete=models.PROTECT)
    amount = models.FloatField()
