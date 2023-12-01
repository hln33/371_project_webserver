from socket import *
import os


def get_file_content(file_path):
    if os.path.isfile(file_path):
        with open(file_path, 'rb') as file:
            content = file.read()
            return content
    else:
        return b''


def construct_http_response(status_line: str, data: str) -> bytes:
    response = f'HTTP/1.1 {status_line}\r\n\r\n{data}'
    return response.encode('utf-8')


def handle_request(http_request: str):
    lines = http_request.split('\r\n')

    # first line in http request is the request line
    request_line = lines[0]
    request_type = request_line.split()[0]
    file_path = os.getcwd() + request_line.split()[1]

    status_line = '400 Bad Request'
    data = '400 Bad Request'
    if request_type == 'GET':
        content = get_file_content(file_path)
        if "If-Modified-Since" in http_request:
            status_line = '304 Not Modified'
            data = '304 Not Modified'
        elif content:
            status_line = '200 Ok'
            data = content.decode('utf-8')
        else:
            status_line = '404 Not Found'
            data = '404 Not Found'
    return construct_http_response(status_line, data)


def run_server(ip_addr: str, port: int):
    server_socket = socket(AF_INET, SOCK_STREAM)
    server_socket.bind((ip_addr, port))
    server_socket.listen(1)

    while True:
        client_socket, client_address = server_socket.accept()
        request_data = client_socket.recvfrom(1024)[0].decode('ascii')
        response = handle_request(request_data)
        client_socket.send(response)
        client_socket.close()


if __name__ == '__main__':
    IP_ADDR = 'localhost'
    PORT_NUMBER = 8000
    run_server(IP_ADDR, PORT_NUMBER)
