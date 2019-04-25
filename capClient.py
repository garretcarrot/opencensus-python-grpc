import grpc

import defs_pb2_grpc as proto
import defs_pb2 as pb

def main():
    channel = grpc.insecure_channel('localhost:9778')
    stub = proto.FetchStub(channel)

    while True:
        line_in = input('> ')
        capitalized = stub.Capitalize(pb.Payload(data=bytes(line_in, encoding='utf-8')))
        print('< %s\n' % capitalized.data.decode('utf-8'))

if __name__ == "__main__":
    main()
