from socket import *

def run_proxy_server(proxy_ip: str, proxy_port: int, target_ip: str, target_port: int):
    proxy_socket = socket(AF_INET, SOCK_STREAM)
    proxy_socket.bind((proxy_ip, proxy_port))
    proxy_socket.listen(1)

    while True:
        client_socket, client_address = proxy_socket.accept()
        client_request = client_socket.recv(4096).decode('utf-8')
        destination_host, destination_port = extract_destination(client_request)

        try:
            target_socket = socket(AF_INET, SOCK_STREAM)
            target_socket.connect((destination_host, destination_port))
            target_socket.sendall(client_request.encode('utf-8'))
            server_response = b''
            while True:
                data = target_socket.recv(4096)
                if not data:
                    break
                server_response += data

            
            client_socket.sendall(server_response)

        except Exception as e:
            print(f"Error: {e}")
            client_socket.sendall(b"HTTP/1.1 500 Internal Server Error\r\n\r\nProxy Error")
        finally:
            target_socket.close()
            client_socket.close()

def extract_destination(request):

    lines = request.split('\r\n')
    host_line = [line for line in lines if line.startswith('Host')]
    if host_line:
        host = host_line[0].split(' ')[1].split(':')[0]
        port = 80
        return host, port
    else:
        raise ValueError("Host header not found in the request")

if __name__ == '__main__':
    PROXY_IP = 'localhost'
    PROXY_PORT = 8088
    TARGET_IP = 'localhost'
    TARGET_PORT = 8000

    run_proxy_server(PROXY_IP, PROXY_PORT, TARGET_IP, TARGET_PORT)
