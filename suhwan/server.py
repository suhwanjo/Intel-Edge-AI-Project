import socket
import json

def start_server(host='0.0.0.0', port=5000):
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((host, port))
    server_socket.listen(1)
    print(f"Listening on {host}:{port}")

    while True:
        client_socket, addr = server_socket.accept()
        print(f"Connection from {addr}")

        data = client_socket.recv(1024).decode('utf-8')
        if data:
            try:
                data = json.loads(data)
                # 데이터 처리 로직 추가 (예: 화면에 출력)
                print("Received data:", data)
            except json.JSONDecodeError:
                print("Received invalid JSON data")

        client_socket.close()

if __name__ == "__main__":
    start_server()
