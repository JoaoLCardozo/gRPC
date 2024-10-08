import grpc
from concurrent import futures
import chat_pb2_grpc
import chat_pb2

class ChatService(chat_pb2_grpc.ChatServiceServicer):
    def __init__(self):
        self.clients = []  # Lista para armazenar os clientes conectados

    def Chat(self, request_iterator, context):
        for new_message in request_iterator:
            print(f"Received message from {new_message.user}: {new_message.message}")
            self.broadcast_message(new_message)
    
    def broadcast_message(self, message):
        for client in self.clients:
            client.put(message)

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    chat_pb2_grpc.add_ChatServiceServicer_to_server(ChatService(), server)
    server.add_insecure_port('[::]:50051')
    server.start()
    print("Chat server started on port 50051")
    server.wait_for_termination()

if __name__ == '__main__':
    serve()