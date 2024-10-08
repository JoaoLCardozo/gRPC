import grpc
import chat_pb2
import chat_pb2_grpc
import threading

def receive_messages(stub):
    for message in stub.Chat(iter([])):  # Recebe mensagens do servidor
        print(f"{message.user}: {message.message}")

def send_messages(stub, user_name):
    def message_generator():
        while True:
            message = input(f"{user_name}: ")  # Coleta a mensagem do usuário
            yield chat_pb2.ChatMessage(user=user_name, message=message)

    # Envia as mensagens usando o streaming bidirecional
    stub.Chat(message_generator())

def run(user_name):
    with grpc.insecure_channel('localhost:50051') as channel:
        stub = chat_pb2_grpc.ChatServiceStub(channel)

        # Thread para receber mensagens
        receive_thread = threading.Thread(target=receive_messages, args=(stub,))
        receive_thread.start()

        # Enviar mensagens para o servidor
        send_messages(stub, user_name)

if __name__ == '__main__':
    user_name = input("Enter your username: ")  # Solicita o nome do usuário
    run(user_name)