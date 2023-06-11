from django.db import models

from account.models import Group, Member
from common.models import CURRENCY_CHOICES, BasicModelMixin


class Balance(models.Model):
    member = models.ForeignKey(
        Member, on_delete=models.CASCADE, related_name="balances"
    )
    balance = models.IntegerField()
    currency = models.CharField(default="TWD", max_length=10, choices=CURRENCY_CHOICES)


class Record(BasicModelMixin):
    TYPE_CHOICES = [
        ("expense", "expense"),
        ("income", "income"),
    ]

    group = models.ForeignKey(Group, on_delete=models.CASCADE)
    what = models.CharField(max_length=100)
    amount = models.FloatField()
    type = models.CharField(max_length=10, choices=TYPE_CHOICES)
    currency = models.CharField(default="TWD", max_length=10, choices=CURRENCY_CHOICES)
    exchange_rate = models.FloatField(default=1)
    note = models.TextField(default="", blank=True)
    is_equal_split = models.BooleanField(default=True)
    # images_urls


class From(models.Model):
    record = models.ForeignKey(Record, on_delete=models.CASCADE)
    member = models.OneToOneField(Member, on_delete=models.PROTECT)
    amout = models.FloatField()


class To(models.Model):
    record = models.ForeignKey(Record, on_delete=models.CASCADE)
    member = models.OneToOneField(Member, on_delete=models.PROTECT)
    amout = models.FloatField()
