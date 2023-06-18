from django.contrib.auth.models import User
from django.db import models

from common.models import CURRENCY_CHOICES, BasicModelMixin


class Group(BasicModelMixin):
    """
    Model representing a group.
    """
    
    PUBLIC_PERMISSION_CHOICES = [
        ("limited", "limited"),
        ("public", "public"),
        ("private", "private"),
    ]

    owner = models.ForeignKey(User, on_delete=models.PROTECT)
    name = models.CharField(max_length=50)
    note = models.TextField(default="", blank=True)
    public_permission = models.CharField(
        max_length=20, choices=PUBLIC_PERMISSION_CHOICES
    )
    primary_currency = models.CharField(
        default="TWD", max_length=10, choices=CURRENCY_CHOICES
    )
    # image = models.ImageField()


class Member(BasicModelMixin):
    """
    Model representing a member of a group.
    """

    PERMISSION_CHOICES = [
        ("edit", "edit"),
        ("view", "view"),
        ("deactivated", "deactivated"),
    ]

    user = models.ForeignKey(User, on_delete=models.PROTECT, blank=True, null=True)
    group = models.ForeignKey(Group, on_delete=models.CASCADE, related_name="members")
    name = models.CharField(max_length=50)
    permission = models.CharField(max_length=20, choices=PERMISSION_CHOICES)
    # primary_balance
