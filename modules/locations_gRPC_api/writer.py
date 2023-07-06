import grpc
import location_pb2
import location_pb2_grpc

"""
Sample implementation of a writer that can be used to write messages to gRPC.
"""

print("Sending sample payload...")

channel = grpc.insecure_channel("localhost:5005")
stub = location_pb2_grpc.LocationServiceStub(channel)

# Update this with desired payload
location = location_pb2.LocationMessage(
    id=29,
    person_id=1,
    coordinate="010100000000ADF9F197925EC0FDA19927D7C64240",
    creation_time='2020-08-18 10:37:06.000000'
)


response = stub.Create(location)
