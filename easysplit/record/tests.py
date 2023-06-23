from typing import List

from django.urls import reverse
from pydantic import BaseModel, ValidationError
from rest_framework import status

from common.tests import BaseTestCase, incorrect_format_message
from record.models import Balance, From, Record, To


class ItemDataModel(BaseModel):
    """
    Represents the data model for from and to data.
    """

    member: str
    amount: float


class RecordDataModel(BaseModel):
    """
    Represents the data model for record data.
    """

    id: str
    group: str
    what: str
    amount: float
    type: str
    currency: str
    exchange_rate: int
    note: str
    is_equal_split: bool
    from_members: List[ItemDataModel]
    to_members: List[ItemDataModel]


class RecordTests(BaseTestCase):
    """
    Test case class for record-related tests.
    """

    def setUp(self):
        """
        Set up the test data before running each test method.

        It creates a default user, logs in with the default user credentials,
        creates a default group, and creates members for the default group.

        Steps performed in the setup:
        1. Calls the parent class's `setUp` method to ensure the base test case setup is executed.
        2. Creates a record for the default group. This record represents the first record in the group and includes details
        such as the title, amount, type, currency, exchange rate, note, and splitting information.
        3. Creates 'From' and 'To' instances. These instances represent the transactions associated with the first record.
        The 'From' instance specifies the member from whom the money is coming, while the 'To' instances specify the members
        to whom the money is being distributed.
        4. Creates `Balance` instances . These instances represent the balances of the members in the group. The owner member
        has a balance of 300 TWD, and the binded member has a balance of -300 TWD. The balances are specific to the currency
        used in the group.
        """
        super().setUp()

        # Create a record for the default group
        self.first_record = Record.objects.create(
            group=self.default_group,
            what="First record",
            amount="600",
            type="expense",
            currency="TWD",
            exchange_rate=1,
            note="This is the first record.",
            is_equal_split=True,
        )

        # Create 'From' and 'To' instances for the first record
        From.objects.create(
            record=self.first_record,
            member=self.owner_member,
            amount=600,
        )
        To.objects.create(
            record=self.first_record,
            member=self.owner_member,
            amount=-300,
        )
        To.objects.create(
            record=self.first_record,
            member=self.binded_member,
            amount=-300,
        )

        # Create balance instances for the members
        Balance.objects.create(
            member=self.owner_member,
            balance=300,
            currency="TWD",
        )
        Balance.objects.create(
            member=self.binded_member,
            balance=-300,
            currency="TWD",
        )

    def test_retrieve_record(self):
        """
        Test retrieving record.
        """
        response = self.client.get(
            reverse(
                "record-detail",
                kwargs={"group_id": self.default_group.id, "pk": self.first_record.id},
            )
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        try:
            data = response.json()
            record_data = RecordDataModel(**data)
        except ValidationError as e:
            self.fail(incorrect_format_message(e))

    def test_list_record(self):
        """
        Test listing record.
        """
        response = self.client.get(
            reverse("record-list", kwargs={"group_id": self.default_group.id})
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        try:
            data = response.json()
            self.assertIsNotNone(data, list)
            for item in data:
                record_data = RecordDataModel(**item)
        except ValidationError as e:
            self.fail(incorrect_format_message(e))

    def test_create_record(self):
        """
        Test creating record.
        """
        record_data = {
            "group": self.default_group.id,
            "what": "Second record",
            "amount": 600,
            "type": "expense",
            "currency": "TWD",
            "exchange_rate": 1,
            "note": "",
            "is_equal_split": True,
            "from_members": [
                {"amount": 600, "member": self.owner_member.id},
            ],
            "to_members": [
                {"amount": -200, "member": self.owner_member.id},
                {"amount": -200, "member": self.binded_member.id},
                {"amount": -200, "member": self.non_binded_member.id},
            ],
        }
        response = self.client.post(
            reverse(
                "record-list",
                kwargs={"group_id": self.default_group.id},
            ),
            data=record_data,
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        try:
            data = response.json()
            record_data = RecordDataModel(**data)
        except ValidationError as e:
            self.fail(incorrect_format_message(e))

        # Check if members' balances have been updated after creating a record.
        response = self.client.get(
            reverse("members", kwargs={"group_id": self.default_group.id})
        )
        data = response.json()
        for item in data:
            if item["name"] == self.owner_member.name:
                self.assertEqual(item["balances"][0]["balance"], 700)
            if item["name"] == self.binded_member.name:
                self.assertEqual(item["balances"][0]["balance"], -500)
            if item["name"] == self.non_binded_member.name:
                self.assertEqual(item["balances"][0]["balance"], -200)

    def test_update_record(self):
        """
        Test updating record.
        """
        record_data = {
            "amount": 600,
            "from_members": [
                {"amount": 600, "member": self.owner_member.id},
            ],
            "to_members": [
                {"amount": -200, "member": self.owner_member.id},
                {"amount": -200, "member": self.binded_member.id},
                {"amount": -200, "member": self.non_binded_member.id},
            ],
        }
        response = self.client.patch(
            reverse(
                "record-detail",
                kwargs={"group_id": self.default_group.id, "pk": self.first_record.id},
            ),
            data=record_data,
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        try:
            data = response.json()
            record_data = RecordDataModel(**data)
        except ValidationError as e:
            self.fail(incorrect_format_message(e))

        # Check if members' balances have been updated after updating a record.
        response = self.client.get(
            reverse("members", kwargs={"group_id": self.default_group.id})
        )
        data = response.json()
        for item in data:
            if item["name"] == self.owner_member.name:
                self.assertEqual(item["balances"][0]["balance"], 400)
            if item["name"] == self.binded_member.name:
                self.assertEqual(item["balances"][0]["balance"], -200)
            if item["name"] == self.non_binded_member.name:
                self.assertEqual(item["balances"][0]["balance"], -200)

    def test_delete_record(self):
        """
        Test deleting record.
        """
        response = self.client.delete(
            reverse(
                "record-detail",
                kwargs={"group_id": self.default_group.id, "pk": self.first_record.id},
            )
        )
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        # Check if members' balances have been updated after deleting a record.
        response = self.client.get(
            reverse("members", kwargs={"group_id": self.default_group.id})
        )
        data = response.json()
        for item in data:
            self.assertEqual(item["balances"][0]["balance"], 0)
