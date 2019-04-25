import grpc
import time
from concurrent import futures

import defs_pb2_grpc as proto
import defs_pb2 as pb

class CapitalizeServer(proto.FetchServicer):
    def __init__(self, *args, **kwargs):
        super(CapitalizeServer, self).__init__()

    def Capitalize(self, request, context):
        return pb.Payload(data=request.data.upper())


def main():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    proto.add_FetchServicer_to_server(CapitalizeServer(), server)
    server.add_insecure_port('[::]:9778')
    server.start()

    try:
        while True:
            time.sleep(3600)
    except KeyboardInterrupt:
        server.stop(0)

if __name__ == "__main__":
    main()
