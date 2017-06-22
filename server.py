import json
import time
from concurrent import futures

import grpc
from django.core.exceptions import ValidationError
from django.db.models import F
from django.forms.models import model_to_dict
from google.protobuf import json_format as _json_format

import api_pb2
import api_pb2_grpc
import db.models
import db.views


def convert(item: db.models.Item) -> api_pb2.Item:
    return api_pb2.Item(**model_to_dict(item))


class APIServicer(api_pb2_grpc.APIServicer):
    def AddItem(self, request: api_pb2.Item, context: grpc.ServicerContext) -> api_pb2.AddItemResponse:
        try:
            item = db.models.Item(**_json_format.MessageToDict(request, including_default_value_fields=True))
            item.full_clean()
            item.save()
            return api_pb2.AddItemResponse(item=convert(item))
        except ValidationError as e:  # TODO: Return correct status code by exception types
            context.set_code(grpc.StatusCode.INTERNAL)
            context.set_details(json.dumps(e.messages))
            return api_pb2.AddItemResponse()

    def GetItem(self, request: api_pb2.GetItemRequest, context: grpc.ServicerContext) -> api_pb2.Item:
        try:
            item = db.models.Item.objects.get(id=request.id)
            item.pv = F('pv') + 1
            item.save()
            item.refresh_from_db()
            return convert(item)
        except db.models.Item.DoesNotExist:
            context.set_code(grpc.StatusCode.NOT_FOUND)
            context.set_details('Item does not exist')
            return api_pb2.Item()

    def UpdateItem(self, request: api_pb2.UpdateItemRequest,
                   context: grpc.ServicerContext) -> api_pb2.UpdateItemResponse:
        try:
            item = db.models.Item.objects.get(id=request.item.id)
            item.__dict__.update(_json_format.MessageToDict(request, including_default_value_fields=True)['item'])
            item.full_clean()
            item.save()
            return api_pb2.UpdateItemResponse(item=convert(item))
        except db.models.Item.DoesNotExist:
            context.set_code(grpc.StatusCode.NOT_FOUND)
            context.set_details('Item does not exist')
            return api_pb2.UpdateItemResponse()
        except ValidationError as e:  # TODO: Return correct status code by exception types
            context.set_code(grpc.StatusCode.INTERNAL)
            context.set_details(json.dumps(e.messages))
            return api_pb2.UpdateItemResponse()

    def DeleteItem(self, request: api_pb2.DeleteItemRequest,
                   context: grpc.ServicerContext) -> api_pb2.DeleteItemResponse:
        try:
            db.models.Item.objects.get(id=request.id).delete()
            return api_pb2.DeleteItemResponse()
        except db.models.Item.DoesNotExist:
            context.set_code(grpc.StatusCode.NOT_FOUND)
            context.set_details('Item does not exist')
            return api_pb2.Item()

    def ListItem(self, request: api_pb2.ListItemRequest, context: grpc.ServicerContext) -> api_pb2.ListItemResponse:
        context.set_code(grpc.StatusCode.INTERNAL)
        context.set_details('Not implemented')
        return api_pb2.ListItemResponse()


def serve() -> None:
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    api_pb2_grpc.add_APIServicer_to_server(APIServicer(), server)
    server.add_insecure_port('[::]:3000')
    server.start()
    try:
        while True:
            time.sleep(86400)
    except KeyboardInterrupt:
        server.stop(0)


if __name__ == '__main__':
    serve()
