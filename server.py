import grpc
import api_pb2
import api_pb2_grpc
from concurrent import futures
import time


class APIServicer(api_pb2_grpc.APIServicer):
    def AddItem(self, request, context):
        pass

    def GetItem(self, request, context):
        pass

    def UpdateItem(self, request, context):
        pass

    def DeleteItem(self, request, context):
        pass

    def ListItem(self, request, context):
        pass


def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    api_pb2_grpc.add_APIServicer_to_server(APIServicer, server)
    server.add_insecure_port('[::]:3000')
    server.start()
    try:
        while True:
            time.sleep(86400)
    except KeyboardInterrupt:
        server.stop(0)


if __name__ == '__main__':
    serve()
