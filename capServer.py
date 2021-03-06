import os
import time
from concurrent import futures

import grpc
from opencensus.common.transports.async_ import AsyncTransport
from opencensus.ext.grpc import server_interceptor
from opencensus.ext.stackdriver import trace_exporter
from opencensus.trace.samplers import always_on
from opencensus.trace.tracer import Tracer


import defs_pb2_grpc as proto
import defs_pb2 as pb

exporter = trace_exporter.StackdriverExporter(
    project_id=os.environ.get("GOOGLE_CLOUD_PROJECT"),
    transport=AsyncTransport,
)


class CapitalizeServer(proto.FetchServicer):
    def __init__(self, *args, **kwargs):
        super(CapitalizeServer, self).__init__()

    def Capitalize(self, request, context):
        tracer = Tracer(sampler=always_on.AlwaysOnSampler(), exporter=exporter)
        with tracer.span(name="Capitalize") as span:
            data = request.data
            span.add_annotation("Data in", len=len(data))
            return pb.Payload(data=request.data.upper())


def main():
    # Set up the gRPC integration/interceptor
    tracer_interceptor = server_interceptor.OpenCensusServerInterceptor(
        always_on.AlwaysOnSampler()
    )

    server = grpc.server(
        futures.ThreadPoolExecutor(max_workers=10),
        interceptors=(tracer_interceptor,),
    )

    proto.add_FetchServicer_to_server(CapitalizeServer(), server)
    server.add_insecure_port("[::]:9778")
    server.start()

    try:
        while True:
            time.sleep(3600)
    except KeyboardInterrupt:
        server.stop(0)


if __name__ == "__main__":
    main()
