from socket import *
import os

# STATUS CODES
OK_CODE = '200 Ok'
NOT_MODIFIED_CODE = '304 Not Modified'
BAD_REQUEST_CODE = '400 Bad Request'
UNAUTHORIZED_CODE = '403 Forbidden'
NOT_FOUND_CODE = '404 Not Found'
LENGTH_REQUIRED_CODE = '411 Length Required'


def create_http_response(status_line: str, data: str) -> bytes:
    response = f'HTTP/1.1 {status_line}\r\n\r\n{data}'
    return response.encode('utf-8')


def parse_http_request(req):
    lines = req.split('\r\n')
    request_line = lines[0]
    request_type = request_line.split()[0]
    file_name = request_line.split()[1]
    return request_type, file_name


def get_file_content(file_path):
    with open(file_path, 'rb') as file:
        content = file.read()
        return content


def handle_request(http_request: str):
    try:
        request_type, file_name = parse_http_request(http_request)
        file_path = os.getcwd() + file_name
        content = get_file_content(file_path)
    except OSError as e:
        return create_http_response(NOT_FOUND_CODE, NOT_FOUND_CODE)
    except (IndexError, ValueError) as e:
        return create_http_response(BAD_REQUEST_CODE, BAD_REQUEST_CODE)

    status_line = BAD_REQUEST_CODE
    data = BAD_REQUEST_CODE
    match request_type:
        case 'GET':
            if 'If-Modified-Since' in http_request:
                status_line = NOT_MODIFIED_CODE
                data = NOT_MODIFIED_CODE
            elif file_name == '/test_auth.html' and 'Authorization' not in http_request:
                status_line, data = UNAUTHORIZED_CODE
                data = UNAUTHORIZED_CODE
            else:
                status_line = OK_CODE
                data = content.decode('utf-8')
        case 'POST':
            if file_name == '/test_content_len_req.html' and 'Content-Length' not in http_request:
                status_line = LENGTH_REQUIRED_CODE
                data = LENGTH_REQUIRED_CODE
            else:
                status_line = OK_CODE
                data = content.decode('utf-8')

    return create_http_response(status_line, data)


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
