from socket import *


def handle_request(request_data):
    print(request_data)


def run_server(ip_addr: str, port: int):
    server_socket = socket(AF_INET, SOCK_STREAM)
    server_socket.bind((ip_addr, port))
    server_socket.listen(1)

    while True:
        client_socket, client_address = server_socket.accept()
        request_data = client_socket.recvfrom(1024)
        handle_request(request_data)


if __name__ == '__main__':
    IP_ADDR = 'localhost'
    PORT_NUMBER = 8000
    run_server(IP_ADDR, PORT_NUMBER)
