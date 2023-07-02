import time
from concurrent import futures

import grpc
import person_pb2
import person_pb2_grpc


class PersonServicer(person_pb2_grpc.PersonServiceServicer):
    def Get(self, request, context):
        first_person = person_pb2.PersonMessage(
            id="8",
            first_name="Paul",
            last_name="Badman",
            company_name='Paul Badman & Associates'
        )

        second_person = person_pb2.PersonMessage(
            id="9",
            first_name="Otto",
            last_name="Spring",
            company_name='The Chicken Sisters Restaurant'
        )

        result = person_pb2.PersonMessageList()
        result.orders.extend([first_person, second_person])
        return result

    def Create(self, request, context):
        print("Received a message!")

        request_value = {
            "id": request.id,
            "first_name": request.first_name,
            "last_name": request.last_name,
            "company_name": request.company_name
        }
        print(request_value)

        return person_pb2.OrderMessage(**request_value)


# Initialize gRPC server
server = grpc.server(futures.ThreadPoolExecutor(max_workers=2))
person_pb2_grpc.add_PersonServiceServicer_to_server(PersonServicer(), server)


print("Server starting on port 5005...")
server.add_insecure_port("[::]:5005")
server.start()
# Keep thread alive
try:
    while True:
        time.sleep(86400)
except KeyboardInterrupt:
    server.stop(0)
