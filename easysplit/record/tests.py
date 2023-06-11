from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from account.models import Group, Member


def create_test_user(username, password):
    user = User.objects.create(username=username)
    user.set_password(password)
    user.save()
    return user


class BasicTests(APITestCase):
    @classmethod
    def setUpTestData(cls):
        create_test_user(username="admin", password="admin")

    def setUp(self):
        self.client.login(username="admin", password="admin")

    @staticmethod
    def create_group():
        return Group.objects.create(
            owner_id=1,
            name="Group1",
            note="",
            public_permission="limited",
            primary_currency="TWD",
        )

    @staticmethod
    def create_members(group):
        user1 = create_test_user(username="user1", password="user1")
        owner_member = Member.objects.create(
            user=group.owner,
            group=group,
            name="Aaron",
            permission="edit",
        )
        binded_member = Member.objects.create(
            user=user1,
            group=group,
            name="Binded member",
            permission="edit",
        )
        non_binded_member = Member.objects.create(
            user=None,
            group=group,
            name="Non-binded member",
            permission="edit",
        )
        return owner_member, binded_member, non_binded_member

    def test_create_record(self):
        group = self.create_group()
        owner_member, binded_member, non_binded_member = self.create_members(group)

        record_data = {
            "what": "Item1",
            "amount": 600,
            "type": "expense",
            "currency": "TWD",
            "exchange_rate": 1,
            "note": "",
            "is_equal_split": True,
            "from": [{"amount": 600, "member_id": owner_member.id}],
            "to": [
                {"amount": -200, "member_id": owner_member.id},
                {"amount": -200, "member_id": binded_member.id},
                {"amount": -200, "member_id": non_binded_member.id},
            ],
        }
        response = self.client.post(
            reverse("record-list", kwargs={"group_id": group.id}), data=record_data
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_get_record(self):
        group = self.create_group()
        response = self.client.get(
            reverse("record-list", kwargs={"group_id": group.id})
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
