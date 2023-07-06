import time
from concurrent import futures

import grpc
import location_pb2
import location_pb2_grpc


class LocationServicer(location_pb2_grpc.LocationServiceServicer):
    def Get(self, request, context):
        first_location = location_pb2.LocationMessage(
            id=29,
            person_id=1,
            coordinate="010100000000ADF9F197925EC0FDA19927D7C64240",
            creation_time='2020-08-18 10:37:06.000000'
        )

        second_location = location_pb2.LocationMessage(
            id=3333,
            person_id=5,
            coordinate='010100000097FDBAD39D925EC0D00A0C59DDC64240',
            creation_time='2020-08-15 10:37:06.000000'
        )

        result = location_pb2.LocationMessageList()
        result.locations.extend([first_location, second_location])
        return result

    def Create(self, request, context):
        print("Received a message!")

        request_value = {
            "id": request.id,
            "person_id": request.person_id,
            "coordinate": request.coordinate,
            "creation_time": request.creation_time
        }
        print(request_value)

        return location_pb2.LocationMessage(**request_value)


# Initialize gRPC server
server = grpc.server(futures.ThreadPoolExecutor(max_workers=2))
location_pb2_grpc.add_LocationServiceServicer_to_server(LocationServicer(), server)


print("Server starting on port 5005...")
server.add_insecure_port("[::]:5005")
server.start()
# Keep thread alive
try:
    while True:
        time.sleep(86400)
except KeyboardInterrupt:
    server.stop(0)