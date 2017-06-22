import uuid

import grpc
import grpc._channel
from django.test import TestCase
from google.protobuf import json_format as _json_format

import api_pb2
import api_pb2_grpc


def random_id() -> str:
    return str(uuid.uuid4())


def sample(item_id: str, name='', title='', description='', price=0, pv=0, status=False) -> dict:
    return {
        'id': item_id,
        'name': name,
        'title': title,
        'description': description,
        'price': price,
        'pv': pv,
        'status': status,
    }


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
        input_data = sample(item_id)

        output_data = _json_format.MessageToDict(self._api.AddItem(api_pb2.Item(**input_data)), True)
        self.assertDictEqual({'item': input_data}, output_data)

    def test_GetItem(self):
        item_id = random_id()
        input_data = sample(item_id)

        self._api.AddItem(api_pb2.Item(**input_data))

        output_data = _json_format.MessageToDict(self._api.GetItem(api_pb2.GetItemRequest(id=item_id)), True)
        input_data['pv'] += 1

        self.assertDictEqual(input_data, output_data)

    def test_UpdateItem(self):
        item_id = random_id()
        input_data = sample(item_id)
        update_data = sample(item_id, 'apple', 'banana', 'cherry', 1, 2, True)

        self._api.AddItem(api_pb2.Item(**input_data))

        output_data = _json_format.MessageToDict(
            self._api.UpdateItem(api_pb2.UpdateItemRequest(item=api_pb2.Item(**update_data))), True)
        self.assertDictEqual({'item': update_data}, output_data)

        output_data = _json_format.MessageToDict(self._api.GetItem(api_pb2.GetItemRequest(id=item_id)), True)
        update_data['pv'] += 1

        self.assertDictEqual(update_data, output_data)

    def test_DeleteItem(self):
        item_id = random_id()
        input_data = sample(item_id)
        output_data = None

        self._api.AddItem(api_pb2.Item(**input_data))
        self._api.DeleteItem(api_pb2.DeleteItemRequest(id=item_id))

        with self.assertRaises(grpc._channel._Rendezvous) as e:
            self._api.GetItem(api_pb2.GetItemRequest(id=item_id))

        self.assertEqual(e.exception._state.code, grpc.StatusCode.NOT_FOUND)

    def test_ListItem(self):
        self._api.ListItem(api_pb2.ListItemRequest())
