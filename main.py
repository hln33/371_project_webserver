from socket import *
import os


def get_file_content(file_path):
    if os.path.isfile(file_path):
        with open(file_path, 'rb') as file:
            content = file.read()
            print(content)
    else:
        print('error')


def handle_request(http_request: str):
    lines = http_request.split('\r\n')

    # first line in http request is the request line
    request_line = lines[0]
    request_type = request_line.split()[0]
    file_path = os.getcwd() + request_line.split()[1]
    get_file_content(file_path)


def run_server(ip_addr: str, port: int):
    server_socket = socket(AF_INET, SOCK_STREAM)
    server_socket.bind((ip_addr, port))
    server_socket.listen(1)

    while True:
        client_socket, client_address = server_socket.accept()
        request_data = client_socket.recvfrom(1024)[0].decode('ascii')
        handle_request(request_data)
        client_socket.close()


if __name__ == '__main__':
    IP_ADDR = 'localhost'
    PORT_NUMBER = 8005
    run_server(IP_ADDR, PORT_NUMBER)
