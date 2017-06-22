import grpc
from django.test import TestCase

import api_pb2
import api_pb2_grpc

import uuid


def random_id() -> str:
    return str(uuid.uuid4())


class APITest(TestCase):
    @classmethod
    def setUpClass(cls):
        channel = grpc.insecure_channel('localhost:3000')
        cls._api = api_pb2_grpc.APIStub(channel)

    @classmethod
    def tearDownClass(cls):
        pass  # TODO: How to close the connection?

    def test_AddItem(self):
        item_id = random_id()

        self._api.AddItem(api_pb2.Item(
            id=item_id,
            name='a',
            title='a',
            description='a',
            price=1,
            pv=1,
            status=True,
        ))

    def test_GetItem(self):
        item_id = random_id()

        self._api.AddItem(api_pb2.Item(
            id=item_id,
            name='a',
            title='a',
            description='a',
            price=1,
            pv=1,
            status=True,
        ))

        self._api.GetItem(api_pb2.GetItemRequest(
            id=item_id
        ))

    def test_UpdateItem(self):
        item_id = random_id()

        self._api.AddItem(api_pb2.Item(
            id=item_id,
            name='a',
            title='a',
            description='a',
            price=1,
            pv=1,
            status=True,
        ))

        self._api.UpdateItem(api_pb2.UpdateItemRequest(
            item=api_pb2.Item(
                id=item_id,
                name='b',
                title='b',
                description='b',
                price=1,
                pv=1,
                status=True,
            )
        ))

    def test_DeleteItem(self):
        item_id = random_id()

        self._api.AddItem(api_pb2.Item(
            id=item_id,
            name='a',
            title='a',
            description='a',
            price=1,
            pv=1,
            status=True,
        ))

        self._api.DeleteItem(api_pb2.DeleteItemRequest(
            id=item_id,
        ))

    def test_ListItem(self):
        self._api.ListItem(api_pb2.ListItemRequest())
