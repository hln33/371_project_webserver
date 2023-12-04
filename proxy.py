from socket import *
import os
from datetime import datetime, timedelta

Cache = {}

def run_proxy_server(proxy_ip: str, proxy_port: int, target_ip: str, target_port: int):
    proxy_socket = socket(AF_INET, SOCK_STREAM)
    proxy_socket.bind((proxy_ip, proxy_port))
    proxy_socket.listen(1)

    while True:
        client_socket, client_address = proxy_socket.accept()
        client_request = client_socket.recv(4096).decode('utf-8')
        destination_host, destination_port = extract_destination(client_request)

        if destination_host not in Cache or not valid_cache(destination_host,client_request):
            target_socket = socket(AF_INET, SOCK_STREAM)
            target_socket.connect((target_ip, target_port))
            target_socket.send(client_request.encode('utf-8'))
            server_response = b''
            while True:
                data = target_socket.recv(4096)
                if not data:
                    break
                server_response += data 
            target_socket.close()
            Cache[destination_host] = (server_response, datetime.now())
            server_response_with_headers = headers_cache(server_response)
            client_socket.sendall(server_response_with_headers)
        else:
            client_socket.sendall(Cache[destination_host][0])
        client_socket.close()

def valid_cache(destination_host, client_request):
    if 'Cache-Control: no-cache' in client_request or 'Cache-Control: max-age=0' in client_request:
        return False   
    elif 'Cache-Control: max-age=' in client_request:
        max_age = int(client_request.split('Cache-Control: max-age=')[1].split('\r\n')[0])
        return datetime.now() < Cache[destination_host][1] + timedelta(seconds=max_age)
    else:
        return datetime.now() < Cache[destination_host][1] + timedelta(minutes=5)
    
def headers_cache(response: bytes) -> bytes:
    headers = b'Cache-Control: max-age=300\r\nExpires: ' + (datetime.now() + timedelta(minutes=5)).strftime('%a, %d %b %Y %H:%M:%S GMT').encode('utf-8') + b'\r\n'
    return response.replace(b'\r\n\r\n', b'\r\n' + headers + b'\r\n')

def extract_destination(request):
    lines = request.split('\r\n')
    host_line = [line for line in lines if line.startswith('Host')]
    if host_line:
        host = host_line[0].split(' ')[1].split(':')[0]
        port = 80
        return host, port
    else:
        raise ValueError("Header not found")

if __name__ == '__main__':
    PROXY_IP = 'localhost'
    PROXY_PORT = 8080
    TARGET_IP = 'localhost'
    TARGET_PORT = 8000
    run_proxy_server(PROXY_IP, PROXY_PORT, TARGET_IP, TARGET_PORT)
